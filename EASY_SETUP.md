# Easy ESP32 Setup - Step by Step

## What You'll Do
Install MicroPython on your ESP32 so you can write Python code for it.

**Warning:** This will erase the factory demo.

---

## Step 1: Download MicroPython Firmware

1. Go to: https://micropython.org/download/ESP32_GENERIC/
2. Download the latest **ESP32_GENERIC** `.bin` file
3. Save it to: `Z:\Documents\ham\TRARC\PYTHON\esp32-tft-project\`
4. Rename it to: `firmware.bin` (easier to type)

---

## Step 2: Backup Factory Firmware (Optional)

```bash
cd /z/Documents/ham/TRARC/PYTHON/esp32-tft-project
venv/Scripts/esptool.py --port COM7 read_flash 0 0x400000 factory_backup.bin
```

This saves a backup in case you want the factory demo back later.

---

## Step 3: Flash MicroPython

```bash
# Erase the flash
venv/Scripts/esptool.py --port COM7 erase_flash

# Flash MicroPython (wait for download to finish first!)
venv/Scripts/esptool.py --port COM7 --baud 460800 write_flash -z 0x1000 firmware.bin
```

**This takes about 30 seconds.**

---

## Step 4: Test It Works

```bash
# Connect to the board
venv/Scripts/python.exe -m serial.tools.miniterm COM7 115200
```

You should see:
```
>>>
```

This is the Python prompt! Try:
```python
>>> print("Hello ESP32!")
Hello ESP32!
>>> 
```

**To exit:** Press `Ctrl + ]`

---

## Step 5: Upload Your First Program

```bash
# Upload the test script
venv/Scripts/ampy.exe --port COM7 put examples/hello_display.py main.py

# Press RESET button on ESP32
# The backlight should blink!
```

---

## That's It!

Now you can:
- Write Python code in `src/main.py`
- Upload it: `venv/Scripts/ampy.exe --port COM7 put src/main.py`
- Press RESET button to run it

---

## Quick Reference

```bash
# Upload file
venv/Scripts/ampy.exe --port COM7 put myfile.py

# List files on ESP32
venv/Scripts/ampy.exe --port COM7 ls

# Download file
venv/Scripts/ampy.exe --port COM7 get main.py > downloaded.py

# Connect to REPL
venv/Scripts/python.exe -m serial.tools.miniterm COM7 115200
```

---

## Troubleshooting

**"Failed to connect"**
- Hold BOOT button while running esptool commands
- Try unplugging and replugging USB

**"Port busy"**
- Close any other programs using COM7
- Unplug and replug USB cable

**Need factory demo back?**
```bash
venv/Scripts/esptool.py --port COM7 write_flash 0 factory_backup.bin
```
