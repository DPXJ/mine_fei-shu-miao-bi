@echo off
echo 🚀 启动飞书文档小组件测试...
echo.

echo 📋 检查服务状态:
echo.

echo 🔍 检查后端服务 (端口8000):
netstat -ano | findstr :8000
if %ERRORLEVEL% equ 0 (
    echo ✅ 后端服务已启动
) else (
    echo ❌ 后端服务未启动，正在启动...
    start "后端服务" cmd /c "cd backend_py && python main.py"
    timeout /t 3 /nobreak >nul
)

echo.
echo 🌐 启动小组件前端 (端口3001):
echo 📍 访问地址: http://localhost:3001
echo.

start "小组件前端" cmd /c "cd feishu-widget && npm run dev"

echo.
echo ✅ 服务启动完成！
echo.
echo 📋 测试步骤:
echo 1. 等待浏览器自动打开 http://localhost:3001
echo 2. 查看"AI文档助手"界面
echo 3. 输入AI指令测试生成功能
echo 4. 测试多轮对话优化功能
echo.
pause
