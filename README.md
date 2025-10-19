# ESP32-2432S028R TFT Display Project

Python tools and MicroPython scripts for the AITRIP ESP32-2432S028R development board with 2.8" TFT touchscreen display.

## Hardware Specifications

**Board:** ESP32-2432S028R
- **MCU:** ESP32 (WiFi + Bluetooth)
- **Display:** 2.8" TFT LCD
- **Resolution:** 240x320 pixels
- **Touch:** Resistive touchscreen
- **Interface:** SPI

## Features

- WiFi and Bluetooth connectivity
- Touch-enabled display
- MicroPython support
- Image display capabilities
- GUI development tools

## Project Structure

```
esp32-tft-project/
├── src/
│   └── main.py              # Main MicroPython script
├── tools/
│   ├── image_converter.py   # Convert images for display
│   └── upload_tool.py       # Upload files to ESP32
├── examples/
│   ├── hello_display.py     # Basic display example
│   ├── touch_test.py        # Touch screen test
│   └── wifi_connect.py      # WiFi connection example
├── images/                  # Image assets
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Setup

### 1. Install MicroPython on ESP32

Download MicroPython firmware for ESP32:
```bash
# Install esptool
pip install esptool

# Erase flash
esptool.py --port COM3 erase_flash

# Flash MicroPython
esptool.py --port COM3 --baud 460800 write_flash -z 0x1000 esp32-micropython.bin
```

### 2. Install Python Tools

```bash
cd Z:\Documents\ham\TRARC\PYTHON\esp32-tft-project
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Display Pinout (ESP32-2432S028R)

| Function | GPIO Pin |
|----------|----------|
| TFT_MOSI | GPIO 13  |
| TFT_MISO | GPIO 12  |
| TFT_SCLK | GPIO 14  |
| TFT_CS   | GPIO 15  |
| TFT_DC   | GPIO 2   |
| TFT_RST  | GPIO -1  |
| TFT_BL   | GPIO 21  |
| TOUCH_CS | GPIO 33  |
| SD_CS    | GPIO 5   |

## Quick Start

### Test Display

```python
# Upload and run hello_display.py
python tools/upload_tool.py examples/hello_display.py
```

### Convert Image for Display

```python
# Convert image to raw RGB565 format
python tools/image_converter.py input.jpg output.raw
```

## Usage Examples

See the `examples/` directory for:
- Basic display operations
- Touch screen handling
- WiFi connectivity
- Image display
- GUI elements

## Resources

- [ESP32 MicroPython Documentation](https://docs.micropython.org/en/latest/esp32/quickref.html)
- [TFT Display Driver](https://github.com/russhughes/st7789_mpy)
- Board schematic and pinout

## License

MIT License
