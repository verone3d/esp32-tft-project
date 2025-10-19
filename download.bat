@echo off
REM Quick download script for ESP32 files

if "%1"=="" (
    set PORT=COM3
) else (
    set PORT=%1
)

echo ========================================
echo ESP32 FILE DOWNLOADER
echo ========================================
echo Port: %PORT%
echo.

REM Use venv Python directly instead of activate
if exist venv\Scripts\python.exe (
    venv\Scripts\python.exe tools\download_from_esp32.py %PORT%
) else (
    echo Error: Virtual environment not found
    echo Run setup.bat first
    pause
    exit /b 1
)

echo.
echo Check the 'downloaded_code' folder for your files.
pause
