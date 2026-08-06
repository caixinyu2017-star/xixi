@echo off
setlocal
cd /d "%~dp0"

REM ==================================================================
REM  Helingr Cultural Portrait - Windows EXE builder
REM  Requires Python 3.10 - 3.12 with "Add Python to PATH" checked.
REM  Output: dist\HelingrPortrait.exe
REM  NOTE: this file is ASCII-only with CRLF line endings on purpose,
REM        so cmd.exe parses it correctly on any Windows code page.
REM ==================================================================

echo.
echo [1/3] Checking Python ...
python --version >nul 2>&1
if errorlevel 1 goto NOPY
python --version

echo.
echo [2/3] Installing dependencies (first run takes 2-5 minutes) ...
python -m pip install --upgrade pip -q
python -m pip install -r requirements.txt -q
if errorlevel 1 goto PIPFAIL

echo.
echo [3/3] Building ...
python -m PyInstaller hlr_desktop.spec --noconfirm --clean
if errorlevel 1 goto BUILDFAIL

echo.
echo ==================================================================
echo   BUILD OK
echo   Executable: %cd%\dist\HelingrPortrait.exe
echo   Double-click it to run. Data is stored in hlr_data next to it.
echo ==================================================================
pause
exit /b 0

:NOPY
echo   ERROR: Python not found.
echo   Install Python 3.10-3.12 from https://www.python.org/downloads/
echo   and tick "Add Python to PATH" during setup.
pause
exit /b 1

:PIPFAIL
echo   ERROR: dependency installation failed. Check your network.
pause
exit /b 1

:BUILDFAIL
echo   ERROR: PyInstaller build failed.
pause
exit /b 1
