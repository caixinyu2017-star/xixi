#!/usr/bin/env python3
"""Validate Light installation and client-integration assets.

This gate protects the user-facing installation layer:
- POSIX/PowerShell installers must link 28 skills and refuse to overwrite
  non-link user directories;
- Codex routing snippet must point at per-skill install paths and cover every
  Light skill, including light-orchestrator;
- Codex installation docs must not mention stale aggregate paths;
- Claude/Codex plugin manifests must be valid JSON with expected metadata;
- CI must run this validator when install/plugin assets change.
"""
from __future__ import annotations

import io
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[2]
EXPECTED_SKILLS = 28
FORBIDDEN_SKILL_NAMES = {"light-software", "light-miniprogram", "light-novel"}
REQUIRED_FILES = [
    "install.sh",
    "install.ps1",
    "AGENTS.snippet.md",
    ".codex/INSTALL.md",
    ".claude-plugin/plugin.json",
    ".codex-plugin/plugin.json",
]
INSTALL_TRIGGER_PATHS = [
    "install.sh",
    "install.ps1",
    "AGENTS.snippet.md",
    ".codex/**",
    ".claude-plugin/**",
    ".codex-plugin/**",
]
errors: list[str] = []
warnings: list[str] = []


def read(rel: str) -> str:
    path = ROOT / rel
    if not path.exists():
        errors.append(f"missing install asset: {rel}")
        return ""
    return path.read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def run_command(args: list[str], label: str) -> None:
    try:
        result = subprocess.run(
            args,
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=30,
            check=False,
        )
    except FileNotFoundError:
        warnings.append(f"{label}: command unavailable, skipped")
        return
    except Exception as exc:  # noqa: BLE001 - CI diagnostic
        errors.append(f"{label}: failed to run: {exc}")
        return
    if result.returncode != 0:
        output = result.stdout or ""
        if label == "install.sh syntax" and sys.platform.startswith("win") and (
            "\x00" in output or "w\x00s\x00l" in output.lower() or "wsl" in output.lower()
        ):
            warnings.append(f"{label}: local Windows bash/WSL unavailable, skipped; CI Linux still checks it")
            return
        errors.append(f"{label}: exit {result.returncode}: {output.strip()}")


def run_posix_idempotency_check() -> None:
    """Run install.sh twice under a temporary HOME when bash is usable."""
    with tempfile.TemporaryDirectory(prefix="light-install-sh-") as tmp:
        env = os.environ.copy()
        env["HOME"] = tmp
        for attempt in (1, 2):
            try:
                result = subprocess.run(
                    ["bash", "install.sh", "codex"],
                    cwd=ROOT,
                    env=env,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    timeout=60,
                    check=False,
                )
            except FileNotFoundError:
                if sys.platform.startswith("win"):
                    warnings.append("install.sh idempotency: local bash unavailable, skipped; CI Linux still checks it")
                else:
                    errors.append("install.sh idempotency: bash unavailable")
                return
            output = result.stdout or ""
            if result.returncode != 0:
                if sys.platform.startswith("win") and (
                    "\x00" in output
                    or "w\x00s\x00l" in output.lower()
                    or "wsl" in output.lower()
                    or "install.sh is for macOS/Linux" in output
                ):
                    warnings.append("install.sh idempotency: Windows host should use install.ps1; CI Linux still checks install.sh")
                    return
                errors.append(f"install.sh idempotency attempt {attempt}: exit {result.returncode}: {output.strip()}")
                return
        agents_root = pathlib.Path(tmp) / ".agents"
        skills_root = agents_root / "skills"
        skill_count = len(list(skills_root.glob("light-*/SKILL.md")))
        if skill_count != EXPECTED_SKILLS:
            errors.append(f"install.sh idempotency: expected {EXPECTED_SKILLS} linked skills, found {skill_count}")
        if not sys.platform.startswith("win"):
            symlink_count = sum(1 for path in skills_root.glob("light-*") if path.is_symlink())
            if symlink_count != EXPECTED_SKILLS:
                errors.append(f"install.sh idempotency: expected {EXPECTED_SKILLS} symlinks, found {symlink_count}")
        for rel in [".agents/databases", ".agents/code_assets"]:
            if not (pathlib.Path(tmp) / rel).exists():
                errors.append(f"install.sh idempotency: missing shared resource {rel}")


def run_powershell_idempotency_check(ps_cmd: str) -> None:
    """Run install.ps1 twice under a temporary HOME/USERPROFILE when possible."""
    if not sys.platform.startswith("win"):
        warnings.append("install.ps1 idempotency: non-Windows host, textual checks only")
        return
    with tempfile.TemporaryDirectory(prefix="light-install-ps-") as tmp:
        env = os.environ.copy()
        env["HOME"] = tmp
        env["USERPROFILE"] = tmp
        probe = subprocess.run(
            [ps_cmd, "-NoProfile", "-Command", "Write-Host $HOME"],
            cwd=ROOT,
            env=env,
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=30,
            check=False,
        )
        if probe.returncode != 0 or pathlib.Path(tmp).resolve().as_posix().lower() not in (probe.stdout or "").replace("\\", "/").lower():
            warnings.append("install.ps1 idempotency: PowerShell did not honor temporary HOME, skipped")
            return
        for attempt in (1, 2):
            result = subprocess.run(
                [ps_cmd, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "install.ps1", "-Client", "codex"],
                cwd=ROOT,
                env=env,
                text=True,
                encoding="utf-8",
                errors="replace",
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=60,
                check=False,
            )
            if result.returncode != 0:
                errors.append(f"install.ps1 idempotency attempt {attempt}: exit {result.returncode}: {(result.stdout or '').strip()}")
                return
        skills_root = pathlib.Path(tmp) / ".agents" / "skills"
        skill_count = len(list(skills_root.glob("light-*/SKILL.md")))
        if skill_count != EXPECTED_SKILLS:
            errors.append(f"install.ps1 idempotency: expected {EXPECTED_SKILLS} linked skills, found {skill_count}")
        for rel in [".agents/databases", ".agents/code_assets"]:
            if not (pathlib.Path(tmp) / rel).exists():
                errors.append(f"install.ps1 idempotency: missing shared resource {rel}")


texts = {rel: read(rel) for rel in REQUIRED_FILES}
skills = sorted(path.parent.name for path in (ROOT / "skills").glob("light-*/SKILL.md"))
require(len(skills) == EXPECTED_SKILLS, f"expected {EXPECTED_SKILLS} skills, found {len(skills)}")

for rel, text in texts.items():
    for forbidden in FORBIDDEN_SKILL_NAMES:
        if forbidden in text:
            errors.append(f"{rel}: forbidden out-of-scope skill mention: {forbidden}")

# Installers: safety and count checks.
install_sh = texts["install.sh"]
require("EXPECTED_SKILLS=28" in install_sh, "install.sh: missing EXPECTED_SKILLS=28")
require("case \"$CLIENT\"" in install_sh, "install.sh: missing client validation case")
require("MINGW*|MSYS*|CYGWIN*" in install_sh, "install.sh: must reject Windows Git Bash/MSYS/Cygwin")
require("install.sh is for macOS/Linux" in install_sh, "install.sh: missing Windows-use-install.ps1 guidance")
require("safe_link_dir" in install_sh, "install.sh: missing safe_link_dir helper")
require("Refusing to overwrite non-symlink path" in install_sh, "install.sh: must refuse non-symlink targets")
require("rm -rf" not in install_sh, "install.sh: must not use rm -rf for install targets")
require("$parent/databases" in install_sh and "$parent/code_assets" in install_sh, "install.sh: missing shared sibling links")
require("safe_link_file" in install_sh, "install.sh: missing safe_link_file helper for shared docs")
for _doc in ("CONVENTIONS.md", "ROUTER.md", "ROUTER_EXAMPLES.md", "MODE_REGISTRY.md"):
    require(_doc in install_sh, f"install.sh: missing shared doc link for {_doc}")
run_command(["bash", "-n", "install.sh"], "install.sh syntax")
run_posix_idempotency_check()

install_ps1 = texts["install.ps1"]
require("$ExpectedSkills = 28" in install_ps1, "install.ps1: missing $ExpectedSkills = 28")
require("[ValidateSet('both','claude','codex')]" in install_ps1, "install.ps1: missing Client ValidateSet")
require("ReparsePoint" in install_ps1, "install.ps1: must check ReparsePoint before overwriting")
require("Refusing to overwrite non-link path" in install_ps1, "install.ps1: must refuse non-link targets")
require("cmd.exe /c rmdir" in install_ps1, "install.ps1: must remove existing junctions with cmd.exe /c rmdir")
require("New-Item -ItemType Junction" in install_ps1, "install.ps1: should create junctions")
require("$parent\\databases" in install_ps1 and "$parent\\code_assets" in install_ps1, "install.ps1: missing shared sibling links")
require("Link-File" in install_ps1, "install.ps1: missing Link-File helper for shared docs")
for _doc in ("CONVENTIONS.md", "ROUTER.md", "ROUTER_EXAMPLES.md", "MODE_REGISTRY.md"):
    require(_doc in install_ps1, f"install.ps1: missing shared doc link for {_doc}")
ps_cmd = shutil.which("pwsh") or shutil.which("powershell")
if ps_cmd:
    run_command(
        [
            ps_cmd,
            "-NoProfile",
            "-Command",
            "$tokens=$null;$errors=$null;"
            "[System.Management.Automation.Language.Parser]::ParseFile('install.ps1',[ref]$tokens,[ref]$errors) | Out-Null;"
            "if($errors.Count){$errors | ForEach-Object { Write-Host $_.Message }; exit 1};"
            "Write-Host 'install.ps1 parse ok'",
        ],
        "install.ps1 parse",
    )
else:
    warnings.append("install.ps1 parse: PowerShell unavailable, textual checks only")

if ps_cmd:
    run_powershell_idempotency_check(ps_cmd)
else:
    warnings.append("install.ps1 idempotency: PowerShell unavailable, textual checks only")

# Codex routing snippet: exact per-skill routing, no stale aggregate path.
agents = texts["AGENTS.snippet.md"]
require("~/.agents/skills/<skill-name>/SKILL.md" in agents, "AGENTS.snippet.md: missing per-skill path guidance")
require("~/.agents/skills/light/" not in agents, "AGENTS.snippet.md: stale aggregate skill path")
missing_agents = [skill for skill in skills if skill not in agents]
if missing_agents:
    errors.append(f"AGENTS.snippet.md: missing skill mentions: {', '.join(missing_agents)}")
for boundary_phrase in ["继续 / 刚断了", "light-orchestrator", "light-figure-planning", "light-figure-drawing", "light-slides"]:
    require(boundary_phrase in agents, f"AGENTS.snippet.md: missing boundary phrase {boundary_phrase!r}")

# Codex install docs: must use current repo name and installer, no stale old path.
codex_install = texts[".codex/INSTALL.md"]
require("Light-skills" in codex_install, ".codex/INSTALL.md: missing Light-skills clone path")
require("./install.sh codex" in codex_install, ".codex/INSTALL.md: missing POSIX installer command")
require("install.ps1" in codex_install and "-Client codex" in codex_install, ".codex/INSTALL.md: missing Windows installer command")
require("~/.agents/skills/light-" in codex_install, ".codex/INSTALL.md: should document per-skill links")
require("~/.agents/skills/light/" not in codex_install, ".codex/INSTALL.md: stale aggregate skill path")
require("~/.codex/Light/" not in codex_install, ".codex/INSTALL.md: stale clone path ~/.codex/Light")
require("rm -rf ~/.agents" not in codex_install, ".codex/INSTALL.md: unsafe blanket rm -rf under ~/.agents")
require("skip non-symlink path" in codex_install, ".codex/INSTALL.md: POSIX uninstall must skip non-symlink shared paths")
require("skip non-link path" in codex_install, ".codex/INSTALL.md: Windows uninstall must skip non-link shared paths")
require("LIGHT-SKILLS-START" in codex_install, ".codex/INSTALL.md: missing idempotent AGENTS block marker guidance")

# Plugin manifests: parse JSON and check essential metadata.
for rel in [".claude-plugin/plugin.json", ".codex-plugin/plugin.json"]:
    try:
        data = json.loads(texts[rel])
    except Exception as exc:  # noqa: BLE001
        errors.append(f"{rel}: invalid JSON: {exc}")
        continue
    require(data.get("name") == "light", f"{rel}: name must be light")
    require(bool(data.get("version")), f"{rel}: missing version")
    require(data.get("homepage") == "https://github.com/Light0305/Light-skills", f"{rel}: homepage mismatch")
    require(data.get("repository") == "https://github.com/Light0305/Light-skills", f"{rel}: repository mismatch")
    require(data.get("license") == "MIT", f"{rel}: license mismatch")
    keywords = data.get("keywords") or []
    require("research" in keywords and "academic" in keywords, f"{rel}: missing research/academic keywords")

# Workflow should trigger and run the install validator.
workflow = read(".github/workflows/ci.yml")
for trigger in INSTALL_TRIGGER_PATHS:
    require(trigger in workflow, f"ci.yml: install asset path not in trigger list: {trigger}")
require("python .github/scripts/check_installation_assets.py" in workflow, "ci.yml: missing Check installation assets step")

print(
    "安装资产: "
    f"skills={len(skills)}, install_docs={len(REQUIRED_FILES)}, "
    f"agent_skill_mentions={len(skills) - len(missing_agents)}, warnings={len(warnings)}"
)
if warnings:
    print("\n安装资产校验警告:")
    for warning in warnings:
        print(f"  ! {warning}")
if errors:
    print("\n安装资产校验失败:")
    for error in errors:
        print(f"  ✗ {error}")
    sys.exit(1)

print("✓ 安装脚本、Codex 路由片段与插件清单一致性通过")
