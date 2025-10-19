@echo off
REM Install ILI9341 display driver

echo ========================================
echo ILI9341 Display Driver Installer
echo ========================================
echo.

set PORT=COM7

echo This will download and install the display driver
echo for your ESP32-2432S028R TFT screen.
echo.
pause

echo Downloading driver...
curl -L -o ili9341.py https://raw.githubusercontent.com/jeffmer/micropython-ili9341/master/ili9341.py

if not exist ili9341.py (
    echo.
    echo Download failed. Creating basic driver...
    echo Note: Full driver installation requires manual download
    pause
    exit /b 1
)

echo.
echo Uploading to ESP32...
venv\Scripts\ampy.exe --port %PORT% put ili9341.py

if errorlevel 1 (
    echo.
    echo Upload failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo SUCCESS!
echo ========================================
echo Display driver installed!
echo.
echo Now run the slideshow:
echo   venv\Scripts\ampy.exe --port %PORT% run src\slideshow.py
echo.
pause
