# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller 打包配置：生成单文件 exe。

在 Windows 上执行：pyinstaller hlr_desktop.spec --noconfirm
产物：dist/禾灵儿德育画像.exe
"""
block_cipher = None

a = Analysis(
    ['desktop_app.py'],
    pathex=['.'],
    binaries=[],
    # 词典与映射文件随包携带；教师改这三个 json 即可调参而无需重新打包
    datas=[('hlr_portrait.py', '.')],
    hiddenimports=[
        'hlr_portrait',
        'uvicorn.logging', 'uvicorn.loops', 'uvicorn.loops.auto',
        'uvicorn.protocols', 'uvicorn.protocols.http',
        'uvicorn.protocols.http.auto', 'uvicorn.protocols.websockets',
        'uvicorn.protocols.websockets.auto', 'uvicorn.lifespan',
        'uvicorn.lifespan.on', 'uvicorn.lifespan.off',
        'multipart', 'multipart.multipart',
        'openpyxl', 'docx', 'pptx',
        'email.mime.multipart', 'email.mime.text',
    ],
    hookspath=[],
    runtime_hooks=[],
    # 桌面版只监听 127.0.0.1、不启用 TLS，排除 cryptography 可显著减小体积；
    # 其余为常见的大体积无关包。
    excludes=['matplotlib', 'numpy', 'scipy', 'pandas', 'PIL', 'tkinter',
              'PySide6', 'PyQt5', 'notebook', 'IPython',
              'cryptography', 'OpenSSL', 'pypdf'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz, a.scripts, a.binaries, a.zipfiles, a.datas, [],
    name='禾灵儿德育画像',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,          # 保留控制台窗口用于显示服务地址与错误信息
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
