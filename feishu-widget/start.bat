@echo off
echo 🚀 启动飞书文档小组件开发服务器...
echo.

cd /d "%~dp0"

echo 🔍 检查依赖是否已安装...
if not exist "node_modules" (
    echo ❌ 依赖未安装，正在安装...
    call install.bat
    if %ERRORLEVEL% neq 0 (
        echo ❌ 依赖安装失败，请先运行 install.bat
        pause
        exit /b 1
    )
)

echo.
echo 🌐 启动开发服务器...
echo 📍 访问地址: http://localhost:3001
echo 💡 提示: 按 Ctrl+C 停止服务器
echo.

npm run dev

pause