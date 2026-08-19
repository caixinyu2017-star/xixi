# -*- coding: utf-8 -*-
"""禾创星启动器（跨平台）。

Windows 的 cmd 在批处理文件里遇到中文会乱码（chcp 65001 的老毛病），
所以 .bat 只保留纯英文，真正的安装与启动逻辑放在这里，
由 Python 打印中文提示，不会乱码。

用法：
    python start.py
"""
import os
import socket
import subprocess
import sys
import threading
import time
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VENV = ROOT / ".venv"
LINE = "=" * 60

# 国内访问 PyPI 常常很慢，装不上就自动换清华镜像重试
MIRRORS = [
    (None, "官方源"),
    ("https://pypi.tuna.tsinghua.edu.cn/simple", "清华镜像"),
    ("https://mirrors.aliyun.com/pypi/simple", "阿里云镜像"),
]


def venv_python() -> Path:
    if os.name == "nt":
        return VENV / "Scripts" / "python.exe"
    return VENV / "bin" / "python"


def check_python_version():
    if sys.version_info < (3, 10):
        print("你当前的 Python 版本是 %d.%d，禾创星需要 3.10 或更高版本。"
              % sys.version_info[:2])
        print("请到 https://www.python.org/downloads/ 下载新版本，")
        print("安装第一屏记得勾选 Add python.exe to PATH。")
        return False
    return True


def create_venv() -> bool:
    if venv_python().exists():
        return True
    print("首次运行，正在创建运行环境……")
    result = subprocess.run([sys.executable, "-m", "venv", str(VENV)])
    if result.returncode != 0 or not venv_python().exists():
        print()
        print("[创建运行环境失败]")
        print("如果你的 Python 是从 Microsoft Store 装的，建议卸载后")
        print("到 https://www.python.org/downloads/ 重新下载安装，")
        print("安装时勾选 Add python.exe to PATH。")
        return False
    return True


def install_requirements() -> bool:
    marker = VENV / ".deps-ok"
    req = ROOT / "requirements.txt"
    if marker.exists() and marker.stat().st_mtime >= req.stat().st_mtime:
        return True

    py = str(venv_python())
    subprocess.run([py, "-m", "pip", "install", "-q", "--upgrade", "pip",
                    "--disable-pip-version-check"])

    for index_url, label in MIRRORS:
        print("正在安装依赖（%s），大约需要 1 到 2 分钟，请不要关闭窗口……" % label)
        cmd = [py, "-m", "pip", "install", "-q", "-r", str(req),
               "--disable-pip-version-check"]
        if index_url:
            cmd += ["--index-url", index_url,
                    "--trusted-host", index_url.split("/")[2]]
        if subprocess.run(cmd).returncode == 0:
            marker.write_text("ok", encoding="utf-8")
            print("依赖安装完成。")
            return True
        print("这个源没装成功，换一个再试……")
        print()

    print()
    print("[依赖安装失败] 三个源都没成功，请检查网络后重新运行。")
    return False


def ensure_env_file():
    env, sample = ROOT / ".env", ROOT / ".env.example"
    if not env.exists() and sample.exists():
        env.write_text(sample.read_text(encoding="utf-8"), encoding="utf-8")
        print("已生成 .env 配置文件。填上 ANTHROPIC_API_KEY 即为实时模式；")
        print("不填也能跑，会自动进入离线演示模式。")
        print()


def read_port() -> int:
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if line.startswith("HCX_PORT="):
                try:
                    return int(line.split("=", 1)[1].strip())
                except ValueError:
                    pass
    return 8848


def port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.4)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def pick_free_port(preferred: int) -> int:
    """端口被别的程序占了就自动往后找一个能用的，不让演示卡在报错上。"""
    if not port_in_use(preferred):
        return preferred
    for port in range(preferred + 1, preferred + 21):
        if not port_in_use(port):
            print("端口 %d 已被其他程序占用，自动改用 %d。" % (preferred, port))
            print()
            return port
    print("端口 %d 到 %d 都被占用了，请关掉占用端口的程序，"
          "或在 .env 里改 HCX_PORT 后重试。" % (preferred, preferred + 20))
    return preferred


def open_browser_when_ready(port: int):
    """等端口真正起来再开浏览器，避免打开一个连不上的空白页。"""
    url = "http://127.0.0.1:%d" % port
    deadline = time.time() + 90
    while time.time() < deadline:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.5)
            if sock.connect_ex(("127.0.0.1", port)) == 0:
                time.sleep(0.6)
                webbrowser.open(url)
                return
        time.sleep(0.5)


def main() -> int:
    print(LINE)
    print("  禾创星 · 嘉兴本地化创业智能体")
    print(LINE)
    print()

    if not check_python_version():
        return 1
    if not create_venv():
        return 1
    if not install_requirements():
        return 1
    ensure_env_file()

    port = pick_free_port(read_port())
    print("正在启动服务，稍后会自动打开浏览器。")
    print("地址：http://127.0.0.1:%d" % port)
    print()
    print("演示期间请保持这个窗口开着，关掉它服务就停了。")
    print("结束时按 Ctrl+C 或直接关闭本窗口。")
    print(LINE)
    print()

    threading.Thread(target=open_browser_when_ready, args=(port,),
                     daemon=True).start()
    env = os.environ.copy()
    env["HCX_PORT"] = str(port)
    try:
        return subprocess.call([str(venv_python()), str(ROOT / "server.py")],
                               env=env)
    except KeyboardInterrupt:
        print()
        print("禾创星已停止。")
        return 0


if __name__ == "__main__":
    sys.exit(main())
