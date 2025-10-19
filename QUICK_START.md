# Quick Start Guide - ESP32-2432S028R

## Step 1: Setup Python Environment

```powershell
cd Z:\Documents\ham\TRARC\PYTHON\esp32-tft-project
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Step 2: Flash MicroPython (First Time Only)

1. **Download MicroPython firmware:**
   - Visit: https://micropython.org/download/esp32/
   - Download latest ESP32 firmware (.bin file)

2. **Connect ESP32 via USB**

3. **Find COM port:**
   - Open Device Manager
   - Look under "Ports (COM & LPT)"
   - Note the COM port (e.g., COM3)

4. **Flash firmware:**
```powershell
# Erase flash
esptool.py --port COM3 erase_flash

# Flash MicroPython
esptool.py --port COM3 --baud 460800 write_flash -z 0x1000 esp32-micropython.bin
```

## Step 3: Test Display

```powershell
# Upload test script
python tools\upload_tool.py examples\hello_display.py

# The display backlight should blink
```

## Step 4: Upload Main Script

```powershell
# Upload your main program
python tools\upload_tool.py src\main.py
```

## Step 5: Convert and Upload Images

```powershell
# Convert image
python tools\image_converter.py myimage.jpg myimage.raw

# Upload to ESP32
python tools\upload_tool.py myimage.raw COM3 /images/myimage.raw
```

## Common Commands

```powershell
# List files on ESP32
python tools\upload_tool.py --list COM3

# Upload file
python tools\upload_tool.py myfile.py COM3

# Convert image
python tools\image_converter.py input.jpg output.raw 240 320
```

## Troubleshooting

**Problem:** "Port COM3 not found"
- Check Device Manager for correct port
- Try different USB cable
- Install CH340 or CP2102 drivers

**Problem:** "Failed to connect to ESP32"
- Hold BOOT button while connecting
- Try lower baud rate: 115200

**Problem:** "ampy not found"
- Run: `pip install adafruit-ampy`

## Next Steps

1. Modify `src/main.py` for your application
2. Add display driver library (ST7789 or ILI9341)
3. Create GUI elements
4. Add WiFi connectivity

73! 📻
