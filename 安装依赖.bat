@echo off
echo ========================================
echo 飞书妙笔 - 安装依赖
echo ========================================

echo 安装后端依赖...
cd /d backend_py
pip install -r requirements.txt

echo 安装前端依赖...
cd /d ..
cd /d frontend
npm install

echo ========================================
echo 依赖安装完成！
echo ========================================
pause