@echo off
REM Check ESP32 connection

if "%1"=="" (
    set PORT=COM3
) else (
    set PORT=%1
)

echo ========================================
echo ESP32 CONNECTION CHECKER
echo ========================================
echo Port: %PORT%
echo.

call venv\Scripts\activate

echo Checking if ESP32 is connected...
echo.

python -c "import serial; import time; ser = serial.Serial('%PORT%', 115200, timeout=2); print('Connected!'); ser.write(b'\r\n'); time.sleep(0.5); print(ser.read(100).decode('utf-8', errors='ignore')); ser.close()" 2>nul

if errorlevel 1 (
    echo.
    echo [ERROR] Cannot connect to %PORT%
    echo.
    echo Troubleshooting:
    echo 1. Check Device Manager for correct COM port
    echo 2. Make sure ESP32 is plugged in via USB
    echo 3. Try pressing RESET button on ESP32
    echo 4. Install CH340 or CP2102 USB drivers
    echo.
) else (
    echo.
    echo [SUCCESS] ESP32 is connected on %PORT%
    echo.
)

pause
