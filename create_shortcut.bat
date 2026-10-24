@echo off
chcp 65001 >nul
setlocal
set PYTHONIOENCODING=utf-8
cd /d "%~dp0"

python "create_shortcut.py"
if not errorlevel 1 goto ok

py -3 "create_shortcut.py"
if not errorlevel 1 goto ok

echo.
echo Python not found or the shortcut could not be created.
echo Install Python 3.9+ and try again: https://www.python.org/downloads/
pause
exit /b 1

:ok
echo.
pause
endlocal
