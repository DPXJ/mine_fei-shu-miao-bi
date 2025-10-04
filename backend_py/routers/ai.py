"""
AI创作路由 - 支持多种AI提供商（Gemini, DeepSeek）
"""
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import httpx
import base64
from io import BytesIO

# 导入AI提供商
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from ai_provider import AIProvider

router = APIRouter()

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
        
        system_prompt = """你是一位专业的内容创作和排版助手。你的任务是：
1. **理解图片内容**：仔细分析每张图片的内容、主题和信息
2. **智能排版**：根据图片内容和文本内容的关联性，将图片插入到文章最合适的位置
3. **重新组织**：优化文章结构，使文字和图片协同表达，逻辑连贯
4. **改善表达**：优化语言，使其流畅自然、专业易读

⚠️ 重要：图片格式要求
- 使用Markdown格式
- **必须**使用这个精确格式标记图片：![图片描述](image_1)、![图片描述](image_2)
- 图片编号从1开始，依次为 image_1, image_2, image_3...
- ❌ 错误示例：![图片](image1.jpg)、![图片](img_1)、![图片](picture1)
- ✅ 正确示例：![产品外观](image_1)、![功能演示](image_2)
- 图片描述应该简洁说明图片内容
- 确保图片位置与其相关内容紧密相连
- 保持原文的核心信息和观点
"""

        user_prompt = f"""原始文本内容：
{combined_text}

用户指示：
{request.instruction}

任务：请根据文本和图片内容，创作一篇高质量的文章，并将图片智能地插入到最合适的位置。"""

        if image_parts:
            user_prompt += f"\n\n📷 文档中包含 {len(image_parts)} 张图片，请：\n1. 仔细理解每张图片的内容\n2. 根据图片与文本的关联性，将图片插入到最合适的位置\n3. 为每张图片添加简洁的描述"
        else:
            user_prompt += "\n\n注意：文档中没有图片。"
        
        # 初始化AI提供商
        ai_provider_name = os.getenv("AI_PROVIDER", "gemini")
        print(f"Using AI Provider: {ai_provider_name}")
        print(f"Generated prompt length: {len(user_prompt)}")
        print(f"Number of images: {len(image_parts)}")
        
        try:
            ai_provider = AIProvider.create(ai_provider_name)
            
            # 检查是否支持多模态
            if image_parts and not ai_provider.supports_multimodal():
                print(f"⚠️ Warning: {ai_provider_name} does not support image understanding")
                user_prompt += f"\n\n⚠️ 注意：当前AI模型（{ai_provider_name}）不支持图片理解，仅能根据文本内容创作。建议切换到支持多模态的模型（如Gemini或千问VL）以实现图片理解和智能排版功能。"
            
            # 调用AI生成（传入图片）
            generated_text = ai_provider.generate(user_prompt, images=image_parts, timeout=60)
            print(f"Generated text length: {len(generated_text)}")
            
            # 修正可能的图片格式错误
            import re
            # 修正 image1.jpg -> image_1
            generated_text = re.sub(r'!\[([^\]]*)\]\(image(\d+)\.(?:jpg|png|jpeg|gif)\)', r'![\1](image_\2)', generated_text)
            # 修正 img_1 -> image_1
            generated_text = re.sub(r'!\[([^\]]*)\]\(img_(\d+)\)', r'![\1](image_\2)', generated_text)
            # 修正 picture1 -> image_1
            generated_text = re.sub(r'!\[([^\]]*)\]\(picture(\d+)\)', r'![\1](image_\2)', generated_text)
            print(f"After format fix: {len(generated_text)}")
                    
        except TimeoutError as e:
            print(f"AI API call timed out: {e}")
            # 如果超时，返回带提示的示例响应
            generated_text = f"""# ⚠️ AI生成超时

**问题：** API请求超时（30秒）

**可能原因：**
1. 网络连接问题（国内访问Gemini需要VPN）
2. API服务暂时不可用
3. 请求内容过长

**建议：**
1. 如果使用Gemini：请开启VPN后重试
2. 切换到DeepSeek（国内访问更稳定）：
   - 获取DeepSeek API Key: https://platform.deepseek.com
   - 在.env文件中添加：`DEEPSEEK_API_KEY=你的key`
   - 在.env文件中添加：`AI_PROVIDER=deepseek`

---

## 基于文档内容的文章预览

{combined_text[:500]}...

*重新配置后请再次点击生成*"""
            print("Using fallback content due to timeout")
            
        except Exception as e:
            print(f"AI API call failed: {e}")
            # 如果其他错误，返回错误提示
            generated_text = f"""# ❌ AI生成失败

**错误信息：** {str(e)}

**建议：**
1. 检查API Key是否正确配置
2. 确认网络连接正常
3. 如果使用Gemini需要VPN
4. 考虑切换到DeepSeek（国内访问更稳定）

---

## 文档内容预览

{combined_text[:500]}...

*解决问题后请再次尝试*"""
            print("Using fallback content due to error")
        
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
        images = session.get("images", [])
        
        refine_prompt = f"""当前文章版本：
{current_article}

用户的修改要求：
{request.instruction}

请根据用户的要求对文章进行修改，输出完整的修改后文章（使用Markdown格式）。"""

        if images:
            refine_prompt += f"\n\n⚠️ 重要：文档中有 {len(images)} 张图片\n"
            refine_prompt += "- **必须**使用精确格式：![图片描述](image_1)、![图片描述](image_2)...\n"
            refine_prompt += "- ❌ 错误：![图片](image1.jpg)、![图片](img_1)\n"
            refine_prompt += "- ✅ 正确：![产品外观](image_1)、![功能演示](image_2)"

        # 添加到消息历史
        session["messages"].append({
            "role": "user",
            "content": refine_prompt
        })
        
        # 使用当前配置的AI提供商
        ai_provider_name = os.getenv("AI_PROVIDER", "gemini")
        print(f"Refine using AI Provider: {ai_provider_name}")
        
        try:
            ai_provider = AIProvider.create(ai_provider_name)
            
            # 检查是否支持多模态（如果有图片）
            if images and not ai_provider.supports_multimodal():
                refine_prompt += f"\n\n⚠️ 注意：当前AI模型（{ai_provider_name}）不支持图片理解，仅能根据文本内容精修。"
            
            # 调用AI生成（传入图片以保持上下文）
            refined_text = ai_provider.generate(refine_prompt, images=images if ai_provider.supports_multimodal() else [], timeout=60)
            print(f"Refined text length: {len(refined_text)}")
            
            # 修正可能的图片格式错误
            import re
            refined_text = re.sub(r'!\[([^\]]*)\]\(image(\d+)\.(?:jpg|png|jpeg|gif)\)', r'![\1](image_\2)', refined_text)
            refined_text = re.sub(r'!\[([^\]]*)\]\(img_(\d+)\)', r'![\1](image_\2)', refined_text)
            refined_text = re.sub(r'!\[([^\]]*)\]\(picture(\d+)\)', r'![\1](image_\2)', refined_text)
            print(f"After format fix: {len(refined_text)}")
                
        except TimeoutError as e:
            print(f"Refine API call timed out: {e}")
            refined_text = f"""# ⚠️ AI精修超时

请求超时，请检查网络连接后重试。

当前文章版本：
{current_article}"""
            
        except Exception as e:
            print(f"Refine API call failed: {e}")
            raise HTTPException(status_code=500, detail=f"精修失败: {str(e)}")
        
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


@router.get("/preview/{session_id}")
async def preview_article(session_id: str):
    """
    预览重新排版后的文章（包含图片）
    返回文章内容和图片数据，用于前端渲染
    """
    session = sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="会话不存在")
    
    return {
        "session_id": session_id,
        "doc_id": session["doc_id"],
        "article_content": session["current_article"],
        "images": session.get("images", []),  # 图片数据（base64）
        "original_blocks": session.get("original_blocks", [])
    }