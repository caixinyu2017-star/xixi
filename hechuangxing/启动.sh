#!/usr/bin/env bash
# 禾创星一键启动（macOS / Linux）
set -e
cd "$(dirname "$0")"

if [ ! -d ".venv" ]; then
  echo "首次运行，正在创建运行环境……"
  python3 -m venv .venv
  ./.venv/bin/pip install -q --upgrade pip
  ./.venv/bin/pip install -q -r requirements.txt
  echo "环境准备完成。"
fi

if [ ! -f ".env" ] && [ -f ".env.example" ]; then
  cp .env.example .env
  echo "已生成 .env，可在里面填 ANTHROPIC_API_KEY；不填也能跑（离线演示模式）。"
fi

echo "正在启动禾创星，浏览器打开 http://127.0.0.1:8848"
./.venv/bin/python server.py
