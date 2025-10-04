@echo off
echo ========================================
echo 飞书妙笔 - 项目启动脚本
echo ========================================

echo 正在启动后端服务...
start "后端服务" cmd /k "cd /d backend_py && python main.py"

echo 等待3秒让后端启动...
timeout /t 3 /nobreak > nul

echo 正在启动前端服务...
start "前端服务" cmd /k "cd /d frontend && npm run dev"

echo ========================================
echo 启动完成！
echo 后端服务: http://localhost:8000
echo 前端服务: http://localhost:3000
echo ========================================
echo 按任意键退出...
pause > nul