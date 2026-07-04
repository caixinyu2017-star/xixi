@echo off
rem ============================================================
rem  Claude Science - Windows 一键安装脚本
rem  用法：双击本文件，按窗口里的提示操作即可。
rem
rem  脚本会自动完成：
rem    1) 安装 WSL2（Windows 的 Linux 子系统，需重启一次）
rem    2) 安装 Ubuntu 24.04
rem    3) 在 Ubuntu 中安装 Claude Science
rem    4) 在桌面生成 ClaudeScience.bat 启动器
rem
rem  注意：本文件必须保持 UTF-8 编码与 CRLF 换行，请勿转换。
rem  注意：wsl.exe 失败时常返回 -1，因此错误检查一律用
rem        if %errorlevel% neq 0 而不是 if errorlevel 1 。
rem ============================================================
setlocal
chcp 65001 >nul
set "WSL_UTF8=1"
set "DISTRO=Ubuntu-24.04"
title Claude Science 一键安装

rem ---------- 请求管理员权限 ----------
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo 安装需要管理员权限，即将弹出确认窗口，请点击“是”。
    powershell -NoProfile -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b 0
)

echo.
echo ==================================================
echo    Claude Science 一键安装（共 4 步，可重复运行）
echo ==================================================
echo.

rem ---------- 第 1 步：WSL ----------
echo [第 1 步] 检查 WSL ...
where wsl.exe >nul 2>&1
if %errorlevel% neq 0 goto need_wsl
wsl.exe --status >nul 2>&1
if %errorlevel% neq 0 goto need_wsl
echo           WSL 已就绪，尝试更新到最新版（更新失败也不影响）...
wsl.exe --update >nul 2>&1
wsl.exe --set-default-version 2 >nul 2>&1
goto check_distro

:need_wsl
echo           正在安装 WSL，需要下载系统组件，请耐心等待...
wsl.exe --install -d %DISTRO% --web-download
if %errorlevel% neq 0 wsl.exe --install -d %DISTRO%
if %errorlevel% neq 0 (
    echo.
    echo [出错] WSL 安装失败。常见原因：
    echo    1. Windows 版本太旧 —— 请先通过系统更新升级 Windows，
    echo       需要 Windows 10 2004 以上或 Windows 11；
    echo    2. 电脑未开启虚拟化 —— 需要在 BIOS 中开启虚拟化功能。
    echo 可将本窗口截图发给协助你的人求助。
    pause
    exit /b 1
)
echo.
echo ==================================================
echo  [重要] WSL 已装好，现在需要重启电脑。
echo         重启后请【再次双击本文件】完成剩余安装。
echo ==================================================
choice /c YN /m "现在立即重启电脑吗？重启前请先保存其他工作。Y=立即重启 N=稍后自己重启"
if errorlevel 2 exit /b 0
echo 电脑将在 5 秒后重启...
shutdown /r /t 5
exit /b 0

rem ---------- 第 2 步：Ubuntu 24.04 ----------
:check_distro
echo [第 2 步] 检查 Ubuntu 24.04 ...
wsl.exe -d %DISTRO% -u root -- true >nul 2>&1
if %errorlevel% equ 0 goto have_distro
echo           正在安装 Ubuntu 24.04，需要下载数百 MB，请耐心等待...
echo.
echo --------------------------------------------------
echo  注意：接下来会要求创建 Linux 用户，请照做：
echo   1. 出现 Enter new UNIX username 时，输入一个
echo      英文小写的名字，例如 kexue ，然后按回车；
echo   2. 出现 New password 时输入一个密码并按回车，
echo      输入密码时屏幕上不显示内容，这是正常的，
echo      之后会要求再输入一遍确认；
echo   3. 请记住这个用户名和密码。
echo   4. 如果创建完用户后停在了 Ubuntu 的绿色命令行里，
echo      输入 exit 并回车即可回到本安装程序。
echo --------------------------------------------------
echo.
pause
wsl.exe --install -d %DISTRO% --web-download
if %errorlevel% neq 0 wsl.exe --install -d %DISTRO%
set /a WAITED=0
:wait_distro
wsl.exe -d %DISTRO% -u root -- true >nul 2>&1
if %errorlevel% equ 0 goto have_distro
set /a WAITED+=10
if %WAITED% geq 1800 (
    echo [出错] 等待 Ubuntu 安装超时，请重新双击本文件再试一次。
    pause
    exit /b 1
)
echo           等待 Ubuntu 初始化...（若弹出了新窗口，请先去那个窗口里创建用户）
timeout /t 10 /nobreak >nul
goto wait_distro

:have_distro
echo           Ubuntu 已就绪。
wsl.exe --set-version %DISTRO% 2 >nul 2>&1

rem ---------- 第 3 步：安装 Claude Science ----------
echo [第 3 步] 在 Ubuntu 中安装 Claude Science ，需要几分钟，取决于网速...
wsl.exe -d %DISTRO% -u root -- bash -lc "apt-get update -y && DEBIAN_FRONTEND=noninteractive apt-get install -y curl ca-certificates bubblewrap procps"
if %errorlevel% neq 0 (
    echo [出错] Ubuntu 软件源更新失败，请检查网络后重新双击本文件。
    pause
    exit /b 1
)
wsl.exe -d %DISTRO% -- bash -lc "curl -fsSL https://claude.ai/install-claude-science.sh | bash"
if %errorlevel% neq 0 (
    echo [出错] Claude Science 下载安装失败。
    echo        请确认当前网络能够访问 claude.ai ，然后重新双击本文件。
    pause
    exit /b 1
)
wsl.exe -d %DISTRO% -- bash -lc "test -x $HOME/.local/bin/claude-science"
if %errorlevel% neq 0 (
    echo [出错] 未找到安装后的 claude-science 程序，请将本窗口截图求助。
    pause
    exit /b 1
)
echo           Claude Science 安装成功。

rem ---------- 第 4 步：生成桌面启动器 ----------
echo [第 4 步] 在桌面生成启动器 ClaudeScience.bat ...
set "LAUNCHER="
for /f "usebackq delims=" %%L in (`powershell -NoProfile -Command "$d=[Environment]::GetFolderPath('Desktop'); $p=Join-Path $d 'ClaudeScience.bat'; $src=[IO.File]::ReadAllLines('%~f0',[Text.Encoding]::UTF8); $out=New-Object System.Collections.Generic.List[string]; foreach($l in $src){ if($l.StartsWith(':::')){ $out.Add($l.Substring(3)) } }; [IO.File]::WriteAllLines($p,$out,(New-Object Text.UTF8Encoding($false))); Write-Output $p"`) do set "LAUNCHER=%%L"
if not defined LAUNCHER (
    echo [出错] 生成桌面启动器失败，请将本窗口截图求助。
    pause
    exit /b 1
)

echo.
echo ==================================================
echo   安装完成！
echo   以后每次使用：双击桌面上的 ClaudeScience.bat ，
echo   它会自动启动服务并在浏览器中打开页面。
echo   首次打开需要登录 Claude 账号，账号需要
echo   Pro / Max / Team / Enterprise 订阅。
echo ==================================================
echo.
choice /c YN /m "现在就启动 Claude Science 吗？Y=启动 N=退出"
if errorlevel 2 exit /b 0
call "%LAUNCHER%"
exit /b 0

rem ============================================================
rem  以下以 ::: 开头的内容是桌面启动器 ClaudeScience.bat 的模板，
rem  由第 4 步自动提取生成到桌面，本安装脚本自身不会执行它们。
rem ============================================================
:::@echo off
:::rem  Claude Science 启动器（由 ClaudeScience-Install.bat 自动生成）
:::setlocal
:::chcp 65001 >nul
:::set "WSL_UTF8=1"
:::set "DISTRO=Ubuntu-24.04"
:::set "PORT=8765"
:::title Claude Science
:::echo 正在启动 Claude Science ，请稍候...
:::wsl.exe -d %DISTRO% -- bash -lc "test -x $HOME/.local/bin/claude-science" >nul 2>&1
:::if %errorlevel% neq 0 (
:::    echo [出错] 尚未安装 Claude Science ，或 Ubuntu 未安装成功。
:::    echo        请先运行 ClaudeScience-Install.bat 完成安装。
:::    pause
:::    exit /b 1
:::)
:::rem ---- 通过探测端口判断服务是否已在运行 ----
:::wsl.exe -d %DISTRO% -- bash -lc "timeout 2 bash -c 'exec 3<>/dev/tcp/127.0.0.1/%PORT%' 2>/dev/null" >nul 2>&1
:::if %errorlevel% neq 0 goto start_server
:::echo Claude Science 已在后台运行。
:::set "URL="
:::for /f "usebackq delims=" %%U in (`wsl.exe -d %DISTRO% -- bash -lc "tr -d '\r' < ~/claude-science-server.log 2>/dev/null | sed -e 's/\x1b\[[0-9;]*m//g' | grep -m1 -oE 'https?://localhost[^[:space:]]+|https?://127\.0\.0\.1[^[:space:]]+'"`) do set "URL=%%U"
:::if defined URL if not "%URL:~0,4%"=="http" set "URL="
:::if not defined URL set "URL=http://localhost:%PORT%/"
:::goto openurl
::::start_server
:::echo 正在启动服务，首次启动可能需要一点时间...
:::wsl.exe -d %DISTRO% -- bash -lc "rm -f ~/claude-science-server.log; setsid nohup $HOME/.local/bin/claude-science serve --port %PORT% --no-browser >~/claude-science-server.log 2>&1 & sleep 2"
:::set "URL="
:::set /a TRIES=0
::::waiturl
:::for /f "usebackq delims=" %%U in (`wsl.exe -d %DISTRO% -- bash -lc "tr -d '\r' < ~/claude-science-server.log 2>/dev/null | sed -e 's/\x1b\[[0-9;]*m//g' | grep -m1 -oE 'https?://localhost[^[:space:]]+|https?://127\.0\.0\.1[^[:space:]]+'"`) do set "URL=%%U"
:::if defined URL if not "%URL:~0,4%"=="http" set "URL="
:::if defined URL goto openurl
:::set /a TRIES+=1
:::if %TRIES% geq 60 goto failed
:::timeout /t 2 /nobreak >nul
:::goto waiturl
::::openurl
:::echo.
:::echo 正在打开浏览器："%URL%"
:::start "" "%URL%"
:::echo.
:::echo 若浏览器没有自动打开，请手动复制上面引号里的网址到浏览器地址栏。
:::echo 若页面提示无权限或登录过期，请在命令提示符运行 wsl --shutdown 后再双击本启动器。
:::echo 首次使用需要登录你的 Claude 账号。关闭本窗口不影响后台服务。
:::echo 如需彻底停止服务，可在命令提示符中运行： wsl --shutdown
:::pause
:::exit /b 0
::::failed
:::echo [出错] 启动超时。以下是日志内容，请截图发给协助你的人：
:::wsl.exe -d %DISTRO% -- bash -lc "tail -n 40 ~/claude-science-server.log 2>/dev/null"
:::pause
:::exit /b 1
