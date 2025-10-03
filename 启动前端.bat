@echo off
chcp 65001 >nul
echo ================================
echo   飞书妙笔 - 仅启动前端
echo ================================
echo.

if not exist "frontend\.env.local" (
    echo [提示] 环境配置文件不存在，使用默认配置
    echo NEXT_PUBLIC_API_URL=http://localhost:8000 > frontend\.env.local
)

cd frontend
echo [信息] 启动前端服务...
npm run dev


