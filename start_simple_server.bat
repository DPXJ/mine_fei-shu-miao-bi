@echo off
echo 🚀 启动简单的HTTP服务器...

cd feishu-widget\public

echo 📍 当前目录: %CD%
echo 🌐 服务地址: http://localhost:3001
echo 📄 测试页面: http://localhost:3001/test.html
echo 📄 原页面: http://localhost:3001/simple.html
echo 💡 按 Ctrl+C 停止服务器
echo.

python -m http.server 3001
