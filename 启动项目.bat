@echo off
chcp 65001 >nul
echo ================================
echo   飞书妙笔 - 启动脚本
echo ================================
echo.

echo [1/3] 检查环境配置...
if not exist "backend_py\.env" (
    echo [警告] 后端环境配置文件不存在！
    echo 请复制 backend_py\.env.example 为 backend_py\.env 并填写配置
    pause
    exit /b 1
)

if not exist "frontend\.env.local" (
    echo [提示] 前端环境配置文件不存在，使用默认配置
    echo NEXT_PUBLIC_API_URL=http://localhost:8000 > frontend\.env.local
)

echo [2/3] 启动后端服务...
start "飞书妙笔-后端" cmd /k "cd backend_py && python main.py"
timeout /t 3 /nobreak >nul

echo [3/3] 启动前端服务...
start "飞书妙笔-前端" cmd /k "cd frontend && npm run dev"

echo.
echo ================================
echo   启动完成！
echo ================================
echo.
echo 前端地址: http://localhost:3000
echo 后端地址: http://localhost:8000
echo.
echo 按任意键关闭此窗口...
pause >nul


