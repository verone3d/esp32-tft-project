"""
Image Converter for ESP32 TFT Display
Converts images to RGB565 raw format for display
"""

import sys
from pathlib import Path
from PIL import Image


def rgb888_to_rgb565(r, g, b):
    """Convert RGB888 to RGB565 format."""
    r5 = (r >> 3) & 0x1F
    g6 = (g >> 2) & 0x3F
    b5 = (b >> 3) & 0x1F
    return (r5 << 11) | (g6 << 5) | b5


def convert_image_to_rgb565(input_path, output_path, width=240, height=320):
    """
    Convert image to RGB565 raw format.
    
    Args:
        input_path: Input image file
        output_path: Output raw file
        width: Target width (default 240)
        height: Target height (default 320)
    """
    print(f"Converting {input_path}...")
    
    # Open and resize image
    img = Image.open(input_path)
    img = img.convert('RGB')
    img = img.resize((width, height), Image.Resampling.LANCZOS)
    
    # Convert to RGB565
    pixels = img.load()
    data = bytearray()
    
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            rgb565 = rgb888_to_rgb565(r, g, b)
            # Big-endian format
            data.append((rgb565 >> 8) & 0xFF)
            data.append(rgb565 & 0xFF)
    
    # Write to file
    with open(output_path, 'wb') as f:
        f.write(data)
    
    print(f"Converted! Output: {output_path}")
    print(f"Size: {len(data)} bytes ({width}x{height})")


def main():
    """Main function."""
    if len(sys.argv) < 3:
        print("Usage: python image_converter.py input.jpg output.raw [width] [height]")
        print("\nExamples:")
        print("  python image_converter.py photo.jpg photo.raw")
        print("  python image_converter.py photo.jpg photo.raw 240 320")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    width = int(sys.argv[3]) if len(sys.argv) > 3 else 240
    height = int(sys.argv[4]) if len(sys.argv) > 4 else 320
    
    if not Path(input_path).exists():
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)
    
    convert_image_to_rgb565(input_path, output_path, width, height)


if __name__ == "__main__":
    main()
