@echo off
REM Easy MicroPython flasher

echo ========================================
echo ESP32 MICROPYTHON FLASHER
echo ========================================
echo.
echo This will:
echo 1. Backup factory firmware (optional)
echo 2. Erase flash
echo 3. Install MicroPython
echo.
echo WARNING: This erases the factory demo!
echo.
pause

set PORT=COM7
set FIRMWARE=firmware.bin

if not exist %FIRMWARE% (
    echo.
    echo ERROR: firmware.bin not found!
    echo.
    echo Please download MicroPython firmware:
    echo 1. Go to: https://micropython.org/download/ESP32_GENERIC/
    echo 2. Download latest .bin file
    echo 3. Save as: %FIRMWARE%
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Step 1: Backup Factory Firmware
echo ========================================
set /p BACKUP="Create backup? (y/n): "

if /i "%BACKUP%"=="y" (
    echo Backing up to factory_backup.bin...
    venv\Scripts\esptool.py --port %PORT% read_flash 0 0x400000 factory_backup.bin
    echo Backup complete!
)

echo.
echo ========================================
echo Step 2: Erase Flash
echo ========================================
echo Erasing flash on %PORT%...
venv\Scripts\esptool.py --port %PORT% erase_flash

if errorlevel 1 (
    echo.
    echo ERROR: Failed to erase flash
    echo Try holding BOOT button and run again
    pause
    exit /b 1
)

echo.
echo ========================================
echo Step 3: Flash MicroPython
echo ========================================
echo Flashing %FIRMWARE% to %PORT%...
venv\Scripts\esptool.py --port %PORT% --baud 460800 write_flash -z 0x1000 %FIRMWARE%

if errorlevel 1 (
    echo.
    echo ERROR: Failed to flash firmware
    pause
    exit /b 1
)

echo.
echo ========================================
echo SUCCESS!
echo ========================================
echo MicroPython is now installed!
echo.
echo Next steps:
echo 1. Press RESET button on ESP32
echo 2. Test: venv\Scripts\python.exe -m serial.tools.miniterm COM7 115200
echo 3. Upload code: venv\Scripts\ampy.exe --port COM7 put src\main.py
echo.
pause
