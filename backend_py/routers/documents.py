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
    page_token: Optional[str] = None
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
                "order_by": "EditedTime"
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
                    documents.append(Document(
                        doc_id=file.get("token"),
                        title=file.get("name", "未命名文档"),
                        doc_type=file.get("type"),
                        updated_at=file.get("modified_time", ""),
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
            
            # 获取文档所有块
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
            for block in raw_blocks:
                block_type = block.get("block_type")
                block_id = block.get("block_id")
                
                if block_type == 1:  # 文本块
                    text_content = block.get("text", {})
                    if text_content:
                        text = extract_text_from_elements(text_content.get("elements", []))
                        if text.strip():
                            content_blocks.append(ContentBlock(
                                block_id=block_id,
                                block_type="text",
                                text=text
                            ))
                
                elif block_type == 27:  # 图片块
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
            
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"网络请求失败: {str(e)}")


@router.get("/image/{doc_id}/{image_token}")
async def get_image(
    doc_id: str,
    image_token: str,
    authorization: str = Header(...)
):
    """
    获取图片数据（返回图片URL或base64）
    """
    try:
        token = authorization.replace("Bearer ", "")
        
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
        if element.get("text_run"):
            content = element["text_run"].get("content", "")
            text_parts.append(content)
    return "".join(text_parts)


