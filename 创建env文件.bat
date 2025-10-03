@echo off
chcp 65001 >nul
echo 正在创建 .env 文件...

cd backend_py

(
echo # 飞书应用配置
echo FEISHU_APP_ID=your_app_id_here
echo FEISHU_APP_SECRET=your_app_secret_here
echo FEISHU_REDIRECT_URI=http://localhost:3000/auth/callback
echo.
echo # Google Gemini配置
echo GEMINI_API_KEY=your_gemini_api_key_here
echo.
echo # 服务配置
echo BACKEND_URL=http://localhost:8000
echo FRONTEND_URL=http://localhost:3000
) > .env

cd ..

echo ✓ backend_py\.env 文件创建成功！

cd frontend

echo NEXT_PUBLIC_API_URL=http://localhost:8000 > .env.local

cd ..

echo ✓ frontend\.env.local 文件创建成功！
echo.
echo ======================================
echo 提示：请编辑 backend_py\.env 文件
echo 填写您的飞书和Gemini密钥
echo ======================================
pause

