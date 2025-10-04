"""
飞书文档操作路由
"""
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel
from typing import List, Optional
import httpx
import os

router = APIRouter()


class Document(BaseModel):
    doc_id: str
    title: str
    doc_type: str
    updated_at: str
    url: str


class DocumentListResponse(BaseModel):
    documents: List[Document]
    has_more: bool


class ContentBlock(BaseModel):
    block_id: str
    block_type: str
    text: Optional[str] = None
    image_token: Optional[str] = None
    image_url: Optional[str] = None


class DocumentContent(BaseModel):
    doc_id: str
    title: str
    blocks: List[ContentBlock]


@router.get("/list", response_model=DocumentListResponse)
async def get_documents(
    authorization: str = Header(...),
    page_size: int = 20,
    page_token: Optional[str] = None,
    order_by: str = "EditedTime",
    direction: str = "DESC"
):
    """
    获取用户的飞书文档列表
    """
    try:
        # 提取token
        token = authorization.replace("Bearer ", "")
        
        async with httpx.AsyncClient() as client:
            # 获取文档列表
            params = {
                "page_size": page_size,
                "order_by": order_by,
                "direction": direction
            }
            if page_token:
                params["page_token"] = page_token
                
            response = await client.get(
                "https://open.feishu.cn/open-apis/drive/v1/files",
                headers={"Authorization": f"Bearer {token}"},
                params=params
            )
            
            data = response.json()
            
            if data.get("code") != 0:
                raise HTTPException(
                    status_code=400,
                    detail=f"获取文档列表失败: {data.get('msg')}"
                )
            
            files = data.get("data", {}).get("files", [])
            has_more = data.get("data", {}).get("has_more", False)
            
            # 过滤出文档类型（docx）
            documents = []
            for file in files:
                if file.get("type") == "docx":
                    # 处理时间戳 - 飞书返回的是毫秒级时间戳
                    modified_time = file.get("modified_time", "")
                    if modified_time:
                        try:
                            # 飞书时间戳是毫秒级，需要转换为秒级
                            timestamp = int(modified_time) / 1000
                            from datetime import datetime
                            dt = datetime.fromtimestamp(timestamp)
                            modified_time = dt.strftime("%Y-%m-%d %H:%M:%S")
                        except (ValueError, TypeError):
                            modified_time = "未知时间"
                    else:
                        modified_time = "未知时间"
                    
                    documents.append(Document(
                        doc_id=file.get("token"),
                        title=file.get("name", "未命名文档"),
                        doc_type=file.get("type"),
                        updated_at=modified_time,
                        url=file.get("url", "")
                    ))
            
            return DocumentListResponse(
                documents=documents,
                has_more=has_more
            )
            
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"网络请求失败: {str(e)}")


@router.get("/content/{doc_id}", response_model=DocumentContent)
async def get_document_content(
    doc_id: str,
    authorization: str = Header(...)
):
    """
    获取文档内容（文本和图片）
    """
    try:
        token = authorization.replace("Bearer ", "")
        
        async with httpx.AsyncClient() as client:
            # 获取文档元数据
            doc_response = await client.get(
                f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            doc_data = doc_response.json()
            
            if doc_data.get("code") != 0:
                raise HTTPException(
                    status_code=400,
                    detail=f"获取文档失败: {doc_data.get('msg')}"
                )
            
            title = doc_data.get("data", {}).get("document", {}).get("title", "未命名")
            
            # 直接使用blocks API获取文档内容（按照官方文档）
            print(f"Fetching blocks for doc_id: {doc_id}")
            blocks_response = await client.get(
                f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}/blocks",
                headers={"Authorization": f"Bearer {token}"},
                params={
                    "page_size": 500,
                    "document_revision_id": -1,  # 获取最新版本
                    "user_id_type": "open_id"
                }
            )
            
            blocks_data = blocks_response.json()
            print(f"Blocks API response code: {blocks_data.get('code')}")
            print(f"Blocks API response: {blocks_data}")
            
            if blocks_data.get("code") != 0:
                raise HTTPException(
                    status_code=400,
                    detail=f"获取文档blocks失败: {blocks_data.get('msg')} (code: {blocks_data.get('code')})"
                )
            
            raw_blocks = blocks_data.get("data", {}).get("items", [])
            print(f"Found {len(raw_blocks)} blocks")
            
            # 解析内容块
            content_blocks = []
            for i, block in enumerate(raw_blocks):
                block_type = block.get("block_type")
                block_id = block.get("block_id")
                print(f"Block {i}: type={block_type}, id={block_id}")
                print(f"Block content: {block}")
                
                # 处理不同类型的文本块
                text_content = None
                text_source = ""
                
                if block_type == 1:  # 页面/标题块
                    text_content = block.get("page", {})
                    text_source = "page"
                elif block_type == 2:  # 普通文本块
                    text_content = block.get("text", {})
                    text_source = "text"
                elif block_type == 4:  # 标题块
                    text_content = block.get("heading2", {})
                    text_source = "heading2"
                elif block_type == 5:  # 其他标题块
                    text_content = block.get("heading1", {}) or block.get("heading3", {})
                    text_source = "heading1/3"
                
                if text_content:
                    print(f"Block {i} ({text_source}): {text_content}")
                    elements = text_content.get("elements", [])
                    print(f"Elements: {elements}")
                    
                    if elements:
                        text = extract_text_from_elements(elements)
                        print(f"Extracted text: '{text}'")
                        
                        if text.strip():
                            content_blocks.append(ContentBlock(
                                block_id=block_id,
                                block_type="text",
                                text=text
                            ))
                            print(f"Added text block: {text[:50]}...")
                
                elif block_type == 27:  # 图片块
                    image = block.get("image", {})
                    image_token = image.get("token")
                    if image_token:
                        content_blocks.append(ContentBlock(
                            block_id=block_id,
                            block_type="image",
                            image_token=image_token
                        ))
                        print(f"Added image block: {image_token}")
                
                else:
                    print(f"Unhandled block type: {block_type}")
            
            print(f"Total content blocks created: {len(content_blocks)}")
            
            return DocumentContent(
                doc_id=doc_id,
                title=title,
                blocks=content_blocks
            )
            
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"网络请求失败: {str(e)}")


async def get_document_content_fallback(doc_id: str, token: str, title: str):
    """
    回退方法：使用blocks API获取文档内容
    """
    try:
        async with httpx.AsyncClient() as client:
            blocks_response = await client.get(
                f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}/blocks",
                headers={"Authorization": f"Bearer {token}"},
                params={"page_size": 500}
            )
            
            blocks_data = blocks_response.json()
            
            if blocks_data.get("code") != 0:
                raise HTTPException(
                    status_code=400,
                    detail=f"获取文档内容失败: {blocks_data.get('msg')}"
                )
            
            raw_blocks = blocks_data.get("data", {}).get("items", [])
            
            # 解析内容块
            content_blocks = []
            print(f"Fallback: Total blocks found: {len(raw_blocks)}")
            
            for block in raw_blocks:
                block_type = block.get("block_type")
                block_id = block.get("block_id")
                
                if block_type == 27:  # 图片块
                    image = block.get("image", {})
                    image_token = image.get("token")
                    if image_token:
                        content_blocks.append(ContentBlock(
                            block_id=block_id,
                            block_type="image",
                            image_token=image_token
                        ))
            
            return DocumentContent(
                doc_id=doc_id,
                title=title,
                blocks=content_blocks
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"回退方法失败: {str(e)}")


@router.post("/create")
async def create_feishu_document(
    request: dict,
    authorization: str = Header(...)
):
    """
    创建新的飞书文档并写入内容
    """
    try:
        token = authorization.replace("Bearer ", "")
        title = request.get("title", "AI生成的文章")
        content = request.get("content", "")
        images = request.get("images", [])  # [{mime_type: str, data: str (base64)}]
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            # 1. 创建新文档 - 清理标题中的特殊字符
            import re
            # 移除或替换特殊字符，避免GBK编码问题
            clean_title = re.sub(r'[^\w\s\-_\.\(\)\[\]（）【】]', '', title)
            if not clean_title.strip():
                clean_title = "AI创作文档"
            
            print(f"Original title: {title}")
            print(f"Clean title: {clean_title}")
            
            create_response = await client.post(
                "https://open.feishu.cn/open-apis/docx/v1/documents",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                },
                json={
                    "title": clean_title,
                    "folder_token": ""  # 创建在根目录
                }
            )
            
            create_data = create_response.json()
            print(f"Create document response: {create_data}")
            
            if create_data.get("code") != 0:
                raise HTTPException(
                    status_code=400,
                    detail=f"创建文档失败: {create_data.get('msg')}"
                )
            
            doc_id = create_data.get("data", {}).get("document", {}).get("document_id")
            doc_url = f"https://feishu.cn/docx/{doc_id}"
            
            # 2. 上传图片到飞书（如果有）
            image_tokens = {}
            for idx, img in enumerate(images):
                try:
                    import io
                    import base64
                    import time
                    
                    # 解码base64图片
                    img_data = base64.b64decode(img['data'])
                    
                    # 上传图片 - 使用正确的multipart/form-data格式
                    files = {
                        'file': (f'image_{idx+1}.jpg', io.BytesIO(img_data), img.get('mime_type', 'image/jpeg'))
                    }
                    
                    # 注意：parent_type和parent_node必须一起传
                    upload_response = await client.post(
                        "https://open.feishu.cn/open-apis/drive/v1/medias/upload_all",
                        headers={"Authorization": f"Bearer {token}"},
                        files=files,
                        data={
                            "file_name": f'image_{idx+1}.jpg',
                            "parent_type": "docx_image",
                            "parent_node": doc_id,
                            "size": str(len(img_data))
                        }
                    )
                    
                    # 限速：避免触发频率限制
                    time.sleep(0.3)
                    
                    upload_data = upload_response.json()
                    print(f"Upload image {idx+1} response: {upload_data}")
                    
                    if upload_data.get("code") == 0:
                        file_token = upload_data.get("data", {}).get("file_token")
                        image_tokens[f"image_{idx+1}"] = file_token
                        print(f"Image {idx+1} uploaded successfully: {file_token}")
                    else:
                        print(f"Image {idx+1} upload failed: {upload_data.get('msg')}")
                        
                except Exception as e:
                    print(f"Error uploading image {idx+1}: {e}")
            
            # 3. 解析Markdown并转换为飞书blocks
            # 将 ![描述](image_N) 替换为实际的图片token
            import re
            
            # 按行处理内容
            lines = content.split('\n')
            blocks_to_create = []
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # 检查是否是图片标记
                img_match = re.match(r'!\[([^\]]*)\]\(image_(\d+)\)', line)
                if img_match:
                    img_num = img_match.group(2)
                    img_key = f"image_{img_num}"
                    
                    if img_key in image_tokens:
                        # 添加图片块
                        blocks_to_create.append({
                            "block_type": 27,  # 图片类型
                            "image": {
                                "token": image_tokens[img_key]
                            }
                        })
                    continue
                
                # 检查是否是标题(从最长的开始检查,避免误匹配)
                if line.startswith('####'):
                    # 四级标题在飞书中不存在,转为三级标题
                    blocks_to_create.append({
                        "block_type": 5,  # 三级标题
                        "heading3": {
                            "elements": [{"text_run": {"content": line[5:].strip()}}]
                        }
                    })
                elif line.startswith('###'):
                    blocks_to_create.append({
                        "block_type": 5,  # 三级标题
                        "heading3": {
                            "elements": [{"text_run": {"content": line[4:].strip()}}]
                        }
                    })
                elif line.startswith('##'):
                    blocks_to_create.append({
                        "block_type": 4,  # 二级标题
                        "heading2": {
                            "elements": [{"text_run": {"content": line[3:].strip()}}]
                        }
                    })
                elif line.startswith('#'):
                    blocks_to_create.append({
                        "block_type": 3,  # 一级标题
                        "heading1": {
                            "elements": [{"text_run": {"content": line[2:].strip()}}]
                        }
                    })
                else:
                    # 普通文本
                    blocks_to_create.append({
                        "block_type": 2,  # 文本块类型是2
                        "paragraph": {
                            "elements": [{"text_run": {"content": line}}]
                        }
                    })
            
            # 4. 分批创建blocks（飞书限制每次最多50个）
            if blocks_to_create:
                # 获取文档根block_id
                doc_info_response = await client.get(
                    f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}",
                    headers={"Authorization": f"Bearer {token}"}
                )
                
                doc_info = doc_info_response.json()
                if doc_info.get("code") == 0:
                    root_block_id = doc_info.get("data", {}).get("document", {}).get("block_id")
                    
                    # 分批创建（每批最多50个）
                    batch_size = 50
                    total_batches = (len(blocks_to_create) + batch_size - 1) // batch_size
                    
                    for batch_idx in range(total_batches):
                        start_idx = batch_idx * batch_size
                        end_idx = min(start_idx + batch_size, len(blocks_to_create))
                        batch_blocks = blocks_to_create[start_idx:end_idx]
                        
                        print(f"Creating batch {batch_idx + 1}/{total_batches}: {len(batch_blocks)} blocks")
                        
                        # 调试：打印前3个block的结构
                        if batch_blocks:
                            import json
                            for i, block in enumerate(batch_blocks[:3]):
                                print(f"Block {i+1} structure: {json.dumps(block, ensure_ascii=False, indent=2)}")
                        
                        # 测试：只发送第一个block
                        test_block = [{
                            "block_type": 2,
                            "text": {
                                "elements": [{"text_run": {"content": "测试文本"}}],
                                "style": {}
                            }
                        }]
                        
                        print(f"Testing with simple block: {json.dumps(test_block, ensure_ascii=False, indent=2)}")
                        
                        children_response = await client.post(
                            f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}/blocks/{root_block_id}/children",
                            headers={
                                "Authorization": f"Bearer {token}",
                                "Content-Type": "application/json"
                            },
                            json={
                                "children": test_block
                            }
                        )
                        
                        children_data = children_response.json()
                        print(f"Batch {batch_idx + 1} response: {children_data}")
                        
                        if children_data.get("code") != 0:
                            # 安全处理错误消息，避免GBK编码问题
                            error_msg = children_data.get('msg', 'Unknown error')
                            try:
                                print(f"Batch {batch_idx + 1} failed: {error_msg}")
                            except UnicodeEncodeError:
                                print(f"Batch {batch_idx + 1} failed: [Error message contains special characters]")
                            break
                        else:
                            print(f"Batch {batch_idx + 1} created successfully")
                        
                        # 批次间延迟，避免触发频率限制
                        if batch_idx < total_batches - 1:
                            time.sleep(0.5)
            
            return {
                "doc_id": doc_id,
                "doc_url": doc_url,
                "message": "文档创建成功"
            }
            
    except Exception as e:
        # 安全处理异常消息，避免GBK编码问题
        try:
            error_msg = str(e)
            print(f"Error creating document: {error_msg}")
            raise HTTPException(status_code=500, detail=f"创建文档失败: {error_msg}")
        except UnicodeEncodeError:
            print("Error creating document: [Error message contains special characters]")
            raise HTTPException(status_code=500, detail="创建文档失败: 文档内容包含特殊字符，请检查输入")


@router.get("/image/{doc_id}/{image_token}")
async def get_image(
    doc_id: str,
    image_token: str,
    token: str = None,
    authorization: str = Header(None)
):
    """
    获取图片数据（返回图片URL或base64）
    """
    try:
        # 优先从query parameter获取token，如果没有则从header获取
        if not token and authorization:
            token = authorization.replace("Bearer ", "")
        
        if not token:
            raise HTTPException(status_code=401, detail="缺少认证token")
        
        async with httpx.AsyncClient() as client:
            # 下载图片
            response = await client.get(
                f"https://open.feishu.cn/open-apis/drive/v1/medias/{image_token}/download",
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=400, detail="图片下载失败")
            
            # 返回图片二进制数据
            from fastapi.responses import Response
            return Response(
                content=response.content,
                media_type=response.headers.get("content-type", "image/jpeg")
            )
            
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"图片下载失败: {str(e)}")


def extract_text_from_elements(elements: List[dict]) -> str:
    """
    从飞书文档元素中提取文本
    """
    text_parts = []
    for element in elements:
        # 尝试多种可能的文本字段
        if element.get("text_run"):
            content = element["text_run"].get("content", "")
            text_parts.append(content)
        elif element.get("text"):
            content = element.get("text", "")
            text_parts.append(content)
        elif element.get("content"):
            content = element.get("content", "")
            text_parts.append(content)
        elif isinstance(element, str):
            text_parts.append(element)
    
    return "".join(text_parts)


