@echo off
chcp 65001 >nul
title GhostCore - Fingerprint Testing Suite
cd /d "%~dp0"
python test_fingerprint.py %*
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo An error occurred running test_fingerprint.py.
    pause
)
