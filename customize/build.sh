#!/usr/bin/env bash
# 把技能目录打包成可上传到 claude.ai → Customize → Skills 的 zip。
#
# 用法：bash customize/build.sh
# 产物：customize/dist/<skill>.zip，每个 zip 的根目录是 <skill>/，内含 SKILL.md。
#
# 打包出来的技能必须自包含：不依赖同插件下的兄弟技能、不依赖仓库里的其他路径。

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST="${REPO_ROOT}/customize/dist"

# 要打包的技能：<zip 名>=<相对仓库根的技能目录>
SKILLS=(
  "gpt-image-2=plugins/gpt-image-2/skills/gpt-image-2"
  "nature-skills=plugins/nature-skills/skills/nature-skills"
)

command -v zip >/dev/null 2>&1 || { echo "需要 zip 命令，请先安装（apt-get install -y zip）" >&2; exit 1; }

rm -rf "${DIST}"
mkdir -p "${DIST}"

for entry in "${SKILLS[@]}"; do
  name="${entry%%=*}"
  src="${REPO_ROOT}/${entry#*=}"

  if [[ ! -f "${src}/SKILL.md" ]]; then
    echo "✗ ${name}: ${src}/SKILL.md 不存在" >&2
    exit 1
  fi

  staging="$(mktemp -d)"
  # -L 解引用软链，保证 zip 里是真实文件而不是断链
  cp -RL "${src}" "${staging}/${name}"
  find "${staging}/${name}" \
    \( -name '__pycache__' -o -name '*.pyc' -o -name '.DS_Store' \) \
    -exec rm -rf {} + 2>/dev/null || true

  ( cd "${staging}" && zip -qr "${DIST}/${name}.zip" "${name}" )
  rm -rf "${staging}"

  size="$(du -h "${DIST}/${name}.zip" | cut -f1)"
  files="$(unzip -Z1 "${DIST}/${name}.zip" | grep -cv '/$' || true)"
  echo "✓ ${name}.zip  (${size}, ${files} 个文件)"
done

echo
echo "产物在 ${DIST}/"
echo "上传：claude.ai → 左下角头像 → Customize → Skills → Upload skill → 选 zip"
