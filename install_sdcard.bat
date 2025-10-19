@echo off
REM Install SD card driver to ESP32

echo ========================================
echo SD Card Driver Installer
echo ========================================
echo.

set PORT=COM7
set URL=https://raw.githubusercontent.com/micropython/micropython/master/drivers/sdcard/sdcard.py

echo Downloading sdcard.py driver...
curl -o sdcard.py %URL%

if not exist sdcard.py (
    echo.
    echo Error: Failed to download sdcard.py
    echo.
    echo Manual download:
    echo 1. Go to: %URL%
    echo 2. Save as: sdcard.py
    echo 3. Run: venv\Scripts\ampy.exe --port %PORT% put sdcard.py
    pause
    exit /b 1
)

echo.
echo Uploading to ESP32 on %PORT%...
venv\Scripts\ampy.exe --port %PORT% put sdcard.py

if errorlevel 1 (
    echo.
    echo Error: Failed to upload
    pause
    exit /b 1
)

echo.
echo ========================================
echo SUCCESS!
echo ========================================
echo SD card driver installed!
echo.
echo Now you can run:
echo   venv\Scripts\ampy.exe --port %PORT% run examples\sd_card_simple.py
echo.
pause
