@echo off
chcp 65001 >nul
cd /d "%~dp0"
title 禾创星 - 嘉兴本地化创业智能体

echo ============================================================
echo   禾创星 · 嘉兴本地化创业智能体
echo ============================================================
echo.

REM ---- 先确认电脑上装了 Python ----
python --version >nul 2>&1
if errorlevel 1 (
  echo [没找到 Python]
  echo.
  echo 请先安装 Python 3.10 或更高版本：
  echo   1. 打开 https://www.python.org/downloads/
  echo   2. 下载安装包并运行
  echo   3. 安装第一屏务必勾选 Add python.exe to PATH
  echo   4. 装完后重新双击本文件
  echo.
  pause
  exit /b 1
)

REM ---- 首次运行：创建环境并安装依赖 ----
if not exist ".venv" (
  echo 首次运行，正在创建运行环境，大约需要 1 到 2 分钟。
  echo 这个窗口会停一会儿，属于正常现象，请不要关闭。
  echo.
  python -m venv .venv
  .venv\Scripts\python -m pip install -q --upgrade pip
  .venv\Scripts\pip install -q -r requirements.txt
  if errorlevel 1 (
    echo.
    echo [依赖安装失败] 请检查网络后重试。
    pause
    exit /b 1
  )
  echo 环境准备完成。
  echo.
)

REM ---- 首次运行：生成配置文件 ----
if not exist ".env" (
  if exist ".env.example" (
    copy /y ".env.example" ".env" >nul
    echo 已生成 .env 配置文件。填上 ANTHROPIC_API_KEY 即为实时模式；
    echo 不填也能跑，会自动进入离线演示模式。
    echo.
  )
)

echo 正在启动服务，稍后会自动打开浏览器。
echo 地址：http://127.0.0.1:8848
echo.
echo 演示期间请保持这个黑色窗口开着，关掉它服务就停了。
echo 结束时按 Ctrl+C 或直接关闭本窗口。
echo ============================================================
echo.

REM ---- 等服务起来再开浏览器，避免打开空白页 ----
start "" cmd /c "timeout /t 6 >nul && start "" http://127.0.0.1:8848"

.venv\Scripts\python server.py
pause
