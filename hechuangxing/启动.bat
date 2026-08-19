@echo off
chcp 65001 >nul
cd /d "%~dp0"
title 禾创星 - 嘉兴本地化创业智能体

if not exist ".venv" (
  echo 首次运行，正在创建运行环境……
  python -m venv .venv
  .venv\Scripts\python -m pip install -q --upgrade pip
  .venv\Scripts\pip install -q -r requirements.txt
  echo 环境准备完成。
)

if not exist ".env" (
  if exist ".env.example" (
    copy /y ".env.example" ".env" >nul
    echo 已生成 .env，可在里面填 ANTHROPIC_API_KEY；不填也能跑（离线演示模式）。
  )
)

echo 正在启动禾创星，浏览器打开 http://127.0.0.1:8848
start "" http://127.0.0.1:8848
.venv\Scripts\python server.py
pause
