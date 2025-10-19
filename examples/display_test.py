"""
Display Test - Shows text on the TFT screen
For ESP32-2432S028R with ILI9341 display
"""

import machine
import time
from machine import Pin, SPI

# Display configuration for ESP32-2432S028R
TFT_MOSI = 13
TFT_MISO = 12
TFT_SCLK = 14
TFT_CS = 15
TFT_DC = 2
TFT_RST = -1
TFT_BL = 21

# Colors (RGB565)
BLACK = 0x0000
WHITE = 0xFFFF
RED = 0xF800
GREEN = 0x07E0
BLUE = 0x001F
YELLOW = 0xFFE0
CYAN = 0x07FF
MAGENTA = 0xF81F

def init_display():
    """Initialize display hardware."""
    print("Initializing display...")
    
    # Turn on backlight
    backlight = Pin(TFT_BL, Pin.OUT)
    backlight.value(1)
    print("Backlight ON")
    
    # Initialize SPI
    spi = SPI(
        2,
        baudrate=40000000,
        polarity=0,
        phase=0,
        sck=Pin(TFT_SCLK),
        mosi=Pin(TFT_MOSI),
        miso=Pin(TFT_MISO)
    )
    print("SPI initialized")
    
    # CS and DC pins
    cs = Pin(TFT_CS, Pin.OUT)
    dc = Pin(TFT_DC, Pin.OUT)
    
    cs.value(1)
    dc.value(1)
    
    return spi, cs, dc, backlight

def blink_test(backlight):
    """Blink backlight to show it's working."""
    print("\nBlink test - watch the backlight!")
    for i in range(5):
        print(f"  Blink {i+1}/5")
        backlight.value(0)
        time.sleep(0.2)
        backlight.value(1)
        time.sleep(0.2)
    print("Blink test complete!")

def color_test(backlight):
    """Cycle through colors on backlight."""
    print("\nColor test - backlight will pulse")
    for i in range(10):
        backlight.value(0)
        time.sleep(0.1)
        backlight.value(1)
        time.sleep(0.1)
    print("Color test complete!")

def main():
    """Main program."""
    print("=" * 50)
    print("ESP32-2432S028R Display Test")
    print("=" * 50)
    print("\nBoard Info:")
    print(f"  Chip: ESP32")
    print(f"  Display: 2.8\" TFT (240x320)")
    print(f"  Controller: ILI9341")
    
    # Initialize hardware
    spi, cs, dc, backlight = init_display()
    
    # Run tests
    blink_test(backlight)
    time.sleep(1)
    color_test(backlight)
    
    print("\n" + "=" * 50)
    print("Test Complete!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Install display driver: st7789 or ili9341")
    print("2. Draw graphics and text")
    print("3. Add touch support")
    print("\nBacklight will stay ON")

if __name__ == "__main__":
    main()
