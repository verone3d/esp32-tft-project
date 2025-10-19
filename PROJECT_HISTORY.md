# ESP32-2432S028R TFT Slideshow - Complete Project History

## Project Overview

This project creates an image slideshow on an ESP32-2432S028R development board with a 2.4" TFT display. Images are read from an SD card and displayed in a continuous loop with configurable delays per image.

---

## Hardware Specifications

**Board:** AITRIP ESP32-2432S028R
- **Display:** 2.4" ILI9341 TFT (240x320 pixels)
- **SD Card:** Micro SD slot
- **Processor:** ESP32 dual-core
- **Flash:** 4MB
- **WiFi:** Built-in

### Pin Configuration

**Display (SPI Bus 1 - HSPI):**
- SCLK: GPIO 14
- MOSI: GPIO 13
- MISO: GPIO 12
- CS: GPIO 15
- DC: GPIO 2
- Backlight: GPIO 21

**SD Card (SPI Bus 2 - VSPI):**
- SCLK: GPIO 18
- MOSI: GPIO 23
- MISO: GPIO 19
- CS: GPIO 5

---

## Setup Process

### 1. Initial Setup

**Tools Installed:**
- Python 3.x with virtual environment
- esptool (for flashing firmware)
- ampy (for file management)
- pyserial (for serial communication)

**Virtual Environment Setup:**
```bash
cd Z:/Documents/ham/TRARC/PYTHON/esp32-tft-project
python -m venv venv
venv/Scripts/activate
pip install esptool adafruit-ampy pyserial
```

### 2. Firmware Flashing

**Backup Factory Firmware:**
```bash
venv/Scripts/python.exe -m esptool --port COM7 read_flash 0 0x400000 factory_backup.bin
```

**Erase Flash:**
```bash
venv/Scripts/python.exe -m esptool --port COM7 erase_flash
```

**Flash MicroPython:**
```bash
venv/Scripts/python.exe -m esptool --port COM7 --baud 460800 write_flash -z 0x1000 firmware.bin
```

**MicroPython Firmware Used:**
- ESP32_GENERIC-20240602-v1.23.0.bin
- Downloaded from: https://micropython.org/download/ESP32_GENERIC/

### 3. File Management

**Upload Files to ESP32:**
```bash
# Upload display driver
venv/Scripts/ampy.exe --port COM7 put ili9341.py

# Upload SD card driver
venv/Scripts/ampy.exe --port COM7 put sdcard.py

# Upload slideshow as main.py (auto-runs on boot)
venv/Scripts/ampy.exe --port COM7 put src/slideshow.py main.py
```

**Run Scripts:**
```bash
# Run without uploading
venv/Scripts/ampy.exe --port COM7 run src/slideshow.py
```

---

## Key Issues Resolved

### Issue 1: Git Bash Path Problems
**Problem:** Commands like `venv\Scripts\python.exe` not working in Git Bash
**Solution:** Use forward slashes: `venv/Scripts/python.exe`

### Issue 2: SD Card Not Detected
**Problem:** "no SD card" error
**Solution:** Board uses SPI bus 2 (VSPI), not SPI bus 1 (HSPI)
- Changed from `SPI(1, ...)` to `SPI(2, ...)`
- Correct pins: GPIO 18, 19, 23, 5

### Issue 3: Display Orientation
**Problem:** Images displayed backwards/mirrored, only 75% of screen used
**Solution:** 
- Set display dimensions to 240x320 (portrait)
- MADCTL register = 0x08 (BGR mode, correct orientation)

### Issue 4: Slow Image Loading
**Problem:** Images took too long to load with visible scrolling
**Solution:** 
- Created RAW RGB565 format converter
- Pre-converts BMP to RGB565 (2x faster loading)
- Optimized SPI speed to 60MHz
- Pre-allocated buffers to avoid memory allocation during display

### Issue 5: sdcard Module Not Found
**Problem:** "invalid syntax" when importing sdcard
**Solution:** Manually created and uploaded sdcard.py driver to ESP32

---

## Project Structure

```
esp32-tft-project/
├── venv/                          # Virtual environment (not in git)
├── src/
│   └── slideshow.py              # Main slideshow script
├── examples/
│   ├── system_info.py            # Display ESP32 system info
│   ├── wifi_test.py              # WiFi scanner
│   ├── display_test.py           # Display backlight test
│   ├── sd_card_simple.py         # Simple SD card reader
│   ├── sd_card_test.py           # Comprehensive SD card test
│   └── sd_card_debug.py          # SD card hardware diagnostics
├── tools/
│   └── convert_images_fast.py    # BMP to RAW converter
├── ili9341.py                     # ILI9341 display driver
├── sdcard.py                      # SD card driver
├── config.txt                     # Configuration template
├── requirements.txt               # Python dependencies
├── GIT_WORKFLOW.md               # Git commands reference
├── QUICK_START.md                # Quick start guide
├── SLIDESHOW_GUIDE.md            # Slideshow usage guide
└── README.md                      # Project documentation
```

---

## Configuration System

### config.txt Format

Place `config.txt` on your SD card (not on ESP32):

```
# Default delay for all images
delay=2

# Per-image delays (optional)
img1.raw=1
img2.raw=3
img3.raw=2
img4.raw=5
logo3.raw=1.5
rose003.raw=4
```

**Features:**
- Default delay applies to all images
- Per-image delays override default
- Supports decimal values (e.g., 1.5 seconds)
- Case-sensitive filenames
- Works with both .bmp and .raw files
- Read once at startup

---

## Image Formats

### BMP Format (Slower)
- 24-bit BMP files
- 240x320 pixels
- Converted to RGB565 on-the-fly
- ~2 seconds to display

### RAW Format (Faster - Recommended)
- Pre-converted RGB565 format
- No conversion needed
- ~1 second to display (2x faster)
- Use `convert_images_fast.py` to create

**Convert Images:**
```bash
venv/Scripts/python.exe tools/convert_images_fast.py Z:/path/to/images
```

---

## Display Driver Details

### ILI9341 Driver (ili9341.py)

**Key Features:**
- 240x320 portrait mode
- 16-bit RGB565 color
- 60MHz SPI speed
- Pre-allocated buffers for speed
- Supports both BMP and RAW formats

**Display Functions:**
- `show_bmp(filepath)` - Display BMP file
- `show_raw(filepath, width, height)` - Display RAW RGB565 file
- `fill(color)` - Fill screen with solid color
- `blit_buffer(buffer, x, y, w, h)` - Write buffer to display

**Initialization:**
```python
from machine import Pin, SPI
from ili9341 import Display

spi = SPI(1, baudrate=60000000, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
display = Display(spi, dc=Pin(2), cs=Pin(15), rst=None)
```

---

## SD Card Driver Details

### SDCard Driver (sdcard.py)

**Mounting SD Card:**
```python
from machine import Pin, SPI
import sdcard
import os

# Initialize SPI for SD card (Bus 2 - VSPI)
spi = SPI(2, baudrate=1000000, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
cs = Pin(5, Pin.OUT)

# Mount SD card
sd = sdcard.SDCard(spi, cs)
os.mount(sd, '/sd')

# List files
files = os.listdir('/sd')
```

**Important:** This board uses SPI bus 2 (VSPI) for SD card, not bus 1!

---

## Slideshow Script Details

### Main Features

1. **Auto-start on boot** (when uploaded as main.py)
2. **Configurable delays** per image
3. **Supports BMP and RAW** formats
4. **Automatic format detection** (prefers RAW if available)
5. **Endless loop** with configurable timing
6. **Backlight control**

### Key Functions

**`init_backlight()`**
- Turns on display backlight (GPIO 21)

**`mount_sd_card()`**
- Mounts SD card at /sd
- Uses SPI bus 2 (VSPI)

**`read_config()`**
- Reads config.txt from SD card
- Parses default and per-image delays
- Returns config dictionary

**`get_image_files()`**
- Lists all .raw and .bmp files
- Prefers .raw files (faster)
- Returns sorted list and file type

**`init_display()`**
- Initializes ILI9341 display
- 60MHz SPI speed
- Returns display object

**`display_image(display, filepath, file_type)`**
- Displays image based on type
- Handles both BMP and RAW formats

**`slideshow_with_display(display, image_files, file_type, config)`**
- Main slideshow loop
- Uses per-image delays from config
- Displays image index and delay time
- Loops endlessly

---

## Performance Optimizations

### Display Speed
1. **60MHz SPI** - Maximum stable speed for this board
2. **Pre-allocated buffers** - No memory allocation during display
3. **Optimized pixel conversion** - Reduced array lookups
4. **4KB chunk size** - Balance between speed and memory

### Image Loading Speed
1. **RAW format** - Pre-converted RGB565 (2x faster than BMP)
2. **Direct memory transfer** - No conversion needed for RAW
3. **Efficient file reading** - Chunked reading for large files

### Attempted Optimizations (Reverted)
- 80MHz SPI - Caused jerky display
- 8KB chunks - No speed improvement, more jerky
- Multi-row buffering - Added complexity without benefit

**Result:** 60MHz SPI with 4KB chunks provides best balance of speed and smoothness.

---

## Testing Scripts

### system_info.py
Displays ESP32 system information:
- MicroPython version
- CPU frequency
- Memory usage
- Flash size
- File system contents

### wifi_test.py
Scans and displays WiFi networks:
- SSID
- Signal strength (RSSI)
- Channel
- Security type

### display_test.py
Tests display hardware:
- Backlight control
- SPI initialization
- Pin configuration

### sd_card_debug.py
Diagnoses SD card issues:
- Tests both SPI buses
- Checks pin configuration
- Verifies SD card detection
- **This script helped identify SPI bus 2 requirement**

---

## Common Commands Reference

### Upload Files
```bash
# Upload display driver
venv/Scripts/ampy.exe --port COM7 put ili9341.py

# Upload SD card driver
venv/Scripts/ampy.exe --port COM7 put sdcard.py

# Upload slideshow (auto-run on boot)
venv/Scripts/ampy.exe --port COM7 put src/slideshow.py main.py
```

### Run Scripts
```bash
# Run without uploading
venv/Scripts/ampy.exe --port COM7 run src/slideshow.py

# Run example scripts
venv/Scripts/ampy.exe --port COM7 run examples/system_info.py
venv/Scripts/ampy.exe --port COM7 run examples/wifi_test.py
```

### List Files on ESP32
```bash
venv/Scripts/ampy.exe --port COM7 ls
```

### Delete Files from ESP32
```bash
venv/Scripts/ampy.exe --port COM7 rm main.py
```

### Convert Images
```bash
venv/Scripts/python.exe tools/convert_images_fast.py Z:/path/to/images
```

---

## Git Workflow

### Before Making Changes
```bash
cd Z:/Documents/ham/TRARC/PYTHON/esp32-tft-project
git pull origin main
```

### After Making Changes
```bash
git add .
git commit -m "Description of changes"
git push origin main
```

See `GIT_WORKFLOW.md` for complete reference.

---

## Troubleshooting Guide

### Problem: Slideshow doesn't auto-start on boot
**Solution:** Upload as main.py:
```bash
venv/Scripts/ampy.exe --port COM7 put src/slideshow.py main.py
```

### Problem: SD card not detected
**Check:**
1. SD card formatted as FAT32
2. SD card properly inserted
3. Using SPI bus 2 (not bus 1)
4. Correct pins: GPIO 18, 19, 23, 5

### Problem: Images display incorrectly
**Check:**
1. Images are 240x320 pixels
2. Images are 24-bit BMP or RAW format
3. Display orientation (MADCTL = 0x08)

### Problem: Images load slowly
**Solution:** Convert to RAW format:
```bash
venv/Scripts/python.exe tools/convert_images_fast.py path/to/images
```

### Problem: Config not working
**Check:**
1. config.txt is on SD card (not ESP32)
2. Filenames match exactly (case-sensitive)
3. Format is: `filename.raw=delay`
4. No extra spaces around =

### Problem: Display is blank
**Check:**
1. Backlight is on (GPIO 21)
2. Display driver uploaded (ili9341.py)
3. Correct SPI pins (GPIO 14, 13, 12, 15, 2)

---

## Technical Specifications

### Memory Usage
- **Flash:** ~100KB for MicroPython scripts
- **RAM:** ~20KB for display buffers
- **SD Card:** Unlimited images (FAT32 limit)

### Performance
- **BMP Loading:** ~2 seconds per image
- **RAW Loading:** ~1 second per image
- **Display Refresh:** 60 FPS capable
- **SPI Speed:** 60MHz (display), 1MHz (SD card)

### Color Depth
- **Display:** 16-bit RGB565 (65,536 colors)
- **BMP Input:** 24-bit RGB888
- **RAW Input:** 16-bit RGB565 (pre-converted)

### File Size
- **BMP (240x320):** ~225KB per image
- **RAW (240x320):** ~150KB per image
- **Savings:** ~33% smaller with RAW format

---

## Future Enhancement Ideas

### Possible Improvements
1. **Touch screen support** - Board has touch controller
2. **Button controls** - Pause, skip, speed control
3. **Transition effects** - Fade, slide, etc.
4. **Image scaling** - Support different resolutions
5. **WiFi image download** - Fetch images from server
6. **Random order** - Shuffle images
7. **Folder support** - Organize images in folders
8. **Status display** - Show image info overlay
9. **Power saving** - Sleep mode between images
10. **Multiple playlists** - Switch between image sets

### Hardware Additions
- External buttons for control
- RTC module for scheduled slideshows
- Larger SD card support
- External power supply for 24/7 operation

---

## Important Notes

### Git Bash vs PowerShell
- **Git Bash:** Use forward slashes (`/`)
- **PowerShell/CMD:** Use backslashes (`\`)
- **Recommendation:** Use PowerShell for consistency

### Network Drive Issues
- Project on NAS (Z: drive)
- Git requires safe.directory exception
- Consider moving to local drive for better Git performance

### Serial Port
- **Port:** COM7
- **Baud:** 115200 (default), 460800 (flashing)
- **Driver:** CP2102 USB-to-UART

### MicroPython Limitations
- Limited RAM (~100KB free)
- No floating point display in some operations
- File I/O is slower than native code
- Some Python libraries not available

---

## Resources

### Documentation
- MicroPython: https://docs.micropython.org/
- ESP32: https://docs.espressif.com/
- ILI9341: https://cdn-shop.adafruit.com/datasheets/ILI9341.pdf

### Tools
- esptool: https://github.com/espressif/esptool
- ampy: https://github.com/scientifichackers/ampy
- MicroPython firmware: https://micropython.org/download/

### Community
- MicroPython Forum: https://forum.micropython.org/
- ESP32 Forum: https://www.esp32.com/

---

## Project Timeline

1. **Initial Setup** - Installed tools, created virtual environment
2. **Firmware Flash** - Backed up factory firmware, flashed MicroPython
3. **Basic Tests** - System info, WiFi scan, display backlight
4. **SD Card Setup** - Debugged SPI bus issue, mounted SD card
5. **Display Driver** - Created ILI9341 driver, fixed orientation
6. **Slideshow Script** - Basic loop, image display
7. **Optimization** - RAW format, speed improvements
8. **Configuration** - Added config.txt support
9. **Per-Image Delays** - Individual timing per image
10. **Documentation** - Created comprehensive guides

---

## Credits

**Hardware:** AITRIP ESP32-2432S028R
**Firmware:** MicroPython v1.23.0
**Display Driver:** Custom ILI9341 driver (based on community examples)
**SD Card Driver:** MicroPython community sdcard.py

---

## License

This project is open source. Feel free to modify and share!

---

## Contact

For questions or issues, refer to:
- Project documentation in this repository
- MicroPython forums
- ESP32 community resources

---

**Last Updated:** October 18, 2025
**Version:** 1.0
**Status:** Complete and working

73! 📻🖼️
