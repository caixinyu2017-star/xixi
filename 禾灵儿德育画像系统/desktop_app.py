#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
禾灵儿文化德育数字画像 —— 桌面版启动器
===============================================================================

双击 exe 后本程序会：
    1. 在本机 127.0.0.1 上挑一个空闲端口，启动内置的画像服务；
    2. 优先以原生窗口打开界面（需 pywebview），否则退回默认浏览器；
    3. 关闭窗口 / 按 Ctrl+C 即退出，数据保存在 exe 同目录的 hlr_data 文件夹。

整个界面与算法与网站版完全一致（同一份 hlr_portrait.py），
因此本地评出来的分数与部署到网站后评出来的分数逐位相同。
"""
from __future__ import annotations

import os
import socket
import sys
import threading
import time
import webbrowser

# PyInstaller 打包后，工作目录可能不是 exe 所在目录，这里统一校正，
# 保证 hlr_data 数据库始终落在 exe 旁边。
if getattr(sys, "frozen", False):
    os.chdir(os.path.dirname(sys.executable))
    sys.path.insert(0, os.path.dirname(sys.executable))
else:
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import hlr_portrait as H   # noqa: E402


def free_port(preferred: int = 8777) -> int:
    for port in (preferred, 8778, 8779, 8800, 8801):
        with socket.socket() as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue
    with socket.socket() as s:                 # 交给系统随机分配
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def wait_ready(url: str, timeout: float = 25.0) -> bool:
    import urllib.request
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=1.5) as r:
                if r.status == 200:
                    return True
        except Exception:
            time.sleep(0.35)
    return False


def main() -> int:
    port = free_port()
    url = f"http://127.0.0.1:{port}/"

    def serve() -> None:
        import uvicorn
        uvicorn.run(H.app, host="127.0.0.1", port=port, log_level="warning")

    threading.Thread(target=serve, daemon=True).start()

    print("=" * 66)
    print(f"  {H.APP_NAME}  v{H.APP_VERSION}")
    print(f"  服务地址：{url}")
    print(f"  数据文件：{H.STORE.db_path}")
    print("  关闭本窗口即退出程序。")
    print("=" * 66)

    if not wait_ready(url + "api/health"):
        print("服务启动失败，请检查依赖是否完整。")
        input("按回车键退出 ...")
        return 1

    try:                                        # 优先原生窗口
        import webview
        window = webview.create_window(
            f"{H.APP_NAME} v{H.APP_VERSION}", url, width=1360, height=900)
        webview.start()
        return 0
    except Exception:
        pass

    webbrowser.open(url)                        # 退回系统浏览器
    print("已在浏览器中打开。若未自动打开，请手动访问上面的地址。")
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        print("\n已退出。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
