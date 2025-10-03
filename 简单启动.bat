@echo off
chcp 65001 >nul
echo ================================
echo   飞书妙笔 - 简单启动
echo ================================
echo.

echo [1/2] 启动后端服务...
start "后端服务" cmd /k "cd /d %~dp0backend_py && python main.py"

echo 等待3秒...
timeout /t 3 /nobreak >nul

echo [2/2] 启动前端服务...
start "前端服务" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo ================================
echo   启动完成！
echo ================================
echo.
echo 前端地址: http://localhost:3000
echo 后端地址: http://localhost:8000
echo.
echo 请等待30-60秒让服务完全启动
echo 然后打开浏览器访问: http://localhost:3000
echo.
pause

