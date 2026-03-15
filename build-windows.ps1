# 五子棋游戏 - Windows 打包脚本 (PowerShell)
# 在 Windows 上运行此脚本

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  五子棋游戏 - Windows 打包脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[1/4] Python 环境：$pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[错误] 未检测到 Python，请先安装 Python 3.8+" -ForegroundColor Red
    Write-Host "下载地址：https://www.python.org/downloads/" -ForegroundColor Yellow
    pause
    exit 1
}

# 创建虚拟环境
Write-Host ""
Write-Host "[2/4] 创建虚拟环境..." -ForegroundColor Cyan
if (Test-Path "venv") {
    Write-Host "删除旧的虚拟环境..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force "venv"
}
python -m venv venv

# 安装依赖
Write-Host ""
Write-Host "[3/4] 安装依赖..." -ForegroundColor Cyan
& ".\venv\Scripts\Activate.ps1"
pip install --upgrade pip | Out-Null
pip install pygame pyinstaller

# 打包
Write-Host ""
Write-Host "[4/4] 打包成 exe..." -ForegroundColor Cyan
pyinstaller --onefile `
    --windowed `
    --name "五子棋游戏" `
    --icon=NONE `
    --add-data "gomoku.py;." `
    gomoku.py

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  打包完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "可执行文件位置：dist\五子棋游戏.exe" -ForegroundColor White
Write-Host ""

if (Test-Path "dist\五子棋游戏.exe") {
    $fileSize = (Get-Item "dist\五子棋游戏.exe").Length / 1MB
    Write-Host "文件大小：$([math]::Round($fileSize, 2)) MB" -ForegroundColor White
    Write-Host ""
    Write-Host "现在可以运行 dist\五子棋游戏.exe 测试游戏！" -ForegroundColor Green
}

Write-Host ""
pause
