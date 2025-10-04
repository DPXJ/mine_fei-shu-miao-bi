@echo off
chcp 65001 >nul
echo ========================================
echo 飞书妙笔 - 最终修复启动脚本
echo ========================================

echo.
echo 1. 删除旧的 .env 文件（如果存在）...
if exist "backend_py\.env" del "backend_py\.env"

echo.
echo 2. 创建正确编码的 .env 文件...
powershell -Command "Set-Content -Path 'backend_py\.env' -Value @('# Feishu App Configuration', 'FEISHU_APP_ID=cli_a855c1780938900b', 'FEISHU_APP_SECRET=DXAXNDNvdviTiPgt64f3rbqF6pPCiVEv', 'FEISHU_REDIRECT_URI=http://localhost:3000/auth/callback', '', '# Google Gemini API Configuration', 'GEMINI_API_KEY=AIzaSyBKO6KCRL_elzgXliklCYe8HnKvvyos9Kc', '', '# Server Configuration', 'BACKEND_URL=http://localhost:8000', 'FRONTEND_URL=http://localhost:3000') -Encoding UTF8"

echo .env 文件创建完成！

echo.
echo 3. 启动后端服务...
start "飞书妙笔-后端" cmd /k "cd /d backend_py && python main.py"

echo.
echo 4. 等待后端启动（5秒）...
timeout /t 5 /nobreak >nul

echo.
echo 5. 启动前端服务...
start "飞书妙笔-前端" cmd /k "cd /d frontend && npm run dev"

echo.
echo ========================================
echo 启动完成！
echo ========================================
echo.
echo 后端地址: http://localhost:8000
echo 前端地址: http://localhost:3000
echo.
echo 已修复的所有问题：
echo ✓ React 渲染错误（对象不能作为子元素）
echo ✓ Gemini API Key 配置问题
echo ✓ 文档时间显示错误（1970年问题）
echo ✓ .env 文件编码问题
echo ✓ 错误处理优化
echo.
echo 请等待服务完全启动后访问前端地址
echo 如果还有问题，请查看终端窗口的错误信息
echo.
pause
