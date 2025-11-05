@echo off
setlocal enabledelayedexpansion

echo ====================================
echo VenturaAI Setup Script for Windows
echo ====================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Installing Python...

    :: Download Python installer
    echo Downloading Python installer...
    powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile '%TEMP%\python-installer.exe'"

    :: Install Python silently
    echo Installing Python...
    "%TEMP%\python-installer.exe" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

    :: Wait for installation to complete
    timeout /t 10 /nobreak >nul

    :: Refresh PATH
    call refreshenv >nul 2>&1 || (
        echo Please restart your command prompt and run this script again.
        pause
        exit /b 1
    )

    :: Verify Python installation
    python --version >nul 2>&1
    if !errorlevel! neq 0 (
        echo Python installation failed. Please install Python manually from https://python.org
        pause
        exit /b 1
    )

    echo Python installed successfully.
) else (
    echo Python is already installed.
    python --version
)

echo.

:: Create VenturaAI directory in Documents
set "VENTURA_DIR=%USERPROFILE%\Documents\VenturaAI"
if not exist "%VENTURA_DIR%" (
    echo Creating VenturaAI directory...
    mkdir "%VENTURA_DIR%"
) else (
    echo VenturaAI directory already exists.
)

:: Navigate to VenturaAI directory
cd /d "%VENTURA_DIR%"

:: Initialize virtual environment
echo Creating virtual environment...
if not exist "venv" (
    python -m venv venv
) else (
    echo Virtual environment already exists.
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

:: Install fastmcp
echo Installing fastmcp>=2.0.0...
pip install fastmcp>=2.0.0

:: Create client_proxy.py file
echo Creating client_proxy.py...
(
echo import asyncio
echo from fastmcp import Client, FastMCP
echo.
echo async def run^(^):
echo     async with Client^("https://mcp.venturasecurities.com/mcp"^) as connected_client:
echo         proxy = FastMCP.as_proxy^(connected_client^)
echo         await proxy.run_stdio_async^(^)
echo.
echo.
echo if __name__ == "__main__":
echo     asyncio.run^(run^(^)^)
) > client_proxy.py

echo client_proxy.py created successfully.




:: Detect architecture and download appropriate Claude Desktop
echo.
echo Detecting system architecture...

:: Get processor architecture
for /f "tokens=2 delims==" %%i in ('wmic os get osarchitecture /value ^| find "="') do set ARCH=%%i

echo Architecture detected: %ARCH%



REM Detect architecture
if "%PROCESSOR_ARCHITECTURE%"=="AMD64" (
    set "ARCH=x64"
) else if "%PROCESSOR_ARCHITEW6432%"=="AMD64" (
    set "ARCH=x64"
) else if "%PROCESSOR_ARCHITECTURE%"=="ARM64" (
    set "ARCH=arm64"
) else (
    set "ARCH=x86"
)

REM Download Claude Desktop
call :download_claude_desktop
for /f %%p in ('call :download_claude_desktop') do set "installer_path=%%p"
if !errorlevel! neq 0 exit /b 1

REM Install Claude Desktop
call :install_claude_desktop_windows "%installer_path%"
exit /b !errorlevel!

REM ==========================================
REM FUNCTIONS
REM ==========================================

:download_file
set "url=%~1"
set "output_path=%~2"

echo Downloading from %url%...

REM Try PowerShell first
powershell -Command "try { $ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri '%url%' -OutFile '%output_path%' -UseBasicParsing; Write-Host 'Download completed' } catch { Write-Error $_.Exception.Message; exit 1 }"

if !errorlevel! equ 0 (
    echo Download completed
    exit /b 0
) else (
    echo PowerShell download failed, trying curl...

    REM Try curl as fallback
    curl -L -o "%output_path%" "%url%"
    if !errorlevel! equ 0 (
        echo Download completed with curl
        exit /b 0
    ) else (
        echo Both PowerShell and curl download methods failed
        exit /b 1
    )
)

:download_claude_desktop
echo Downloading Claude Desktop...

set "download_url="
set "installer_name="

if "%ARCH%"=="arm64" (
    set "download_url=https://storage.googleapis.com/osprey-downloads-c02f6a0d-347c-492b-a752-3e0651722e97/nest-win-arm64/Claude-Setup-arm64.exe"
    set "installer_name=Claude-Setup-arm64.exe"
) else (
    set "download_url=https://storage.googleapis.com/osprey-downloads-c02f6a0d-347c-492b-a752-3e0651722e97/nest-win-x64/Claude-Setup-x64.exe"
    set "installer_name=Claude-Setup-x64.exe"
)

set "installer_path=%TEMP%\%installer_name%"
call :download_file "%download_url%" "%installer_path%"
if !errorlevel! neq 0 exit /b 1

echo Claude Desktop downloaded to: %installer_path%
echo %installer_path%
exit /b 0

:install_claude_desktop_windows
set "installer_path=%~1"

echo Installing Claude Desktop on Windows...

REM Run installer silently
echo Running silent installation...
"%installer_path%" /S

REM Wait for installation to complete
echo Waiting for installation to complete...
timeout /t 15 /nobreak >nul

REM Verify installation (check if Claude.exe exists in common locations)
if exist "%LOCALAPPDATA%\Programs\Claude\Claude.exe" (
    echo Claude Desktop installed successfully
) else if exist "%PROGRAMFILES%\Claude\Claude.exe" (
    echo Claude Desktop installed successfully
) else if exist "%PROGRAMFILES(X86)%\Claude\Claude.exe" (
    echo Claude Desktop installed successfully
) else (
    echo Warning: Could not verify Claude Desktop installation
)

REM Clean up installer
if exist "%installer_path%" del "%installer_path%" >nul 2>&1

echo Claude Desktop installation completed
exit /b 0




echo.
echo ====================================
echo Setup Complete!
echo ====================================
echo.
echo VenturaAI directory: %VENTURA_DIR%
echo Virtual environment created and activated
echo fastmcp installed
echo client_proxy.py created
echo Claude Desktop downloaded and installed
echo.
echo To run the client proxy:
echo 1. Navigate to %VENTURA_DIR%
echo 2. Activate the virtual environment: venv\Scripts\activate.bat
echo 3. Run: python client_proxy.py
echo.
echo Press any key to exit...
pause >nul