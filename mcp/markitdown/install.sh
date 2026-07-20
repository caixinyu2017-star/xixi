#!/usr/bin/env bash
# MarkItDown MCP Server installer for Claude Code
# 为 Claude Code 安装 MarkItDown MCP 服务器
#
# What it does / 功能:
#   1. pip install markitdown-mcp (+ ensure the cffi backend is present)
#   2. merge the "markitdown" server into ~/.claude/.mcp.json
#   3. enable it in ~/.claude/settings.json (enabledMcpjsonServers)
#   4. verify the server boots over STDIO
#
# Usage / 用法:
#   bash install.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="${HOME}/.claude"
MCP_JSON="${CLAUDE_DIR}/.mcp.json"
SETTINGS_JSON="${CLAUDE_DIR}/settings.json"

echo "=== MarkItDown MCP Installer ==="
echo "Target: ${CLAUDE_DIR}"
echo

# Pick a pip / python that exist.
PIP_BIN="$(command -v pip3 || command -v pip || true)"
PY_BIN="$(command -v python3 || command -v python || true)"
if [ -z "${PY_BIN}" ]; then
    echo "ERROR: python3 not found on PATH." >&2
    exit 1
fi

# 1. Install the package.
echo "[1/4] Installing markitdown-mcp..."
if [ -n "${PIP_BIN}" ]; then
    "${PIP_BIN}" install --quiet --upgrade markitdown-mcp || {
        echo "  WARNING: pip install failed. Install manually: pip install markitdown-mcp" >&2
    }
else
    echo "  WARNING: no pip found. Install manually: pip install markitdown-mcp" >&2
fi

# markitdown -> pdfminer.six -> cryptography needs cffi's compiled _cffi_backend.
# Some base images ship cryptography without cffi, which crashes the server on
# startup with "No module named '_cffi_backend'". Repair it defensively.
if ! "${PY_BIN}" -c "import _cffi_backend" >/dev/null 2>&1; then
    echo "  Repairing missing cffi backend (_cffi_backend)..."
    [ -n "${PIP_BIN}" ] && "${PIP_BIN}" install --quiet cffi || true
fi

# 2. Merge the server into .mcp.json.
echo "[2/4] Configuring .mcp.json..."
mkdir -p "${CLAUDE_DIR}"
if [ -f "${MCP_JSON}" ]; then
    if grep -q '"markitdown"' "${MCP_JSON}" 2>/dev/null; then
        echo "  markitdown already in .mcp.json, skipping merge."
    else
        "${PY_BIN}" -c "
import json
with open('${MCP_JSON}', 'r') as f:
    cfg = json.load(f)
cfg.setdefault('mcpServers', {})['markitdown'] = {
    'command': 'markitdown-mcp',
    'args': [],
}
with open('${MCP_JSON}', 'w') as f:
    json.dump(cfg, f, indent=2)
    f.write('\n')
print('  Merged markitdown into existing .mcp.json')
"
    fi
else
    cp "${SCRIPT_DIR}/mcp-snippet.json" "${MCP_JSON}"
    echo "  Created new .mcp.json"
fi

# 3. Enable in settings.json.
echo "[3/4] Enabling in settings.json..."
if [ -f "${SETTINGS_JSON}" ]; then
    "${PY_BIN}" -c "
import json
with open('${SETTINGS_JSON}', 'r') as f:
    cfg = json.load(f)
enabled = cfg.setdefault('enabledMcpjsonServers', [])
if 'markitdown' not in enabled:
    enabled.append('markitdown')
    with open('${SETTINGS_JSON}', 'w') as f:
        json.dump(cfg, f, indent=2)
        f.write('\n')
    print('  Added markitdown to enabledMcpjsonServers')
else:
    print('  markitdown already enabled')
"
else
    echo '  NOTE: settings.json not found. Manually add "markitdown" to enabledMcpjsonServers.'
fi

# 4. Verify the CLI is installed and boots.
echo "[4/4] Verifying..."
if command -v markitdown-mcp >/dev/null 2>&1 && markitdown-mcp --help >/dev/null 2>&1; then
    echo "  markitdown-mcp CLI OK."
else
    echo "  WARNING: markitdown-mcp did not run cleanly. See README troubleshooting." >&2
fi

echo
echo "=== Done ==="
echo "Next steps:"
echo "  1. Restart Claude Code (or /clear)."
echo "  2. Ask Claude to convert a document, e.g. 'convert file:///path/to/paper.pdf to markdown'."
