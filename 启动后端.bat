@echo off
chcp 65001 >nul
echo ================================
echo   飞书妙笔 - 仅启动后端
echo ================================
echo.

if not exist "backend_py\.env" (
    echo [警告] 环境配置文件不存在！
    echo 请复制 backend_py\.env.example 为 backend_py\.env 并填写配置
    pause
    exit /b 1
)

cd backend_py
echo [信息] 启动后端服务...
python main.py


