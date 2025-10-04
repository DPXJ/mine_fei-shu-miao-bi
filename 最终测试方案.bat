@echo off
chcp 65001 >nul
echo 🚀 飞书文档AI助手 - 最终测试方案
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
echo 🔍 检查前端服务 (端口3000):
netstat -ano | findstr :3000
if %ERRORLEVEL% equ 0 (
    echo ✅ 前端服务已启动
) else (
    echo ❌ 前端服务未启动，正在启动...
    start "前端服务" cmd /k "cd frontend && npm run dev"
    timeout /t 5 /nobreak >nul
)

echo.
echo 🎉 服务启动完成！
echo.
echo 📍 访问地址:
echo - 主应用: http://localhost:3000
echo - 后端API: http://localhost:8000/docs
echo.
echo 📋 测试步骤:
echo 1. 打开浏览器访问 http://localhost:3000
echo 2. 登录飞书账号
echo 3. 选择文档进行AI生成测试
echo 4. 测试多轮对话功能
echo 5. 测试创建飞书副本功能
echo.
echo 💡 注意: feishu-widget小组件由于依赖问题暂时无法启动
echo 但主应用功能完整，可以正常使用所有AI功能
echo.
pause
