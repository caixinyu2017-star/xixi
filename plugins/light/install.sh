#!/usr/bin/env bash
# Light installer (macOS / Linux)
# Links Light's 28 skills + shared knowledge bases into Claude Code and/or Codex.
# Usage:  ./install.sh            # installs into both clients
#         ./install.sh claude
#         ./install.sh codex
set -euo pipefail

EXPECTED_SKILLS=28
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLIENT="${1:-both}"

usage() {
  echo "Usage: $0 [both|claude|codex]" >&2
}

case "$(uname -s 2>/dev/null || true)" in
  MINGW*|MSYS*|CYGWIN*)
    echo "install.sh is for macOS/Linux. On Windows, run: powershell -ExecutionPolicy Bypass -File install.ps1 -Client ${CLIENT}" >&2
    exit 2
    ;;
esac

case "$CLIENT" in
  both|claude|codex) ;;
  *) usage; exit 2 ;;
esac

safe_link_dir() {
  local link="$1"
  local target="$2"
  if [ -L "$link" ]; then
    rm "$link"
  elif [ -e "$link" ]; then
    echo "Refusing to overwrite non-symlink path: $link" >&2
    echo "Remove it manually if it is an old Light install target." >&2
    return 1
  fi
  ln -s "$target" "$link"
}

safe_link_file() {
  local link="$1"
  local target="$2"
  if [ -L "$link" ]; then
    rm "$link"
  elif [ -e "$link" ]; then
    echo "Refusing to overwrite non-symlink path: $link" >&2
    echo "Remove it manually if it is an old Light install target." >&2
    return 1
  fi
  ln -s "$target" "$link"
}

install_into() {
  local skills_dir="$1"
  local parent
  parent="$(dirname "$skills_dir")"
  mkdir -p "$skills_dir"

  local skill_dirs=("$REPO"/skills/light-*/)
  if [ ! -d "${skill_dirs[0]}" ]; then
    echo "No skills/light-* directories found under $REPO" >&2
    return 1
  fi

  local n=0
  local d name target
  for d in "${skill_dirs[@]}"; do
    target="${d%/}"
    name="$(basename "$target")"
    safe_link_dir "$skills_dir/$name" "$target"
    [ -f "$skills_dir/$name/SKILL.md" ] && n=$((n+1))
  done

  if [ "$n" -ne "$EXPECTED_SKILLS" ]; then
    echo "Expected $EXPECTED_SKILLS skills, linked $n" >&2
    return 1
  fi

  # Shared libraries as siblings so skills' relative paths resolve.
  safe_link_dir "$parent/databases" "$REPO/databases"
  safe_link_dir "$parent/code_assets" "$REPO/code_assets"
  # Shared top-level docs as siblings so skills' "见 CONVENTIONS §5" / 路由文档引用装后仍可达。
  local doc
  for doc in CONVENTIONS.md ROUTER.md ROUTER_EXAMPLES.md MODE_REGISTRY.md; do
    safe_link_file "$parent/$doc" "$REPO/$doc"
  done
  echo "  $skills_dir  ->  $n/$EXPECTED_SKILLS skills"
}

if [ "$CLIENT" = both ] || [ "$CLIENT" = claude ]; then
  echo 'Claude Code:'
  install_into "$HOME/.claude/skills"
fi
if [ "$CLIENT" = both ] || [ "$CLIENT" = codex ]; then
  echo 'Codex:'
  install_into "$HOME/.agents/skills"
fi
echo 'Done. Restart your client to discover the skills.'
