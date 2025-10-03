@echo off
echo 启动后端服务并查看日志...
cd /d "D:\Lan_Company\03-AI-MINE\01-飞书文档图文AI创作\backend_py"
echo 当前目录: %CD%
echo 检查main.py是否存在...
if exist main.py (
    echo main.py 文件存在，启动服务...
    python main.py
) else (
    echo 错误：main.py 文件不存在！
    echo 当前目录文件列表：
    dir
)
pause
