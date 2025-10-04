"""
AI创作路由 - 使用Google Gemini
"""
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import google.generativeai as genai
import os
import httpx
import base64
from io import BytesIO

router = APIRouter()

# 配置Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# 会话存储（生产环境应使用Redis等）
sessions: Dict[str, Dict[str, Any]] = {}


class Message(BaseModel):
    role: str  # "user" 或 "assistant"
    content: str


class CreateRequest(BaseModel):
    doc_id: str
    blocks: List[dict]
    instruction: str
    session_id: Optional[str] = None


class RefineRequest(BaseModel):
    session_id: str
    instruction: str


class AIResponse(BaseModel):
    session_id: str
    content: str
    messages: List[Message]


@router.post("/create", response_model=AIResponse)
async def create_article(
    request: CreateRequest,
    authorization: str = Header(...)
):
    """
    首次生成文章
    """
    try:
        print(f"AI Create request received: doc_id={request.doc_id}, blocks_count={len(request.blocks)}")
        
        # 检查Gemini API Key
        gemini_key = os.getenv("GEMINI_API_KEY")
        if not gemini_key:
            raise HTTPException(status_code=500, detail="Gemini API Key未配置")
        
        print(f"Gemini API Key configured: {gemini_key[:10]}...")
        
        token = authorization.replace("Bearer ", "")
        
        # 准备内容
        text_content = []
        image_parts = []
        
        async with httpx.AsyncClient() as client:
            for block in request.blocks:
                if block.get("block_type") == "text" and block.get("text"):
                    text_content.append(block["text"])
                    
                elif block.get("block_type") == "image" and block.get("image_token"):
                    # 下载图片
                    try:
                        img_response = await client.get(
                            f"https://open.feishu.cn/open-apis/drive/v1/medias/{block['image_token']}/download",
                            headers={"Authorization": f"Bearer {token}"}
                        )
                        if img_response.status_code == 200:
                            image_parts.append({
                                "mime_type": "image/jpeg",
                                "data": base64.b64encode(img_response.content).decode()
                            })
                    except Exception as e:
                        print(f"下载图片失败: {e}")
        
        # 构建prompt
        combined_text = "\n\n".join(text_content)
        
        system_prompt = """你是一位专业的内容创作助手。你的任务是将用户提供的草稿内容重新组织成一篇结构清晰、逻辑连贯的文章。

要求：
1. 保持原文的核心信息和观点
2. 优化文章结构，使其更有逻辑性
3. 改善语言表达，使其更流畅自然
4. 如果有图片，在合适的位置用 ![图片描述](image_N) 标记插入位置，N是图片序号（从1开始）
5. 使用Markdown格式输出
6. 保持专业且易读的写作风格
"""

        user_prompt = f"""原始内容：
{combined_text}

用户指示：
{request.instruction}

请根据以上内容和指示，创作一篇高质量的文章。"""

        if image_parts:
            user_prompt += f"\n\n注意：文档中包含 {len(image_parts)} 张图片，请在文章合适位置标记图片插入点。"
        
        # 调用Gemini API
        print("Initializing Gemini model...")
        model = genai.GenerativeModel("gemini-1.5-pro")
        
        # 构建消息内容
        contents = [user_prompt]
        print(f"Generated prompt length: {len(user_prompt)}")
        
        print("Calling Gemini API...")
        response = model.generate_content(
            contents,
            generation_config=genai.GenerationConfig(
                temperature=0.7,
                max_output_tokens=4096,
            )
        )
        
        print("Gemini API response received")
        generated_text = response.text
        print(f"Generated text length: {len(generated_text)}")
        
        # 创建会话
        session_id = f"{request.doc_id}_{os.urandom(8).hex()}"
        
        sessions[session_id] = {
            "doc_id": request.doc_id,
            "original_blocks": request.blocks,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
                {"role": "assistant", "content": generated_text}
            ],
            "current_article": generated_text,
            "images": image_parts
        }
        
        return AIResponse(
            session_id=session_id,
            content=generated_text,
            messages=[
                Message(role="user", content=request.instruction),
                Message(role="assistant", content="已生成文章")
            ]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI生成失败: {str(e)}")


@router.post("/refine", response_model=AIResponse)
async def refine_article(request: RefineRequest):
    """
    多轮对话精修文章
    """
    try:
        # 获取会话
        session = sessions.get(request.session_id)
        if not session:
            raise HTTPException(status_code=404, detail="会话不存在")
        
        # 构建新的prompt
        current_article = session["current_article"]
        
        refine_prompt = f"""当前文章版本：
{current_article}

用户的修改要求：
{request.instruction}

请根据用户的要求对文章进行修改，输出完整的修改后文章（使用Markdown格式）。"""

        # 添加到消息历史
        session["messages"].append({
            "role": "user",
            "content": refine_prompt
        })
        
        # 调用Gemini
        model = genai.GenerativeModel("gemini-1.5-pro")
        
        # 使用历史消息（保留上下文）
        chat = model.start_chat(history=[
            {"role": msg["role"], "parts": [msg["content"]]}
            for msg in session["messages"][1:-1]  # 排除system和最新的user消息
            if msg["role"] in ["user", "model"]
        ])
        
        response = chat.send_message(refine_prompt)
        refined_text = response.text
        
        # 更新会话
        session["messages"].append({
            "role": "assistant",
            "content": refined_text
        })
        session["current_article"] = refined_text
        
        # 构建消息列表
        messages = []
        for msg in session["messages"][1:]:  # 跳过system消息
            if msg["role"] in ["user", "assistant"]:
                # 简化显示
                if "当前文章版本" in msg["content"]:
                    # 这是精修请求，只显示用户指令部分
                    if msg["role"] == "user":
                        instruction_part = msg["content"].split("用户的修改要求：")[-1].split("\n\n请根据")[0].strip()
                        messages.append(Message(role="user", content=instruction_part))
                    else:
                        messages.append(Message(role="assistant", content="已更新文章"))
                elif msg["role"] == "user":
                    # 首次创建请求
                    if "用户指示：" in msg["content"]:
                        instruction = msg["content"].split("用户指示：")[-1].split("\n\n请根据")[0].strip()
                        messages.append(Message(role="user", content=instruction))
        
        return AIResponse(
            session_id=request.session_id,
            content=refined_text,
            messages=messages
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"精修失败: {str(e)}")


@router.delete("/session/{session_id}")
async def reset_session(session_id: str):
    """
    重置会话
    """
    if session_id in sessions:
        del sessions[session_id]
        return {"message": "会话已重置"}
    raise HTTPException(status_code=404, detail="会话不存在")


@router.get("/session/{session_id}")
async def get_session(session_id: str):
    """
    获取会话信息
    """
    session = sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")
    
    return {
        "session_id": session_id,
        "doc_id": session["doc_id"],
        "message_count": len(session["messages"]),
        "current_article": session["current_article"]
    }


