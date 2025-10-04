@echo off
echo ========================================
echo 飞书妙笔 - 完整修复启动脚本
echo ========================================

echo.
echo 1. 确保 .env 文件配置正确...
if not exist "backend_py\.env" (
    echo 创建 .env 文件...
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
) else (
    echo .env 文件已存在，检查配置...
    findstr "GEMINI_API_KEY=AIzaSyBKO6KCRL_elzgXliklCYe8HnKvvyos9Kc" backend_py\.env >nul
    if errorlevel 1 (
        echo 更新 Gemini API Key...
        powershell -Command "(Get-Content backend_py\.env) -replace 'GEMINI_API_KEY=.*', 'GEMINI_API_KEY=AIzaSyBKO6KCRL_elzgXliklCYe8HnKvvyos9Kc' | Set-Content backend_py\.env"
    )
    echo 配置检查完成！
)

echo.
echo 2. 启动后端服务...
start "飞书妙笔-后端" cmd /k "cd backend_py && python main.py"

echo.
echo 3. 等待后端启动（5秒）...
timeout /t 5 /nobreak >nul

echo.
echo 4. 启动前端服务...
start "飞书妙笔-前端" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo 启动完成！
echo ========================================
echo.
echo 后端地址: http://localhost:8000
echo 前端地址: http://localhost:3000
echo.
echo 已修复的问题：
echo ✓ React 渲染错误
echo ✓ Gemini API Key 配置
echo ✓ 文档时间显示
echo ✓ 错误处理优化
echo.
echo 请等待服务完全启动后访问前端地址
echo 如果还有问题，请查看终端窗口的错误信息
echo.
pause
