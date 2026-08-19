#!/usr/bin/env bash
# 禾创星一键启动（macOS / Linux）
set -e
cd "$(dirname "$0")"

echo "============================================================"
echo "  禾创星 · 嘉兴本地化创业智能体"
echo "============================================================"

if ! command -v python3 >/dev/null 2>&1; then
  echo "[没找到 python3] 请先安装 Python 3.10 或更高版本后重试。"
  exit 1
fi

if [ ! -d ".venv" ]; then
  echo "首次运行，正在创建运行环境，大约需要 1 到 2 分钟，请不要关闭窗口。"
  python3 -m venv .venv
  ./.venv/bin/pip install -q --upgrade pip
  ./.venv/bin/pip install -q -r requirements.txt
  echo "环境准备完成。"
fi

if [ ! -f ".env" ] && [ -f ".env.example" ]; then
  cp .env.example .env
  echo "已生成 .env 配置文件。填上 ANTHROPIC_API_KEY 即为实时模式；不填也能跑（离线演示模式）。"
fi

echo "正在启动服务，稍后会自动打开浏览器。地址：http://127.0.0.1:8848"
echo "演示期间请保持这个终端窗口开着，关掉服务就停了。"
echo "============================================================"

# 等服务起来再开浏览器，避免打开空白页
( sleep 6
  if command -v open >/dev/null 2>&1; then open http://127.0.0.1:8848
  elif command -v xdg-open >/dev/null 2>&1; then xdg-open http://127.0.0.1:8848
  fi ) &

./.venv/bin/python server.py
