@echo off
echo 正在创建正确的 .env 文件...

echo # 飞书应用配置 > backend_py\.env
echo FEISHU_APP_ID=cli_a855c1780938900b >> backend_py\.env
echo FEISHU_APP_SECRET=DXAXNDNvdviTiPgt64f3rbqF6pPCiVEv >> backend_py\.env
echo FEISHU_REDIRECT_URI=http://localhost:3000/auth/callback >> backend_py\.env
echo. >> backend_py\.env
echo # Google Gemini API配置 >> backend_py\.env
echo GEMINI_API_KEY=AIzaSyBKO6KCRL_elzgXliklCYe8HnKvvyos9Kc >> backend_py\.env
echo. >> backend_py\.env
echo # 服务器配置 >> backend_py\.env
echo BACKEND_URL=http://localhost:8000 >> backend_py\.env
echo FRONTEND_URL=http://localhost:3000 >> backend_py\.env

echo .env 文件创建完成！
echo 位置: backend_py\.env
pause
