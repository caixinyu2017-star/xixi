#!/usr/bin/env python3
"""校验每个技能的 SKILL.md frontmatter:必须有 name 与 description。
常驻技能(标了 user-invocable: false)单独统计。
另含体量警戒 gate(R8.5):SKILL.md 行数与 description 字符数防膨胀。CI 用。"""
import io
import pathlib
import sys

# 强制 UTF-8 输出,避免 Windows GBK 控制台编不了 ✓/✗
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[2]
SKILLS = ROOT / "skills"

# --- R8.5 体量警戒阈值（带依据，纯防膨胀；2026-06-12 实测最重 120 行/最长 ~626 字符，红线远未触及）---
# 硬上限：超过即报错（CI 红）。依据：单个 SKILL.md 是常驻上下文，过长会挤占 agent 工作记忆；
# 500 行约等于一次性灌入 ~6k token 的常驻成本，超此应把细节下沉 references/。
MAX_SKILL_LINES = 500
MAX_DESC_CHARS = 1024
# 软警戒：超过仅 WARN 提示，不红，提醒考虑下沉。
WARN_SKILL_LINES = 300

errors = []
warnings = []
manual = resident = 0
expected_manual = 17
expected_resident = 11
forbidden_skill_dirs = {"light-miniprogram", "light-software", "light-novel"}


def description_chars(fm: str) -> int:
    """提取 frontmatter 里 description: 的字符数（单行值，去掉前缀与首尾空白）。"""
    for line in fm.splitlines():
        stripped = line.strip()
        if stripped.startswith("description:"):
            return len(stripped[len("description:"):].strip())
    return 0


for skill_dir in sorted(SKILLS.glob("light-*")):
    if skill_dir.name in forbidden_skill_dirs:
        errors.append(f"{skill_dir.name}: 不属于 Light 科研技能包范围,不得放在 skills/ 下")
        continue
    md = skill_dir / "SKILL.md"
    if not md.exists():
        errors.append(f"{skill_dir.name}: 缺 SKILL.md")
        continue
    text = md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        errors.append(f"{skill_dir.name}: 缺 frontmatter")
        continue
    fm = text.split("---", 2)[1]
    has_name = any(l.strip().startswith("name:") for l in fm.splitlines())
    has_desc = any(l.strip().startswith("description:") for l in fm.splitlines())
    if not has_name:
        errors.append(f"{skill_dir.name}: frontmatter 缺 name")
    if not has_desc:
        errors.append(f"{skill_dir.name}: frontmatter 缺 description")
    if any("user-invocable: false" in l for l in fm.splitlines()):
        resident += 1
    else:
        manual += 1

    # R8.5 体量警戒
    n_lines = text.count("\n") + (0 if text.endswith("\n") else 1)
    if n_lines > MAX_SKILL_LINES:
        errors.append(f"{skill_dir.name}: SKILL.md {n_lines} 行 > 上限 {MAX_SKILL_LINES}，须下沉 references/")
    elif n_lines > WARN_SKILL_LINES:
        warnings.append(f"{skill_dir.name}: SKILL.md {n_lines} 行 > 软警戒 {WARN_SKILL_LINES}，建议下沉细节")
    n_desc = description_chars(fm)
    if n_desc > MAX_DESC_CHARS:
        errors.append(f"{skill_dir.name}: description {n_desc} 字符 > 上限 {MAX_DESC_CHARS}")

print(f"技能总数: {manual + resident}  (手动 {manual} / 常驻 {resident})")
if (manual, resident) != (expected_manual, expected_resident):
    errors.append(
        f"技能数量与 README 约定不一致: 实测 手动 {manual}/常驻 {resident}, "
        f"期望 手动 {expected_manual}/常驻 {expected_resident}"
    )
if warnings:
    print("\n体量软警戒（仅提示，不影响 CI）:")
    for w in warnings:
        print(f"  ! {w}")
if errors:
    print("\n校验失败:")
    for e in errors:
        print(f"  ✗ {e}")
    sys.exit(1)
print(f"✓ 所有技能 frontmatter 合规（体量上限 {MAX_SKILL_LINES} 行/{MAX_DESC_CHARS} 字符，均未触及）")
