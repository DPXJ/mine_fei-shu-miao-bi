@echo off
chcp 65001 >nul
echo 🚀 启动飞书文档AI助手前端...
echo.

echo 📍 切换到frontend目录...
cd /d "%~dp0frontend"

echo.
echo 🌐 启动Next.js开发服务器...
echo 📍 访问地址: http://localhost:3000
echo 💡 提示: 按 Ctrl+C 停止服务器
echo.

npm run dev

pause
