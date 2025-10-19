# Image Slideshow Guide

Display BMP images from SD card in an endless loop.

## Quick Start

### Simple Mode (No Display Driver)

This will cycle through images and print their names:

```bash
venv/Scripts/ampy.exe --port COM7 run src/slideshow.py
```

**What it does:**
- Mounts SD card
- Lists all BMP files
- Cycles through them every 2 seconds
- Prints filename for each image

### Full Mode (With Display Driver)

To actually show images on the screen, you need a display driver first.

## Install Display Driver

The ESP32-2432S028R uses an **ILI9341** display controller.

### Option 1: Download Driver

```bash
# Download ILI9341 driver
curl -o ili9341.py https://github.com/rdagger/micropython-ili9341/raw/master/ili9341.py

# Upload to ESP32
venv/Scripts/ampy.exe --port COM7 put ili9341.py
```

### Option 2: Use Alternative Driver

```bash
# ST7789 driver (similar, may work)
curl -o st7789.py https://github.com/russhughes/st7789_mpy/raw/master/st7789.py
venv/Scripts/ampy.exe --port COM7 put st7789.py
```

## Upload Slideshow

```bash
# Upload the slideshow script
venv/Scripts/ampy.exe --port COM7 put src/slideshow.py main.py

# Press RESET button on ESP32
# Slideshow will start automatically!
```

## How It Works

1. **Mounts SD card** using SPI bus 2
2. **Finds all .bmp files** on the card
3. **Sorts them** alphabetically
4. **Displays each image** for 2 seconds
5. **Loops forever** - goes back to first image after last

## Customization

Edit `src/slideshow.py` to change:

```python
# Change display time (in seconds)
time.sleep(2)  # Change to 5 for 5 seconds

# Filter different file types
bmp_files = [f for f in files if f.lower().endswith('.jpg')]

# Reverse order
bmp_files.sort(reverse=True)
```

## Troubleshooting

**"No BMP files found"**
- Make sure SD card has .bmp files
- Files must have .bmp extension

**"Display driver not found"**
- Install ili9341.py driver first
- Or use simple mode (just prints filenames)

**Images don't display**
- Check BMP format (should be 24-bit, 320x240)
- Try converting images to correct format

**Slideshow too fast/slow**
- Change `time.sleep(2)` to desired seconds

## Stop Slideshow

If running via `ampy run`:
- Press `Ctrl+C`

If uploaded as `main.py`:
- Press `RESET` button
- Upload a different `main.py`

## Next Steps

1. Install display driver
2. Test with simple mode first
3. Upload as main.py for auto-start
4. Add more images to SD card
5. Customize timing and order

73! 📻
