@echo off
echo 正在修复项目问题并启动...

echo.
echo 1. 创建 .env 文件...
echo # 飞书应用配置 > .env
echo FEISHU_APP_ID=cli_a855c1780938900b >> .env
echo FEISHU_APP_SECRET=DXAXNDNvdviTiPgt64f3rbqF6pPCiVEv >> .env
echo FEISHU_REDIRECT_URI=http://localhost:3000/auth/callback >> .env
echo. >> .env
echo # Google Gemini API配置 >> .env
echo GEMINI_API_KEY=AIzaSyBKO6KCRL_elzgXliklCYe8HnKvvyos9Kc >> .env
echo. >> .env
echo # 服务器配置 >> .env
echo BACKEND_URL=http://localhost:8000 >> .env
echo FRONTEND_URL=http://localhost:3000 >> .env

echo .env 文件创建完成！

echo.
echo 2. 启动后端服务...
start "后端服务" cmd /k "cd backend_py && python main.py"

echo.
echo 3. 等待后端启动...
timeout /t 3 /nobreak >nul

echo.
echo 4. 启动前端服务...
start "前端服务" cmd /k "cd frontend && npm run dev"

echo.
echo 项目启动完成！
echo 后端地址: http://localhost:8000
echo 前端地址: http://localhost:3000
echo.
echo 请等待服务完全启动后访问前端地址
pause
