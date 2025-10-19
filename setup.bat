@echo off
REM Setup script for ESP32 TFT project

echo ========================================
echo ESP32-2432S028R TFT Project Setup
echo ========================================
echo.

REM Create virtual environment
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate and install dependencies
echo Installing dependencies...
call venv\Scripts\activate
pip install -r requirements.txt

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Connect your ESP32 via USB
echo 2. Flash MicroPython (see QUICK_START.md)
echo 3. Upload scripts: python tools\upload_tool.py src\main.py
echo.
echo Documentation:
echo - README.md - Project overview
echo - QUICK_START.md - Step-by-step guide
echo.
pause
