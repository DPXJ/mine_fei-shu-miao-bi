@echo off
chcp 65001 >nul
echo ================================
echo   飞书妙笔 - 安装依赖
echo ================================
echo.

echo [1/2] 安装后端依赖...
cd backend_py
if not exist "venv" (
    echo 创建Python虚拟环境...
    python -m venv venv
)
call venv\Scripts\activate
pip install -r requirements.txt
cd ..

echo.
echo [2/2] 安装前端依赖...
cd frontend
call npm install
cd ..

echo.
echo ================================
echo   依赖安装完成！
echo ================================
echo.
pause


