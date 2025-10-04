@echo off
chcp 65001 >nul
echo 🚀 Feishu Document AI Assistant - Start App
echo.

echo 📋 Starting services:
echo 1. Backend service
echo 2. Frontend service
echo.

echo 🔧 Step 1: Starting backend service...
start "Backend Service" cmd /k "cd /d %~dp0backend_py && python main.py"

echo Waiting for backend to start...
timeout /t 5 /nobreak >nul

echo.
echo 🌐 Step 2: Starting frontend service...
start "Frontend Service" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ✅ Services started!
echo.
echo 📍 Access URLs:
echo - Main App: http://localhost:3000
echo - Backend API: http://localhost:8000/docs
echo.
echo 📋 Usage Instructions:
echo 1. Wait for browser to open http://localhost:3000
echo 2. If browser doesn't open automatically, visit the URL manually
echo 3. Login with Feishu account to start using AI features
echo.
echo 💡 Tip: Closing this window won't stop services
echo To stop services, close the corresponding command windows
echo.
pause
