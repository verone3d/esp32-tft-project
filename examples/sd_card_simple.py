"""
Simple SD Card Reader
Just lists files on SD card
"""

import machine
import os
from machine import Pin, SPI

SD_CS = 5

def read_sd_card():
    """Read SD card contents."""
    print("Reading SD card...")
    
    try:
        # Setup SPI - Use SPI bus 2 (VSPI) with standard pins
        spi = SPI(2, baudrate=1000000, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
        cs = Pin(SD_CS, Pin.OUT)
        
        # Import and mount SD card
        import sdcard
        sd = sdcard.SDCard(spi, cs)
        os.mount(sd, '/sd')
        
        print("\n✓ SD card mounted!")
        print("\nFiles on SD card:")
        print("-" * 40)
        
        # List all files
        for item in os.listdir('/sd'):
            try:
                stat = os.stat('/sd/' + item)
                size = stat[6]
                is_dir = stat[0] & 0x4000
                
                if is_dir:
                    print(f"📁 {item}/")
                else:
                    print(f"📄 {item:<30} {size:>10,} bytes")
            except:
                print(f"? {item}")
        
        print("-" * 40)
        
        # Unmount
        os.umount('/sd')
        print("\n✓ Done!")
        
    except ImportError:
        print("\n✗ Error: sdcard.py module not found")
        print("\nDownload sdcard.py:")
        print("https://github.com/micropython/micropython/raw/master/drivers/sdcard/sdcard.py")
        print("\nThen upload:")
        print("ampy --port COM7 put sdcard.py")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nMake sure:")
        print("- SD card is inserted")
        print("- SD card is formatted (FAT32)")

if __name__ == "__main__":
    read_sd_card()
