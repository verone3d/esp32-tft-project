"""
Image Slideshow for ESP32-2432S028R
Displays BMP images from SD card in a loop
Each image shows for 2 seconds
"""

import machine
import os
import time
from machine import Pin, SPI

# Display pins
TFT_MOSI = 13
TFT_MISO = 12
TFT_SCLK = 14
TFT_CS = 15
TFT_DC = 2
TFT_RST = -1
TFT_BL = 21

# SD Card pins (SPI2)
SD_CS = 5
SD_SCLK = 18
SD_MOSI = 23
SD_MISO = 19

def init_backlight():
    """Turn on display backlight."""
    backlight = Pin(TFT_BL, Pin.OUT)
    backlight.value(1)
    print("✓ Backlight ON")
    return backlight

def mount_sd_card():
    """Mount SD card."""
    print("Mounting SD card...")
    try:
        # Initialize SPI for SD card (SPI bus 2)
        spi = SPI(2, baudrate=1000000, sck=Pin(SD_SCLK), mosi=Pin(SD_MOSI), miso=Pin(SD_MISO))
        cs = Pin(SD_CS, Pin.OUT)
        
        # Mount SD card
        import sdcard
        sd = sdcard.SDCard(spi, cs)
        os.mount(sd, '/sd')
        
        print("✓ SD card mounted")
        return True
    except Exception as e:
        print(f"✗ SD card error: {e}")
        return False

def read_config():
    """Read configuration from config.txt on SD card."""
    config = {
        'delay': 2  # Default delay in seconds
    }
    
    try:
        with open('/sd/config.txt', 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip().lower()
                    value = value.strip()
                    
                    if key == 'delay':
                        try:
                            config['delay'] = float(value)
                            print(f"Config: delay = {config['delay']} seconds")
                        except ValueError:
                            print(f"Invalid delay value: {value}, using default")
        
    except OSError:
        print("No config.txt found, using defaults")
        print(f"  Default delay: {config['delay']} seconds")
    except Exception as e:
        print(f"Error reading config: {e}")
    
    return config

def get_image_files():
    """Get list of image files from SD card (RAW or BMP)."""
    try:
        files = os.listdir('/sd')
        # Filter for RAW files first (faster), then BMP
        raw_files = [f for f in files if f.lower().endswith('.raw')]
        bmp_files = [f for f in files if f.lower().endswith('.bmp')]
        
        # Prefer RAW files if available
        if raw_files:
            print(f"Using {len(raw_files)} RAW files (fast mode)")
            raw_files.sort()
            return raw_files, 'raw'
        else:
            print(f"Using {len(bmp_files)} BMP files (normal mode)")
            bmp_files.sort()
            return bmp_files, 'bmp'
    except Exception as e:
        print(f"Error reading files: {e}")
        return [], 'bmp'

def init_display():
    """Initialize ILI9341 display."""
    print("Initializing display...")
    try:
        # Initialize SPI for display (SPI bus 1) - Faster baudrate
        spi = SPI(1, baudrate=60000000, sck=Pin(TFT_SCLK), mosi=Pin(TFT_MOSI), miso=Pin(TFT_MISO))
        
        # Import display driver
        from ili9341 import Display
        
        # Initialize display (no reset pin on this board)
        display = Display(spi, dc=Pin(TFT_DC), cs=Pin(TFT_CS), rst=None)
        
        print("✓ Display initialized")
        return display
    except ImportError:
        print("✗ Display driver not found")
        print("  Install ili9341.py driver first")
        return None
    except Exception as e:
        print(f"✗ Display error: {e}")
        return None

def display_image(display, filepath, file_type='bmp'):
    """Display an image on screen."""
    try:
        if file_type == 'raw':
            # RAW files are much faster (no conversion needed)
            success = display.show_raw(filepath, 240, 320)
        else:
            # BMP files need conversion
            success = display.show_bmp(filepath)
        
        if success:
            print(f"    ✓ Displayed")
        else:
            print(f"    ✗ Failed to display")
    except Exception as e:
        print(f"    ✗ Error: {e}")

def slideshow_simple(image_files):
    """Simple slideshow without display driver (just prints info)."""
    print("\n" + "=" * 60)
    print(" SLIDESHOW MODE (Simple)")
    print("=" * 60)
    print(f"Found {len(image_files)} images")
    print("Press Ctrl+C to stop\n")
    
    image_index = 0
    
    try:
        while True:
            # Get current image
            image_file = image_files[image_index]
            
            print(f"[{image_index + 1}/{len(image_files)}] Displaying: {image_file}")
            
            # In full version, this would display the image
            # For now, just show the filename
            
            # Wait 2 seconds
            time.sleep(2)
            
            # Move to next image
            image_index = (image_index + 1) % len(image_files)
            
    except KeyboardInterrupt:
        print("\n\nSlideshow stopped")

def slideshow_with_display(display, image_files, file_type='bmp', delay=2):
    """Full slideshow with display driver."""
    print("\n" + "=" * 60)
    print(f" SLIDESHOW MODE ({'Fast' if file_type == 'raw' else 'Normal'})")
    print("=" * 60)
    print(f"Found {len(image_files)} images")
    print(f"Delay: {delay} seconds per image")
    print("Press Ctrl+C to stop\n")
    
    image_index = 0
    
    try:
        while True:
            # Get current image
            image_file = image_files[image_index]
            filepath = '/sd/' + image_file
            
            print(f"[{image_index + 1}/{len(image_files)}] {image_file}")
            
            # Display the image
            display_image(display, filepath, file_type)
            
            # Wait configured delay
            time.sleep(delay)
            
            # Move to next image
            image_index = (image_index + 1) % len(image_files)
            
    except KeyboardInterrupt:
        print("\n\nSlideshow stopped")

def main():
    """Main program."""
    print("=" * 60)
    print(" ESP32 Image Slideshow")
    print("=" * 60)
    print()
    
    # Turn on backlight
    backlight = init_backlight()
    
    # Mount SD card
    if not mount_sd_card():
        print("\nCannot continue without SD card")
        return
    
    # Read configuration
    config = read_config()
    delay = config['delay']
    
    # Get image files
    image_files, file_type = get_image_files()
    
    if not image_files:
        print("\nNo image files found on SD card")
        return
    
    print(f"\nFound {len(image_files)} images:")
    for i, f in enumerate(image_files, 1):
        print(f"  {i}. {f}")
    
    # Try to initialize display
    display = init_display()
    
    if display:
        # Full slideshow with display
        slideshow_with_display(display, image_files, file_type, delay)
    else:
        # Simple slideshow (just prints filenames)
        print("\nRunning in simple mode (no display driver)")
        print("Images will be listed but not displayed")
        slideshow_simple(image_files)

if __name__ == "__main__":
    main()
