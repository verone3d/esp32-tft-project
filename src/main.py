"""
Main MicroPython script for ESP32-2432S028R
2.8" TFT Display with Touch
"""

import machine
import time
from machine import Pin, SPI

# Display pins for ESP32-2432S028R
TFT_MOSI = 13
TFT_MISO = 12
TFT_SCLK = 14
TFT_CS = 15
TFT_DC = 2
TFT_BL = 21  # Backlight

# Touch pins
TOUCH_CS = 33

# SD Card
SD_CS = 5


def init_display():
    """Initialize the TFT display."""
    print("Initializing display...")
    
    # Setup backlight
    backlight = Pin(TFT_BL, Pin.OUT)
    backlight.value(1)  # Turn on backlight
    
    # Setup SPI
    spi = SPI(
        2,
        baudrate=40000000,
        polarity=0,
        phase=0,
        sck=Pin(TFT_SCLK),
        mosi=Pin(TFT_MOSI),
        miso=Pin(TFT_MISO)
    )
    
    print("Display initialized!")
    return spi


def main():
    """Main program."""
    print("ESP32-2432S028R Starting...")
    print("Display: 240x320 TFT")
    
    # Initialize display
    spi = init_display()
    
    # Your code here
    print("Ready!")
    
    # Main loop
    while True:
        # Add your application logic
        time.sleep(1)


if __name__ == "__main__":
    main()
