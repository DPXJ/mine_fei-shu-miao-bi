@echo off
chcp 65001 > nul
echo 启动后端服务...
cd /d "%~dp0backend_py"
python main.py
pause
