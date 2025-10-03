"""
飞书OAuth认证路由
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
import httpx
import os

router = APIRouter()


class AuthUrlResponse(BaseModel):
    auth_url: str


class TokenRequest(BaseModel):
    code: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    expires_in: int
    user_info: dict


@router.get("/url", response_model=AuthUrlResponse)
async def get_auth_url():
    """
    获取飞书OAuth授权URL
    """
    app_id = os.getenv("FEISHU_APP_ID")
    redirect_uri = os.getenv("FEISHU_REDIRECT_URI")
    
    if not app_id or not redirect_uri:
        raise HTTPException(status_code=500, detail="飞书应用配置缺失")
    
    # 飞书OAuth授权URL
    auth_url = (
        f"https://open.feishu.cn/open-apis/authen/v1/authorize?"
        f"app_id={app_id}&"
        f"redirect_uri={redirect_uri}&"
        f"response_type=code&"
        f"state=STATE"
    )
    
    return AuthUrlResponse(auth_url=auth_url)


@router.post("/token", response_model=TokenResponse)
async def exchange_token(request: TokenRequest):
    """
    使用授权码换取access_token
    """
    app_id = os.getenv("FEISHU_APP_ID")
    app_secret = os.getenv("FEISHU_APP_SECRET")
    
    if not app_id or not app_secret:
        raise HTTPException(status_code=500, detail="飞书应用配置缺失")
    
    try:
        # 1. 获取app_access_token
        async with httpx.AsyncClient() as client:
            app_token_response = await client.post(
                "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal",
                json={
                    "app_id": app_id,
                    "app_secret": app_secret
                }
            )
            app_token_data = app_token_response.json()
            
            if app_token_data.get("code") != 0:
                raise HTTPException(
                    status_code=400,
                    detail=f"获取app_access_token失败: {app_token_data.get('msg')}"
                )
            
            app_access_token = app_token_data.get("app_access_token")
            
            # 2. 使用code换取user_access_token
            token_response = await client.post(
                "https://open.feishu.cn/open-apis/authen/v1/oidc/access_token",
                headers={
                    "Authorization": f"Bearer {app_access_token}",
                    "Content-Type": "application/json"
                },
                json={
                    "grant_type": "authorization_code",
                    "code": request.code
                }
            )
            
            token_data = token_response.json()
            
            if token_data.get("code") != 0:
                raise HTTPException(
                    status_code=400,
                    detail=f"获取access_token失败: {token_data.get('msg')}"
                )
            
            data = token_data.get("data", {})
            
            # 3. 获取用户信息
            user_response = await client.get(
                "https://open.feishu.cn/open-apis/authen/v1/user_info",
                headers={"Authorization": f"Bearer {data.get('access_token')}"}
            )
            
            user_data = user_response.json()
            
            return TokenResponse(
                access_token=data.get("access_token"),
                refresh_token=data.get("refresh_token"),
                expires_in=data.get("expires_in", 7200),
                user_info=user_data.get("data", {})
            )
            
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"网络请求失败: {str(e)}")


@router.post("/refresh")
async def refresh_token(refresh_token: str):
    """
    刷新access_token
    """
    app_id = os.getenv("FEISHU_APP_ID")
    app_secret = os.getenv("FEISHU_APP_SECRET")
    
    try:
        async with httpx.AsyncClient() as client:
            # 获取app_access_token
            app_token_response = await client.post(
                "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal",
                json={
                    "app_id": app_id,
                    "app_secret": app_secret
                }
            )
            app_token_data = app_token_response.json()
            app_access_token = app_token_data.get("app_access_token")
            
            # 刷新token
            response = await client.post(
                "https://open.feishu.cn/open-apis/authen/v1/oidc/refresh_access_token",
                headers={"Authorization": f"Bearer {app_access_token}"},
                json={
                    "grant_type": "refresh_token",
                    "refresh_token": refresh_token
                }
            )
            
            return response.json()
            
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"刷新token失败: {str(e)}")


