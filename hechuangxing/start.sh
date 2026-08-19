#!/usr/bin/env bash
# 禾创星启动脚本（macOS / Linux）
cd "$(dirname "$0")"

if command -v python3 >/dev/null 2>&1; then
  exec python3 start.py
elif command -v python >/dev/null 2>&1; then
  exec python start.py
else
  echo "没有找到 python3，请先安装 Python 3.10 或更高版本后重试。"
  exit 1
fi
