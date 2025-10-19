"""
System Info - Show ESP32 details
"""

import machine
import sys
import os
import time

def show_system_info():
    """Display system information."""
    print("=" * 60)
    print(" ESP32-2432S028R System Information")
    print("=" * 60)
    
    # Python version
    print("\n[Python]")
    print(f"  Version: {sys.version}")
    print(f"  Platform: {sys.platform}")
    print(f"  Implementation: {sys.implementation.name}")
    
    # Chip info
    print("\n[Hardware]")
    freq = machine.freq()
    print(f"  CPU Frequency: {freq/1000000:.0f} MHz")
    print(f"  Chip: ESP32-D0WD-V3")
    print(f"  Features: WiFi, Bluetooth, Dual Core")
    
    # Memory info
    print("\n[Memory]")
    import gc
    gc.collect()
    free = gc.mem_free()
    allocated = gc.mem_alloc()
    total = free + allocated
    print(f"  Total RAM: {total:,} bytes ({total/1024:.1f} KB)")
    print(f"  Used RAM: {allocated:,} bytes ({allocated/1024:.1f} KB)")
    print(f"  Free RAM: {free:,} bytes ({free/1024:.1f} KB)")
    print(f"  Usage: {(allocated/total)*100:.1f}%")
    
    # Flash info
    print("\n[Flash Storage]")
    try:
        stat = os.statvfs('/')
        block_size = stat[0]
        total_blocks = stat[2]
        free_blocks = stat[3]
        total_size = block_size * total_blocks
        free_size = block_size * free_blocks
        used_size = total_size - free_size
        
        print(f"  Total: {total_size:,} bytes ({total_size/1024/1024:.2f} MB)")
        print(f"  Used: {used_size:,} bytes ({used_size/1024:.1f} KB)")
        print(f"  Free: {free_size:,} bytes ({free_size/1024/1024:.2f} MB)")
        print(f"  Usage: {(used_size/total_size)*100:.1f}%")
    except:
        print("  Unable to read flash info")
    
    # Files
    print("\n[Files]")
    try:
        files = os.listdir('/')
        print(f"  Root directory files: {len(files)}")
        for f in files:
            try:
                stat = os.stat(f)
                size = stat[6]
                print(f"    - {f:<20} {size:>8,} bytes")
            except:
                print(f"    - {f}")
    except:
        print("  Unable to list files")
    
    # Uptime
    print("\n[System]")
    uptime = time.ticks_ms() / 1000
    print(f"  Uptime: {uptime:.1f} seconds")
    
    # Display pins
    print("\n[Display Pins - ESP32-2432S028R]")
    print("  TFT_MOSI: GPIO 13")
    print("  TFT_SCLK: GPIO 14")
    print("  TFT_CS:   GPIO 15")
    print("  TFT_DC:   GPIO 2")
    print("  TFT_BL:   GPIO 21")
    print("  TOUCH_CS: GPIO 33")
    print("  SD_CS:    GPIO 5")
    
    print("\n" + "=" * 60)
    print(" System check complete!")
    print("=" * 60)

def main():
    """Main program."""
    show_system_info()

if __name__ == "__main__":
    main()
