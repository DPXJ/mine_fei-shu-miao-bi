@echo off
chcp 65001 >nul
echo 🚀 飞书文档AI助手小组件 - 最终测试
echo.

echo 📋 当前服务状态:
echo.

echo 🔍 检查后端服务 (端口8000):
netstat -ano | findstr :8000
if %ERRORLEVEL% equ 0 (
    echo ✅ 后端服务已启动
) else (
    echo ❌ 后端服务未启动，正在启动...
    start "后端服务" cmd /k "cd backend_py && python main.py"
    timeout /t 3 /nobreak >nul
)

echo.
echo 🌐 启动小组件测试服务器 (端口3001)...
echo 📍 访问地址: http://localhost:3001/simple.html
echo.

cd /d "%~dp0"
start "小组件测试服务器" cmd /k "python test_widget_server.py"

echo.
echo ✅ 启动完成！
echo.
echo 📍 测试地址:
echo - 小组件: http://localhost:3001/simple.html
echo - 后端API: http://localhost:8000/docs
echo.
echo 📋 测试步骤:
echo 1. 等待浏览器自动打开 http://localhost:3001/simple.html
echo 2. 查看小组件界面
echo 3. 输入AI指令测试生成功能
echo 4. 检查是否与后端API正常通信
echo.
echo 💡 提示: 这是一个简化版的小组件测试页面
echo 包含了所有核心功能，可以验证AI生成是否正常工作
echo.
pause
