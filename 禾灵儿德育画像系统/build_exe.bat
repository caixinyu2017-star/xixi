@echo off
chcp 65001 >nul
REM ===================================================================
REM  禾灵儿文化德育数字画像 —— Windows 一键打包脚本
REM  用法：安装 Python 3.10~3.12 后，双击本文件即可
REM  产物：dist\禾灵儿德育画像.exe
REM ===================================================================
setlocal
cd /d "%~dp0"

echo.
echo [1/3] 检查 Python ...
python --version >nul 2>&1
if errorlevel 1 (
    echo     × 未检测到 Python。请先到 https://www.python.org/downloads/ 安装
    echo       Python 3.10 至 3.12，安装时务必勾选 "Add Python to PATH"。
    pause
    exit /b 1
)
python --version

echo.
echo [2/3] 安装依赖（首次运行约需 2-5 分钟）...
python -m pip install --upgrade pip -q
python -m pip install -r requirements.txt -q
if errorlevel 1 (
    echo     × 依赖安装失败，请检查网络后重试。
    pause
    exit /b 1
)

echo.
echo [3/3] 开始打包 ...
python -m PyInstaller hlr_desktop.spec --noconfirm --clean
if errorlevel 1 (
    echo     × 打包失败。
    pause
    exit /b 1
)

echo.
echo ===================================================================
echo   打包完成！
echo   可执行文件： %cd%\dist\禾灵儿德育画像.exe
echo   直接双击即可运行，数据会保存在 exe 同目录的 hlr_data 文件夹。
echo ===================================================================
pause
