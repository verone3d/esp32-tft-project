# ESP32 Quick Command Reference

## Setup (First Time)

```powershell
cd Z:\Documents\ham\TRARC\PYTHON\esp32-tft-project
setup.bat
```

## Download Existing Code from ESP32

### Quick Method (Easiest)
```powershell
# Download everything from ESP32
download.bat

# Or specify COM port
download.bat COM4
```

### Manual Method
```powershell
# Activate environment
venv\Scripts\activate

# List files on device
python tools\upload_tool.py --list COM3

# Download specific file
ampy --port COM3 get main.py > main.py

# Download all files
python tools\download_from_esp32.py COM3
```

## Upload Code to ESP32

```powershell
# Upload main script
python tools\upload_tool.py src\main.py COM3

# Upload to specific location
python tools\upload_tool.py myfile.py COM3 /lib/myfile.py
```

## Image Conversion

```powershell
# Convert image for display
python tools\image_converter.py photo.jpg photo.raw

# Specify size
python tools\image_converter.py photo.jpg photo.raw 240 320

# Upload image to ESP32
python tools\upload_tool.py photo.raw COM3 /images/photo.raw
```

## Serial Communication

```powershell
# Connect to REPL
python -m serial.tools.miniterm COM3 115200

# Exit: Ctrl+]
```

## Common Tasks

### Backup Everything
```powershell
download.bat COM3
```

### Upload New Program
```powershell
python tools\upload_tool.py src\main.py COM3
```

### Test Display
```powershell
python tools\upload_tool.py examples\hello_display.py COM3
```

### Flash MicroPython (First Time)
```powershell
esptool.py --port COM3 erase_flash
esptool.py --port COM3 --baud 460800 write_flash -z 0x1000 firmware.bin
```

## File Management

```powershell
# List files
ampy --port COM3 ls

# Delete file
ampy --port COM3 rm filename.py

# Create directory
ampy --port COM3 mkdir /images

# Run without saving
ampy --port COM3 run test.py
```

## Troubleshooting

### Find COM Port
- Device Manager → Ports (COM & LPT)

### Connection Issues
1. Hold BOOT button
2. Press RESET
3. Try different USB cable

### Install Drivers
- CH340: https://www.wch-ic.com/downloads/CH341SER_EXE.html
- CP2102: https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers

## Pin Reference

| Function | GPIO |
|----------|------|
| TFT_MOSI | 13   |
| TFT_SCLK | 14   |
| TFT_CS   | 15   |
| TFT_DC   | 2    |
| TFT_BL   | 21   |
| TOUCH_CS | 33   |
| SD_CS    | 5    |
