@echo off
echo 正在创建正确的.env文件...

cd /d "D:\Lan_Company\03-AI-MINE\01-飞书文档图文AI创作\backend_py"

echo # Feishu Configuration > .env
echo FEISHU_APP_ID=cli_a855c1780938900b >> .env
echo FEISHU_APP_SECRET=DXAXNDNvdviTiPgt64f3rbqF6pPCiVEv >> .env
echo FEISHU_REDIRECT_URI=http://localhost:3000/auth/callback >> .env
echo. >> .env
echo # Gemini Configuration >> .env
echo GEMINI_API_KEY=AIzaSyBKO6KCRL_elzgXliklCYe8HkKvvyos9Kc >> .env
echo. >> .env
echo # Server Configuration >> .env
echo BACKEND_URL=http://localhost:8000 >> .env
echo FRONTEND_URL=http://localhost:3000 >> .env

echo .env文件创建完成！
pause
