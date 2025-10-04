@echo off
chcp 65001 >nul
echo 🚀 Starting Feishu Widget...
echo.

echo 📍 Changing to feishu-widget directory...
cd /d "%~dp0feishu-widget"

echo.
echo 📦 Installing dependencies if needed...
if not exist "node_modules" (
    echo Installing dependencies...
    npm install
)

echo.
echo 🌐 Starting webpack dev server...
echo 📍 Access URL: http://localhost:3001
echo 💡 Press Ctrl+C to stop server
echo.

npm run dev

pause
