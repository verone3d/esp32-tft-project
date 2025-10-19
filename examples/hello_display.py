"""
Hello Display Example
Basic display test for ESP32-2432S028R
"""

import machine
import time
from machine import Pin

# Backlight pin
TFT_BL = 21


def main():
    """Simple display test."""
    print("Hello Display Test")
    
    # Setup backlight
    backlight = Pin(TFT_BL, Pin.OUT)
    
    # Blink backlight
    for i in range(5):
        print(f"Blink {i+1}")
        backlight.value(1)  # On
        time.sleep(0.5)
        backlight.value(0)  # Off
        time.sleep(0.5)
    
    # Leave on
    backlight.value(1)
    print("Display test complete!")


if __name__ == "__main__":
    main()
