@echo off
chcp 65001 >nul
echo 🚀 启动飞书小组件...
echo.

echo 📍 切换到feishu-widget目录...
cd /d "%~dp0feishu-widget"

echo.
echo 🌐 启动webpack开发服务器...
echo 📍 访问地址: http://localhost:3001
echo 💡 提示: 按 Ctrl+C 停止服务器
echo.

npm run dev

pause