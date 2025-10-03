"""
飞书妙笔 - 后端主入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from routers import auth, documents, ai

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
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)


