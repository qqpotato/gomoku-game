@echo off
chcp 65001 >nul
echo ========================================
echo   五子棋游戏 - Windows 打包脚本
echo ========================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装 Python 3.8+
    echo 下载地址：https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/4] 检查 Python 环境...
python --version

REM 创建虚拟环境
echo.
echo [2/4] 创建虚拟环境...
if exist "venv" (
    echo 删除旧的虚拟环境...
    rmdir /s /q venv
)
python -m venv venv

REM 激活虚拟环境并安装依赖
echo.
echo [3/4] 安装依赖 (pygame + pyinstaller)...
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install pygame pyinstaller

REM 使用 PyInstaller 打包
echo.
echo [4/4] 打包成 exe...
pyinstaller --onefile ^
    --windowed ^
    --name "五子棋游戏" ^
    --icon=NONE ^
    --add-data "gomoku.py;." ^
    gomoku.py

echo.
echo ========================================
echo   打包完成！
echo ========================================
echo.
echo 可执行文件位置：dist\五子棋游戏.exe
echo.

REM 测试运行
if exist "dist\五子棋游戏.exe" (
    echo 文件大小：
    dir "dist\五子棋游戏.exe" | find "exe"
    echo.
    echo 你可以直接运行 dist\五子棋游戏.exe 测试
    echo 或者将整个 dist 文件夹分发给其他用户
) else (
    echo [警告] exe 文件生成失败，请检查错误信息
)

echo.
pause
