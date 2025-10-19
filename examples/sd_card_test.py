"""
SD Card Reader for ESP32-2432S028R
Reads and displays contents of SD card
"""

import machine
import os
import time
from machine import Pin, SPI

# SD Card pin for ESP32-2432S028R
SD_CS = 5

def init_sd_card():
    """Initialize SD card."""
    print("=" * 60)
    print(" SD Card Reader - ESP32-2432S028R")
    print("=" * 60)
    print("\nInitializing SD card...")
    
    try:
        # Initialize SPI for SD card - Use SPI bus 2 (VSPI)
        spi = SPI(
            2,
            baudrate=1000000,
            polarity=0,
            phase=0,
            sck=Pin(18),
            mosi=Pin(23),
            miso=Pin(19)
        )
        
        # Initialize SD card
        cs = Pin(SD_CS, Pin.OUT)
        
        # Import SD card driver
        import sdcard
        sd = sdcard.SDCard(spi, cs)
        
        # Mount SD card
        os.mount(sd, '/sd')
        
        print("✓ SD card mounted successfully!")
        return True
        
    except ImportError:
        print("✗ Error: sdcard module not found")
        print("\nTo install sdcard driver:")
        print("1. Download: https://github.com/micropython/micropython/blob/master/drivers/sdcard/sdcard.py")
        print("2. Upload: ampy --port COM7 put sdcard.py")
        return False
        
    except Exception as e:
        print(f"✗ Error initializing SD card: {e}")
        print("\nTroubleshooting:")
        print("- Make sure SD card is inserted")
        print("- Check SD card is formatted (FAT32)")
        print("- Try reinserting the card")
        return False

def list_directory(path, indent=0):
    """List directory contents recursively."""
    try:
        items = os.listdir(path)
        
        for item in sorted(items):
            item_path = path + '/' + item if path != '/' else '/' + item
            
            try:
                stat = os.stat(item_path)
                is_dir = stat[0] & 0x4000  # Check if directory
                
                prefix = "  " * indent
                
                if is_dir:
                    print(f"{prefix}📁 {item}/")
                    # Recursively list subdirectory
                    list_directory(item_path, indent + 1)
                else:
                    size = stat[6]
                    if size < 1024:
                        size_str = f"{size} B"
                    elif size < 1024 * 1024:
                        size_str = f"{size/1024:.1f} KB"
                    else:
                        size_str = f"{size/1024/1024:.2f} MB"
                    
                    print(f"{prefix}📄 {item:<30} {size_str:>10}")
                    
            except Exception as e:
                print(f"{prefix}? {item} (error: {e})")
                
    except Exception as e:
        print(f"Error reading directory: {e}")

def get_sd_info():
    """Get SD card information."""
    try:
        stat = os.statvfs('/sd')
        
        block_size = stat[0]
        total_blocks = stat[2]
        free_blocks = stat[3]
        
        total_size = block_size * total_blocks
        free_size = block_size * free_blocks
        used_size = total_size - free_size
        
        print("\n[SD Card Info]")
        print(f"  Total Size: {total_size/1024/1024:.2f} MB")
        print(f"  Used Space: {used_size/1024/1024:.2f} MB")
        print(f"  Free Space: {free_size/1024/1024:.2f} MB")
        print(f"  Usage: {(used_size/total_size)*100:.1f}%")
        
    except Exception as e:
        print(f"Could not get SD card info: {e}")

def read_file_sample(filepath, lines=10):
    """Read and display first few lines of a text file."""
    try:
        print(f"\n[Preview: {filepath}]")
        print("-" * 60)
        
        with open(filepath, 'r') as f:
            for i, line in enumerate(f):
                if i >= lines:
                    print("... (file continues)")
                    break
                print(line.rstrip())
        
        print("-" * 60)
        
    except Exception as e:
        print(f"Could not read file: {e}")

def count_files(path='/sd'):
    """Count total files and directories."""
    file_count = 0
    dir_count = 0
    total_size = 0
    
    def count_recursive(p):
        nonlocal file_count, dir_count, total_size
        try:
            items = os.listdir(p)
            for item in items:
                item_path = p + '/' + item if p != '/' else '/' + item
                try:
                    stat = os.stat(item_path)
                    is_dir = stat[0] & 0x4000
                    
                    if is_dir:
                        dir_count += 1
                        count_recursive(item_path)
                    else:
                        file_count += 1
                        total_size += stat[6]
                except:
                    pass
        except:
            pass
    
    count_recursive(path)
    return file_count, dir_count, total_size

def main():
    """Main program."""
    # Initialize SD card
    if not init_sd_card():
        return
    
    # Get SD card info
    get_sd_info()
    
    # Count files
    print("\n[Scanning SD card...]")
    file_count, dir_count, total_size = count_files('/sd')
    print(f"  Files: {file_count}")
    print(f"  Directories: {dir_count}")
    print(f"  Total file size: {total_size/1024:.1f} KB")
    
    # List contents
    print("\n[SD Card Contents]")
    print("-" * 60)
    list_directory('/sd')
    print("-" * 60)
    
    # Look for interesting files to preview
    print("\n[Looking for text files...]")
    try:
        items = os.listdir('/sd')
        text_files = [f for f in items if f.endswith(('.txt', '.log', '.csv', '.json'))]
        
        if text_files:
            print(f"Found {len(text_files)} text file(s)")
            # Preview first text file
            read_file_sample('/sd/' + text_files[0])
        else:
            print("No text files found")
            
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 60)
    print(" SD Card scan complete!")
    print("=" * 60)
    
    # Unmount
    try:
        os.umount('/sd')
        print("\n✓ SD card unmounted safely")
    except:
        pass

if __name__ == "__main__":
    main()
