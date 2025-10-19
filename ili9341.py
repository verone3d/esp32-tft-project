"""
ILI9341 Display Driver for ESP32-2432S028R
Simplified driver for displaying BMP images
"""

from micropython import const
from machine import Pin
import time

# ILI9341 Commands
ILI9341_SWRESET = const(0x01)
ILI9341_SLPOUT = const(0x11)
ILI9341_DISPON = const(0x29)
ILI9341_CASET = const(0x2A)
ILI9341_PASET = const(0x2B)
ILI9341_RAMWR = const(0x2C)
ILI9341_MADCTL = const(0x36)
ILI9341_PIXFMT = const(0x3A)

# Display dimensions (portrait mode)
WIDTH = const(240)
HEIGHT = const(320)


class Display:
    """ILI9341 display driver."""
    
    def __init__(self, spi, dc, cs, rst=None, width=WIDTH, height=HEIGHT):
        """Initialize display."""
        self.spi = spi
        self.dc = dc
        self.cs = cs
        self.rst = rst
        self.width = width
        self.height = height
        
        # Initialize pins
        self.dc.init(Pin.OUT, value=0)
        self.cs.init(Pin.OUT, value=1)
        if self.rst:
            self.rst.init(Pin.OUT, value=1)
        
        # Pre-allocate buffers for faster rendering
        self.row_buffer_bgr = bytearray(width * 3 + 3)
        self.row_buffer_rgb565 = bytearray(width * 2)
        
        # Reset and initialize display
        self.reset()
        self.init_display()
    
    def reset(self):
        """Hardware reset."""
        if self.rst:
            self.rst.value(1)
            time.sleep_ms(5)
            self.rst.value(0)
            time.sleep_ms(20)
            self.rst.value(1)
            time.sleep_ms(150)
    
    def write_cmd(self, cmd):
        """Write command."""
        self.cs.value(0)
        self.dc.value(0)
        self.spi.write(bytearray([cmd]))
        self.cs.value(1)
    
    def write_data(self, data):
        """Write data."""
        self.cs.value(0)
        self.dc.value(1)
        if isinstance(data, int):
            self.spi.write(bytearray([data]))
        else:
            self.spi.write(data)
        self.cs.value(1)
    
    def init_display(self):
        """Initialize display registers."""
        # Software reset
        self.write_cmd(ILI9341_SWRESET)
        time.sleep_ms(150)
        
        # Sleep out
        self.write_cmd(ILI9341_SLPOUT)
        time.sleep_ms(255)
        
        # Pixel format: 16-bit color
        self.write_cmd(ILI9341_PIXFMT)
        self.write_data(0x55)
        
        # Memory access control (rotation and color order)
        # Bit 7: MY (Row Address Order)
        # Bit 6: MX (Column Address Order)  
        # Bit 5: MV (Row/Column Exchange)
        # Bit 3: BGR (RGB/BGR Order)
        self.write_cmd(ILI9341_MADCTL)
        self.write_data(0x08)  # BGR=1 only (portrait mode, flip horizontal)
        
        # Display on
        self.write_cmd(ILI9341_DISPON)
        time.sleep_ms(100)
    
    def set_window(self, x0, y0, x1, y1):
        """Set address window."""
        # Column address
        self.write_cmd(ILI9341_CASET)
        self.write_data(bytearray([x0 >> 8, x0 & 0xFF, x1 >> 8, x1 & 0xFF]))
        
        # Row address
        self.write_cmd(ILI9341_PASET)
        self.write_data(bytearray([y0 >> 8, y0 & 0xFF, y1 >> 8, y1 & 0xFF]))
        
        # Write to RAM
        self.write_cmd(ILI9341_RAMWR)
    
    def fill(self, color):
        """Fill screen with color (RGB565)."""
        self.set_window(0, 0, self.width - 1, self.height - 1)
        
        # Create color buffer
        chunk_size = 512
        chunk = bytearray(chunk_size)
        color_bytes = bytearray([color >> 8, color & 0xFF])
        
        for i in range(0, chunk_size, 2):
            chunk[i] = color_bytes[0]
            chunk[i + 1] = color_bytes[1]
        
        # Fill screen
        total_pixels = self.width * self.height
        chunks = total_pixels * 2 // chunk_size
        
        self.cs.value(0)
        self.dc.value(1)
        for _ in range(chunks):
            self.spi.write(chunk)
        self.cs.value(1)
    
    def blit_buffer(self, buffer, x, y, width, height):
        """Write buffer to display."""
        self.set_window(x, y, x + width - 1, y + height - 1)
        
        self.cs.value(0)
        self.dc.value(1)
        self.spi.write(buffer)
        self.cs.value(1)
    
    def show_raw(self, filepath, width=None, height=None):
        """Display raw RGB565 file (much faster than BMP)."""
        if width is None:
            width = self.width
        if height is None:
            height = self.height
        
        try:
            # Set display window
            self.set_window(0, 0, width - 1, height - 1)
            
            # Read and display file directly (already in RGB565 format)
            self.cs.value(0)
            self.dc.value(1)
            
            with open(filepath, 'rb') as f:
                # Read in chunks for memory efficiency
                chunk_size = 4096
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    self.spi.write(chunk)
            
            self.cs.value(1)
            return True
            
        except Exception as e:
            print(f"  Error displaying raw: {e}")
            return False
    
    def show_bmp(self, filepath):
        """Display BMP file from SD card."""
        try:
            with open(filepath, 'rb') as f:
                # Read BMP header
                header = f.read(54)
                
                # Check BMP signature
                if header[0:2] != b'BM':
                    print("Not a valid BMP file")
                    return False
                
                # Get image info
                width = int.from_bytes(header[18:22], 'little')
                height = int.from_bytes(header[22:26], 'little')
                bits_per_pixel = int.from_bytes(header[28:30], 'little')
                
                print(f"  BMP: {width}x{height}, {bits_per_pixel}bpp")
                
                # Only support 24-bit BMP
                if bits_per_pixel != 24:
                    print(f"  Unsupported: {bits_per_pixel}bpp (need 24bpp)")
                    return False
                
                # Calculate row size (must be multiple of 4)
                row_size = ((width * 3 + 3) // 4) * 4
                
                # Use pre-allocated buffers
                row_buffer_bgr = self.row_buffer_bgr
                row_buffer_rgb565 = self.row_buffer_rgb565
                
                # Set display window
                self.set_window(0, 0, min(width, self.width) - 1, min(height, self.height) - 1)
                
                self.cs.value(0)
                self.dc.value(1)
                
                # Read and convert each row - optimized version
                for row in range(min(height, self.height)):
                    # Seek to row (BMP is bottom-to-top)
                    f.seek(54 + (height - 1 - row) * row_size)
                    f.readinto(row_buffer_bgr)
                    
                    # Convert BGR888 to BGR565 - optimized loop
                    idx = 0
                    for col in range(min(width, self.width)):
                        # Get BGR values (BMP is already BGR)
                        b = row_buffer_bgr[idx]
                        g = row_buffer_bgr[idx + 1]
                        r = row_buffer_bgr[idx + 2]
                        idx += 3
                        
                        # Convert to BGR565 (keep BGR order for display)
                        bgr565 = ((b & 0xF8) << 8) | ((g & 0xFC) << 3) | (r >> 3)
                        
                        # Store as big-endian
                        col2 = col * 2
                        row_buffer_rgb565[col2] = bgr565 >> 8
                        row_buffer_rgb565[col2 + 1] = bgr565 & 0xFF
                    
                    # Write row to display
                    self.spi.write(row_buffer_rgb565)
                
                self.cs.value(1)
                
                return True
                
        except Exception as e:
            print(f"  Error displaying BMP: {e}")
            return False
