@echo off
chcp 65001 >nul
echo 🚀 飞书文档AI助手 - 一键启动
echo.

echo 📋 启动步骤:
echo 1. 启动后端服务
echo 2. 启动前端服务
echo.

echo 🔧 步骤1: 启动后端服务...
start "后端服务" cmd /k "cd /d %~dp0backend_py && python main.py"

echo 等待后端服务启动...
timeout /t 5 /nobreak >nul

echo.
echo 🌐 步骤2: 启动前端服务...
start "前端服务" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ✅ 启动完成！
echo.
echo 📍 访问地址:
echo - 主应用: http://localhost:3000
echo - 后端API: http://localhost:8000/docs
echo.
echo 📋 使用说明:
echo 1. 等待浏览器自动打开 http://localhost:3000
echo 2. 如果浏览器没有自动打开，请手动访问上述地址
echo 3. 登录飞书账号开始使用AI功能
echo.
echo 💡 提示: 关闭此窗口不会停止服务
echo 要停止服务，请关闭对应的命令行窗口
echo.
pause
