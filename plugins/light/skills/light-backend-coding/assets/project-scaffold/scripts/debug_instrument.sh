#!/usr/bin/env bash
# 多组件边界证据采集模板（systematic-debugging Phase 1.4）。
# 用途：在 CI->build->sign 或 API->service->db 这类多层系统里，
# 先跑一次把"数据在哪一层断"打出来，再聚焦那一层，而非在最外层反复盲改。
# 用法：复制改成你系统的真实层，每层只回答两件事：进来什么 / 出去什么。
set -euo pipefail

sep() { printf '=== %s ===\n' "$1"; }

# --- Layer 1: 入口/工作流：关键变量是否存在（不回显敏感值，只报 SET/UNSET）---
sep "Layer 1 entry: env/secrets presence"
printf 'API_TOKEN: %s\n' "${API_TOKEN:+SET}${API_TOKEN:-UNSET}"
printf 'DB_URL:    %s\n' "${DB_URL:+SET}${DB_URL:-UNSET}"

# --- Layer 2: 配置/环境是否传播到了子进程 ---
sep "Layer 2 config propagation"
env | grep -E '^(APP_|MODEL_|DATA_)' || echo "no APP_/MODEL_/DATA_ vars in environment"

# --- Layer 3: 依赖/版本一致性（本机 vs CI 不一致是高频根因）---
sep "Layer 3 runtime versions"
python --version 2>&1 || true
python - <<'PY' 2>&1 || true
import sys
print("python:", sys.version.split()[0])
for m in ("numpy", "pandas", "torch", "sklearn"):
    try:
        mod = __import__(m); print(f"{m}: {getattr(mod,'__version__','?')}")
    except ImportError:
        print(f"{m}: NOT INSTALLED")
PY

# --- Layer 4: 数据/产物落点（路径分隔符、是否真生成）---
sep "Layer 4 artifacts"
ls -la ./outputs 2>/dev/null || echo "outputs/ missing"

sep "DONE — 看哪一层第一次出现 UNSET / 缺失 / 版本不符，根因就在该层与上一层之间"
