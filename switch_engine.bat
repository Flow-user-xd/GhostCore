@echo off
chcp 65001 >nul
title GhostCore Switch Browser Version
cd /d "%~dp0"

echo ===================================================================
echo           GhostCore Studio - Switch Browser Engine Version
echo ===================================================================
echo.

python setup_portable_chromium.py --interactive

echo.
pause
