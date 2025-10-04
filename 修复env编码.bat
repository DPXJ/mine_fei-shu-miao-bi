@echo off
chcp 65001 >nul
echo ========================================
echo 修复.env文件编码问题
echo ========================================

echo.
echo 删除旧的.env文件...
if exist "backend_py\.env" del "backend_py\.env"

echo.
echo 创建新的.env文件（UTF-8编码）...
echo # Feishu API Configuration > "backend_py\.env"
echo FEISHU_APP_ID=cli_a855c1780938900b >> "backend_py\.env"
echo FEISHU_APP_SECRET=DXAXNDNvdviTiPgt64f3rbqF6pPCiVEv >> "backend_py\.env"
echo FEISHU_REDIRECT_URI=http://localhost:3000/auth/callback >> "backend_py\.env"
echo. >> "backend_py\.env"
echo # Google Gemini API Configuration >> "backend_py\.env"
echo GEMINI_API_KEY=AIzaSyBKO6KCRL_elzgXliklCYe8HkKvvyos9Kc >> "backend_py\.env"
echo. >> "backend_py\.env"
echo # Server Configuration >> "backend_py\.env"
echo BACKEND_URL=http://localhost:8000 >> "backend_py\.env"
echo FRONTEND_URL=http://localhost:3000 >> "backend_py\.env"

echo.
echo 验证.env文件内容...
type "backend_py\.env"

echo.
echo .env文件创建完成！
echo.
pause
