"""
Convert BMP images to raw RGB565 format for faster loading
This pre-converts the images so the ESP32 doesn't have to do it
"""

import sys
import os
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Error: Pillow not installed")
    print("Run: pip install Pillow")
    sys.exit(1)


def bmp_to_rgb565(input_path, output_path):
    """Convert BMP to raw RGB565 format."""
    print(f"Converting: {input_path}")
    
    # Open image
    img = Image.open(input_path)
    
    # Convert to RGB if needed
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    width, height = img.size
    print(f"  Size: {width}x{height}")
    
    # Get pixel data
    pixels = img.load()
    
    # Create RGB565 data
    data = bytearray()
    
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            
            # Convert to BGR565 (display uses BGR mode)
            bgr565 = ((b & 0xF8) << 8) | ((g & 0xFC) << 3) | (r >> 3)
            
            # Store as big-endian
            data.append(bgr565 >> 8)
            data.append(bgr565 & 0xFF)
    
    # Write to file
    with open(output_path, 'wb') as f:
        f.write(data)
    
    original_size = os.path.getsize(input_path)
    new_size = len(data)
    
    print(f"  Original: {original_size:,} bytes")
    print(f"  RGB565:   {new_size:,} bytes")
    print(f"  Saved to: {output_path}")
    print()


def convert_directory(input_dir, output_dir):
    """Convert all BMP files in directory."""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    # Create output directory
    output_path.mkdir(exist_ok=True)
    
    # Find all BMP files
    bmp_files = list(input_path.glob('*.bmp')) + list(input_path.glob('*.BMP'))
    
    if not bmp_files:
        print(f"No BMP files found in {input_dir}")
        return
    
    print(f"Found {len(bmp_files)} BMP files")
    print("=" * 60)
    print()
    
    for bmp_file in bmp_files:
        output_file = output_path / (bmp_file.stem + '.raw')
        try:
            bmp_to_rgb565(str(bmp_file), str(output_file))
        except Exception as e:
            print(f"  Error: {e}")
            print()
    
    print("=" * 60)
    print(f"Conversion complete! {len(bmp_files)} files converted")
    print(f"Output directory: {output_path.absolute()}")


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("BMP to RGB565 Converter")
        print()
        print("Usage:")
        print("  python convert_images_fast.py <input_directory> [output_directory]")
        print()
        print("Examples:")
        print("  python convert_images_fast.py C:\\images")
        print("  python convert_images_fast.py C:\\images C:\\images_fast")
        print()
        print("This converts BMP files to raw RGB565 format for faster loading.")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else input_dir + "_fast"
    
    if not os.path.exists(input_dir):
        print(f"Error: Directory not found: {input_dir}")
        sys.exit(1)
    
    convert_directory(input_dir, output_dir)


if __name__ == "__main__":
    main()
