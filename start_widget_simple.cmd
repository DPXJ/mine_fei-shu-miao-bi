@echo off
chcp 65001 >nul
echo 🚀 飞书文档AI助手小组件测试
echo.

echo 📋 检查服务状态:
echo.

echo 🔍 后端服务 (端口8000):
netstat -ano | findstr :8000
if %ERRORLEVEL% equ 0 (
    echo ✅ 后端服务已启动
) else (
    echo ❌ 后端服务未启动，正在启动...
    start "后端服务" cmd /k "cd backend_py && python main.py"
    timeout /t 3 /nobreak >nul
)

echo.
echo 🌐 小组件服务器 (端口3001):
netstat -ano | findstr :3001
if %ERRORLEVEL% equ 0 (
    echo ✅ 小组件服务器已启动
) else (
    echo ❌ 小组件服务器未启动，正在启动...
    start "小组件服务器" cmd /k "python test_widget_server.py"
    timeout /t 3 /nobreak >nul
)

echo.
echo ✅ 所有服务已准备就绪！
echo.
echo 📍 访问地址:
echo - 小组件: http://localhost:3001/simple.html
echo - 后端API: http://localhost:8000/docs
echo.
echo 📋 测试步骤:
echo 1. 打开浏览器访问 http://localhost:3001/simple.html
echo 2. 查看小组件界面
echo 3. 输入AI指令测试生成功能
echo 4. 检查是否与后端API正常通信
echo.
echo 💡 提示: 如果浏览器没有自动打开，请手动访问上述地址
echo.
pause
