@echo off
echo 🚀 正在安装飞书文档小组件依赖...
echo.

cd /d "%~dp0"

echo 📦 安装Node.js依赖...
npm install

if %ERRORLEVEL% neq 0 (
    echo ❌ npm安装失败，尝试使用国内镜像...
    npm install --registry=https://registry.npmmirror.com
)

if %ERRORLEVEL% neq 0 (
    echo ❌ 依赖安装失败，请检查网络连接和Node.js环境
    pause
    exit /b 1
)

echo.
echo ✅ 依赖安装完成！
echo.
echo 📋 下一步操作：
echo 1. 确保后端服务已启动 (cd backend_py && python main.py)
echo 2. 启动小组件开发服务器 (npm run dev)
echo 3. 访问 http://localhost:3001 进行测试
echo.
pause