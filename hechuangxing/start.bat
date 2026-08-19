@echo off
cd /d "%~dp0"
title HeChuangXing

REM ---------------------------------------------------------------
REM  This file is intentionally pure ASCII.
REM  Chinese characters inside a .bat file get mangled by cmd.exe
REM  on Chinese Windows, which breaks the whole script.
REM  All Chinese messages are printed by start.py instead.
REM ---------------------------------------------------------------

set "PY="
python --version >nul 2>&1 && set "PY=python"
if not defined PY (
  py -3 --version >nul 2>&1 && set "PY=py -3"
)

if not defined PY goto nopython

%PY% "%~dp0start.py"
echo.
pause
exit /b

:nopython
echo.
echo   Python was not found on this computer.
echo.
echo   Please install Python 3.10 or newer:
echo     1. Open  https://www.python.org/downloads/
echo     2. Download and run the installer
echo     3. IMPORTANT: on the first screen, tick
echo        "Add python.exe to PATH"
echo     4. Then run this file again
echo.
pause
exit /b 1
