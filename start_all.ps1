# 飞书妙笔 - PowerShell启动脚本
Write-Host "================================" -ForegroundColor Cyan
Write-Host "  飞书妙笔 - 启动脚本" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# 检查环境配置
Write-Host "[1/3] 检查环境配置..." -ForegroundColor Yellow
if (-not (Test-Path "backend_py\.env")) {
    Write-Host "[警告] 后端环境配置文件不存在！" -ForegroundColor Red
    Write-Host "请复制 backend_py\.env.example 为 backend_py\.env 并填写配置" -ForegroundColor Red
    Read-Host "按回车键退出"
    exit 1
}

if (-not (Test-Path "frontend\.env.local")) {
    Write-Host "[提示] 前端环境配置文件不存在，使用默认配置" -ForegroundColor Yellow
    "NEXT_PUBLIC_API_URL=http://localhost:8000" | Out-File -FilePath "frontend\.env.local" -Encoding UTF8
}

# 启动后端
Write-Host "[2/3] 启动后端服务..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend_py; python main.py" -WindowStyle Normal

Start-Sleep -Seconds 3

# 启动前端
Write-Host "[3/3] 启动前端服务..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev" -WindowStyle Normal

Write-Host ""
Write-Host "================================" -ForegroundColor Green
Write-Host "  启动完成！" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""
Write-Host "前端地址: http://localhost:3000" -ForegroundColor Cyan
Write-Host "后端地址: http://localhost:8000" -ForegroundColor Cyan
Write-Host ""
Write-Host "按任意键关闭此窗口..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")


