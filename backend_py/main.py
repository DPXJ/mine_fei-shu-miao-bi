"""
飞书妙笔 - 后端主入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from routers import auth, documents, ai

# 直接设置环境变量，避免.env文件编码问题
os.environ["FEISHU_APP_ID"] = "cli_a855c1780938900b"
os.environ["FEISHU_APP_SECRET"] = "DXAXNDNvdviTiPgt64f3rbqF6pPCiVEv"
os.environ["FEISHU_REDIRECT_URI"] = "http://localhost:3000/auth/callback"
os.environ["GEMINI_API_KEY"] = "AIzaSyBKO6KCRL_elzgXliklCYe8HkKvvyos9Kc"
os.environ["DEEPSEEK_API_KEY"] = "sk-7a5f88d8af69468590b756add1514b57"

# AI提供商选择：
# - "deepseek": 仅文本理解，国内直接可用
# - "gemini": 支持图片理解和智能排版，需要VPN
# - "qwen": 支持图片理解和智能排版，国内直接可用 ⭐推荐

# 千问VL配置 - 支持图片理解和智能排版
os.environ["QWEN_API_KEY"] = "sk-8dea6d7ed4864155a0fa33433c5c58a4"
os.environ["AI_PROVIDER"] = "qwen"  # ← 使用千问VL（支持图片理解）

# 如果要切换回DeepSeek（仅文本），注释掉上面两行，取消注释下面这行：
# os.environ["AI_PROVIDER"] = "deepseek"

os.environ["BACKEND_URL"] = "http://localhost:8000"
os.environ["FRONTEND_URL"] = "http://localhost:3000"

# 加载环境变量
load_dotenv()

app = FastAPI(
    title="飞书妙笔 API",
    description="智能内容创作辅助应用后端服务",
    version="1.1.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(documents.router, prefix="/api/documents", tags=["文档"])
app.include_router(ai.router, prefix="/api/ai", tags=["AI创作"])


@app.get("/")
async def root():
    """健康检查"""
    return {
        "status": "ok",
        "message": "飞书妙笔 API 正在运行",
        "version": "1.1.0"
    }


@app.get("/health")
async def health():
    """健康检查端点"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=port, 
        reload=True,
        log_level="info",
        access_log=True,
        use_colors=True
    )


