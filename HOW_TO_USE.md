# How to Use ESP32-2432S028R

Complete guide for using your ESP32 development board with TFT display.

## Hardware Overview

**AITRIP ESP32-2432S028R Specifications:**
- **Display:** 2.8" TFT LCD (240x320 pixels)
- **Touch:** Resistive touchscreen
- **MCU:** ESP32 (dual-core, WiFi + Bluetooth)
- **USB:** Micro USB for power and programming
- **SD Card:** MicroSD card slot
- **Buttons:** BOOT and RESET buttons

## Step 1: Connect the Device

1. **Connect USB cable** to your computer
2. **Check Device Manager** (Windows):
   - Press `Win + X` → Device Manager
   - Look under "Ports (COM & LPT)"
   - Note the COM port (e.g., COM3, COM4)

**If no COM port appears:**
- Install CH340 USB driver: https://www.wch-ic.com/downloads/CH341SER_EXE.html
- Or CP2102 driver if using that chip

## Step 2: Download Existing Code from Device

### Method 1: Using ampy (Recommended)

```powershell
cd Z:\Documents\ham\TRARC\PYTHON\esp32-tft-project
venv\Scripts\activate

# List all files on the device
python tools\upload_tool.py --list COM3

# Download a specific file
ampy --port COM3 get main.py > downloaded_main.py

# Download all files
ampy --port COM3 get boot.py > boot.py
ampy --port COM3 get main.py > main.py
```

### Method 2: Using Thonny IDE (Easiest for Beginners)

1. **Download Thonny:** https://thonny.org/
2. **Install and open Thonny**
3. **Configure:**
   - Tools → Options → Interpreter
   - Select "MicroPython (ESP32)"
   - Select your COM port
4. **View files:**
   - View → Files
   - You'll see device files on the right
   - Right-click any file → Download to PC

### Method 3: Using esptool (Backup entire flash)

```powershell
# Backup entire flash memory (4MB)
esptool.py --port COM3 read_flash 0 0x400000 esp32_backup.bin

# This creates a complete backup of everything on the device
```

## Step 3: Read Serial Output

### Using Python

```powershell
# Install pyserial if not already installed
pip install pyserial

# Read serial output
python -m serial.tools.miniterm COM3 115200
```

### Using Thonny

1. Open Thonny
2. Select interpreter and port (as above)
3. Click "Stop/Restart backend" button
4. You'll see the REPL (Python prompt)
5. Press Ctrl+D to soft reboot and see boot messages

### Using PuTTY

1. Download PuTTY: https://www.putty.org/
2. Open PuTTY
3. Select "Serial"
4. Set COM port and speed (115200)
5. Click "Open"

## Step 4: Interact with Device (REPL)

Once connected via serial:

```python
# Test basic commands
>>> print("Hello ESP32!")
Hello ESP32!

# Check MicroPython version
>>> import sys
>>> sys.version
'3.4.0'

# List files
>>> import os
>>> os.listdir('/')
['boot.py', 'main.py']

# Read file contents
>>> with open('main.py', 'r') as f:
...     print(f.read())

# Test display backlight
>>> from machine import Pin
>>> backlight = Pin(21, Pin.OUT)
>>> backlight.value(1)  # Turn on
>>> backlight.value(0)  # Turn off

# Check WiFi
>>> import network
>>> sta = network.WLAN(network.STA_IF)
>>> sta.active(True)
>>> sta.scan()  # Scan for WiFi networks
```

## Step 5: Download All Files Script

Create a helper script to download everything:

```powershell
# Save this as download_all.bat
@echo off
set PORT=COM3
set OUTPUT_DIR=downloaded_code

mkdir %OUTPUT_DIR%
cd %OUTPUT_DIR%

echo Downloading all files from ESP32...

ampy --port %PORT% get boot.py > boot.py 2>nul
ampy --port %PORT% get main.py > main.py 2>nul
ampy --port %PORT% get config.py > config.py 2>nul

echo Done! Files saved to %OUTPUT_DIR%
```

## Common File Locations on ESP32

```
/ (root)
├── boot.py          # Runs first on boot
├── main.py          # Main program
├── lib/             # Libraries folder
│   ├── st7789.py    # Display driver
│   └── ...
├── images/          # Image files
└── config.py        # Configuration
```

## Useful Commands Reference

### List Files
```powershell
ampy --port COM3 ls
ampy --port COM3 ls /lib
```

### Download File
```powershell
ampy --port COM3 get filename.py > local_filename.py
```

### Upload File
```powershell
ampy --port COM3 put local_file.py remote_file.py
```

### Delete File
```powershell
ampy --port COM3 rm filename.py
```

### Create Directory
```powershell
ampy --port COM3 mkdir /images
```

### Run Script (without saving)
```powershell
ampy --port COM3 run test_script.py
```

## Troubleshooting

### "Failed to connect"
1. Hold BOOT button while connecting
2. Press RESET button
3. Try different USB cable
4. Check COM port in Device Manager

### "Permission denied" or "Port busy"
- Close other programs using the port (Arduino IDE, Thonny, etc.)
- Unplug and replug USB cable

### "ampy not found"
```powershell
pip install adafruit-ampy
```

### Device not responding
1. Press RESET button
2. Reflash MicroPython if needed

## Next Steps

1. **Download existing code** using methods above
2. **Examine the code** to understand what's already there
3. **Modify or create new code** in your project
4. **Upload back to device** using upload_tool.py

## Quick Download Script

I'll create a script to download everything automatically:

```powershell
cd Z:\Documents\ham\TRARC\PYTHON\esp32-tft-project
python tools\download_from_esp32.py COM3
```

This will download all files from your ESP32 to the `downloaded_code/` folder.
