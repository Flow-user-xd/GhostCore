@echo off
title GhostCore Anti-Detect Studio
cd /d "%~dp0"

echo ===================================================================
echo           GhostCore Studio - Anti-Detect Launcher
echo ===================================================================
echo.

:: 1. Verify Python Installation
where python >nul 2>nul
if %errorlevel% equ 0 goto :python_ready

echo.
echo ===================================================================
echo   [!] Python 3 was not detected in your system PATH.
echo ===================================================================
echo GhostCore requires Python 3.10+ to run the anti-detect server.
echo.
set "INSTALL_PY=Y"
set /p "INSTALL_PY=Would you like to install Python 3 automatically from CMD? [Y/N] (default: Y): "
if /i "%INSTALL_PY%"=="N" goto :no_python

echo.
echo [*] Installing Python 3 via Windows Package Manager (winget)...
where winget >nul 2>nul
if %errorlevel% equ 0 (
    winget install --id Python.Python.3.12 -e --accept-package-agreements --accept-source-agreements
) else (
    echo [*] winget not found. Downloading official Python installer via PowerShell...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; (New-Object System.Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.12.8/python-3.12.8-amd64.exe', '%TEMP%\py_installer.exe')"
    echo [*] Running quiet installer...
    "%TEMP%\py_installer.exe" /passive PrependPath=1 Include_test=0 SimpleInstall=1
    if exist "%TEMP%\py_installer.exe" del "%TEMP%\py_installer.exe"
)

:: Refresh PATH for current CMD session
set "PATH=%LOCALAPPDATA%\Programs\Python\Python312;%LOCALAPPDATA%\Programs\Python\Python312\Scripts;C:\Program Files\Python312;C:\Program Files\Python312\Scripts;%PATH%"

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Python installation finished, but python.exe is not yet in the active PATH.
    echo Please close this window and double-click start.bat again!
    echo.
    pause
    exit /b 1
)
echo [+] Python 3 successfully installed!
echo.

:python_ready
echo [1/4] Python detected:
python --version

:: 2. Verify Dependencies
echo.
echo [2/4] Checking requirements...
if exist requirements.txt (
    python -m pip install -q -r requirements.txt
)

:: 3. Verify Chromium Engine
echo.
echo [3/4] Checking Chromium browser engine...
if exist "browser_core\chrome.exe" goto :chrome_ready

echo.
echo ===================================================================
echo   [!] Portable Chromium engine not found in browser_core\
echo ===================================================================
echo GhostCore uses Ungoogled Chromium for 100%% stealth profile isolation.
echo.
set "INSTALL_CR=Y"
set /p "INSTALL_CR=Would you like to select and install one of the latest 3 Chromium versions? [Y/N] (default: Y): "
if /i "%INSTALL_CR%"=="N" goto :skip_chrome

python setup_portable_chromium.py --interactive

if exist "browser_core\chrome.exe" goto :chrome_ready

echo.
echo [ERROR] Chromium browser core not found in browser_core\chrome.exe!
echo You can run 'python setup_portable_chromium.py --interactive' at any time.
echo.
pause
exit /b 1

:skip_chrome
echo.
echo [WARNING] Continuing without portable Chromium. Profiles cannot be launched until installed.
echo.

:chrome_ready
:: 4. Verify Ghost Tunnel (Go Proxy)
echo.
echo [4/4] Checking Ghost Tunnel proxy...
if exist "ghost_tunnel\ghost_tunnel.exe" goto :ghost_ready

echo.
echo ===================================================================
echo   [!] Ghost Tunnel proxy not found.
echo ===================================================================
echo GhostCore requires the Go proxy to perfectly spoof macOS/Linux TCP/TLS.
echo.
set "INSTALL_GO=Y"
set /p "INSTALL_GO=Would you like to install Go and build the proxy? [Y/N] (default: Y): "
if /i "%INSTALL_GO%"=="N" goto :skip_ghost

where go >nul 2>nul
if %errorlevel% neq 0 (
    echo [*] Installing Go via Windows Package Manager (winget)...
    winget install --id GoLang.Go -e --accept-package-agreements --accept-source-agreements
    
    :: Refresh PATH for Go
    set "PATH=C:\Program Files\Go\bin;%PATH%"
)

where go >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Go installation failed or go.exe not in PATH. 
    echo Please install Go manually from https://go.dev/dl/ and restart.
    pause
    goto :skip_ghost
)

echo [*] Building Ghost Tunnel...
cd ghost_tunnel
go mod tidy
go build -ldflags="-s -w" -o ghost_tunnel.exe main.go
cd ..

if exist "ghost_tunnel\ghost_tunnel.exe" (
    echo [+] Ghost Tunnel successfully built!
) else (
    echo [ERROR] Failed to build Ghost Tunnel.
)

:skip_ghost
:ghost_ready

echo.
echo ===================================================================
echo   Launching GhostCore Studio on http://localhost:3000 ...
echo ===================================================================
echo.

python server.py

echo.
echo [GhostCore] Server closed.
pause
exit /b 0

:no_python
echo.
echo [ERROR] Python 3 is required to run GhostCore Studio.
echo Please install Python from https://www.python.org/downloads/
echo (Make sure to check "Add python.exe to PATH" during install)
echo.
pause
exit /b 1

