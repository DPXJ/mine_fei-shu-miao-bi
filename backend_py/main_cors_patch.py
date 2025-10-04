"""
后端CORS配置补丁
将此代码添加到 backend_py/main.py 中
"""

from fastapi.middleware.cors import CORSMiddleware

# 在 app = FastAPI() 之后添加:

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # 现有的前端
        "http://localhost:3001",  # 新的小组件前端
        "*"  # 开发环境允许所有来源
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("✅ CORS已配置: 允许 localhost:3000, localhost:3001 访问")

