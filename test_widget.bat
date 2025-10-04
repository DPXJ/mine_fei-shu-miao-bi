@echo off
chcp 65001 >nul
echo 🚀 Starting Feishu Widget Test...
echo.

echo 📋 Checking services status:
echo.

echo 🔍 Backend service (port 8000):
netstat -ano | findstr :8000
if %ERRORLEVEL% equ 0 (
    echo ✅ Backend service is running
) else (
    echo ❌ Backend service not running, starting...
    start "Backend Service" cmd /k "cd backend_py && python main.py"
    timeout /t 3 /nobreak >nul
)

echo.
echo 🌐 Starting widget frontend (port 3001):
echo 📍 Access URL: http://localhost:3001
echo.

start "Widget Frontend" cmd /k "cd feishu-widget && npm run dev"

echo.
echo ✅ Services started!
echo.
echo 📋 Test steps:
echo 1. Wait for browser to open http://localhost:3001
echo 2. Check "AI Document Assistant" interface
echo 3. Test AI generation with instruction input
echo 4. Test multi-turn conversation optimization
echo.
echo Press any key to continue...
pause >nul
