@echo off
chcp 65001 >nul 2>&1
title CPE381 Computer Graphics - Exam Calculator
setlocal EnableDelayedExpansion

echo.
echo  ╔══════════════════════════════════════════════╗
echo  ║  CPE381 Computer Graphics Exam Calculator    ║
echo  ╚══════════════════════════════════════════════╝
echo.

REM ── Find Python ──────────────────────────────────
where python >nul 2>&1
if %errorlevel% neq 0 (
    where python3 >nul 2>&1
    if %errorlevel% neq 0 (
        echo  [ERROR] Python is not installed or not in PATH.
        echo  Please install Python 3.8+ from https://www.python.org/downloads/
        echo  Make sure to check "Add Python to PATH" during installation.
        pause
        exit /b 1
    )
    set PYTHON=python3
) else (
    set PYTHON=python
)

for /f "tokens=*" %%v in ('%PYTHON% --version 2^>^&1') do set PYVER=%%v
echo  [OK] %PYVER%
echo.

REM ── Check packages ──────────────────────────────
REM Define packages to check (package_name:import_name)
set "PKGS=numpy:numpy tabulate:tabulate matplotlib:matplotlib"
set MISSING=
set MISSING_COUNT=0

echo  Checking dependencies...
for %%p in (%PKGS%) do (
    for /f "tokens=1,2 delims=:" %%a in ("%%p") do (
        %PYTHON% -c "import %%b" >nul 2>&1
        if !errorlevel! equ 0 (
            echo    [✓] %%a
        ) else (
            echo    [✗] %%a  ^(not found^)
            set "MISSING=!MISSING! %%a"
            set /a MISSING_COUNT+=1
        )
    )
)
echo.

REM ── Install missing packages with progress ──────
if !MISSING_COUNT! equ 0 (
    echo  [OK] All dependencies already installed!
) else (
    echo  Installing !MISSING_COUNT! missing package^(s^)...
    echo.

    REM Upgrade pip silently first
    %PYTHON% -m pip install --quiet --upgrade pip >nul 2>&1

    set INSTALLED=0
    for %%m in (!MISSING!) do (
        set /a INSTALLED+=1
        set /a PCT=!INSTALLED!*100/!MISSING_COUNT!

        REM Build progress bar
        set /a FILLED=!PCT!/5
        set /a EMPTY=20-!FILLED!
        set "BAR="
        for /l %%i in (1,1,!FILLED!) do set "BAR=!BAR!█"
        for /l %%i in (1,1,!EMPTY!) do set "BAR=!BAR!░"

        <nul set /p "=  [!BAR!] !PCT!%%  Installing %%m...                    "
        echo.
        %PYTHON% -m pip install --quiet %%m >nul 2>&1
        if !errorlevel! neq 0 (
            echo  [WARN] Failed to install %%m, retrying...
            %PYTHON% -m pip install %%m
        )
    )

    REM Final 100% bar
    <nul set /p "=  [████████████████████] 100%%  Done!                       "
    echo.
    echo.
    echo  [OK] All packages installed successfully!
)

echo.
echo  ╔══════════════════════════════════════════════╗
echo  ║  Starting Exam Calculator...                 ║
echo  ╚══════════════════════════════════════════════╝
echo.

REM Run with UTF-8 encoding support
%PYTHON% -X utf8 "%~dp0main.py"

echo.
pause
