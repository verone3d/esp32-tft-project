"""
SD Card Hardware Debug
Tests SD card pins and SPI communication
"""

import machine
from machine import Pin, SPI
import time

SD_CS = 5
SD_MOSI = 13
SD_MISO = 12
SD_SCLK = 14

print("=" * 60)
print(" SD Card Hardware Debug")
print("=" * 60)

# Test 1: Check pins
print("\n[Test 1: Pin Configuration]")
print(f"  SD_CS:   GPIO {SD_CS}")
print(f"  SD_MOSI: GPIO {SD_MOSI}")
print(f"  SD_MISO: GPIO {SD_MISO}")
print(f"  SD_SCLK: GPIO {SD_SCLK}")

# Test 2: Initialize pins
print("\n[Test 2: Initialize Pins]")
try:
    cs = Pin(SD_CS, Pin.OUT, value=1)
    print("  ✓ CS pin initialized")
except Exception as e:
    print(f"  ✗ CS pin error: {e}")

# Test 3: Initialize SPI
print("\n[Test 3: Initialize SPI]")
try:
    # Try SPI bus 1 (HSPI)
    spi1 = SPI(1, baudrate=100000, sck=Pin(SD_SCLK), mosi=Pin(SD_MOSI), miso=Pin(SD_MISO))
    print("  ✓ SPI bus 1 (HSPI) initialized")
    
    # Send some test data
    cs.value(0)
    spi1.write(b'\xff\xff\xff\xff')
    response = spi1.read(4, 0xff)
    cs.value(1)
    print(f"  Response: {response.hex()}")
    
except Exception as e:
    print(f"  ✗ SPI error: {e}")

# Test 4: Try to detect SD card
print("\n[Test 4: SD Card Detection]")
print("  Attempting to initialize SD card...")
print("  (This may take a few seconds)")

try:
    import sdcard
    
    # Reinitialize with proper settings
    spi = SPI(1, baudrate=100000, polarity=0, phase=0,
              sck=Pin(SD_SCLK), mosi=Pin(SD_MOSI), miso=Pin(SD_MISO))
    cs = Pin(SD_CS, Pin.OUT)
    
    # Try to initialize
    sd = sdcard.SDCard(spi, cs)
    
    print("  ✓ SD card detected!")
    print(f"  Sectors: {sd.sectors}")
    print(f"  Size: {sd.sectors * 512 / 1024 / 1024:.2f} MB")
    
except OSError as e:
    print(f"  ✗ SD card error: {e}")
    print("\n  Troubleshooting:")
    print("  1. Make sure SD card is fully inserted (should click)")
    print("  2. Try removing and reinserting the card")
    print("  3. Verify card is FAT32 formatted")
    print("  4. Try a different SD card")
    print("  5. Power cycle the ESP32 (unplug/replug USB)")
    
except Exception as e:
    print(f"  ✗ Unexpected error: {e}")

# Test 5: Alternative SPI bus
print("\n[Test 5: Try Alternative SPI Configuration]")
try:
    # Try SPI bus 2 (VSPI) - sometimes used instead
    print("  Trying SPI bus 2 (VSPI)...")
    spi2 = SPI(2, baudrate=100000, polarity=0, phase=0,
               sck=Pin(18), mosi=Pin(23), miso=Pin(19))
    cs2 = Pin(SD_CS, Pin.OUT)
    
    import sdcard
    sd2 = sdcard.SDCard(spi2, cs2)
    
    print("  ✓ SD card found on SPI bus 2!")
    print(f"  Note: This board uses SPI2, not SPI1")
    
except Exception as e:
    print(f"  ✗ SPI bus 2 also failed: {e}")

print("\n" + "=" * 60)
print(" Debug complete")
print("=" * 60)
print("\nIf SD card still not detected:")
print("1. Check that card is fully inserted")
print("2. Power cycle ESP32")
print("3. Try different SD card")
print("4. Card may need to be <32GB and FAT32")
