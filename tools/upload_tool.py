"""
Upload Tool for ESP32
Upload files to ESP32 via serial connection
"""

import sys
import subprocess
from pathlib import Path


def upload_file(file_path, port="COM3", target_path=None):
    """
    Upload file to ESP32 using ampy.
    
    Args:
        file_path: Local file to upload
        port: Serial port (default COM3)
        target_path: Target path on ESP32 (default: same filename)
    """
    if not Path(file_path).exists():
        print(f"Error: File not found: {file_path}")
        return False
    
    if target_path is None:
        target_path = Path(file_path).name
    
    print(f"Uploading {file_path} to ESP32...")
    print(f"Port: {port}")
    print(f"Target: {target_path}")
    
    try:
        cmd = ["ampy", "--port", port, "put", file_path, target_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("Upload successful!")
            return True
        else:
            print(f"Upload failed: {result.stderr}")
            return False
    except FileNotFoundError:
        print("Error: ampy not found. Install with: pip install adafruit-ampy")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False


def list_files(port="COM3"):
    """List files on ESP32."""
    print(f"Listing files on ESP32 (port {port})...")
    try:
        cmd = ["ampy", "--port", port, "ls"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
    except Exception as e:
        print(f"Error: {e}")


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Upload file:  python upload_tool.py file.py [port] [target_path]")
        print("  List files:   python upload_tool.py --list [port]")
        print("\nExamples:")
        print("  python upload_tool.py main.py")
        print("  python upload_tool.py main.py COM3")
        print("  python upload_tool.py image.raw COM3 /images/photo.raw")
        print("  python upload_tool.py --list COM3")
        sys.exit(1)
    
    if sys.argv[1] == "--list":
        port = sys.argv[2] if len(sys.argv) > 2 else "COM3"
        list_files(port)
    else:
        file_path = sys.argv[1]
        port = sys.argv[2] if len(sys.argv) > 2 else "COM3"
        target_path = sys.argv[3] if len(sys.argv) > 3 else None
        upload_file(file_path, port, target_path)


if __name__ == "__main__":
    main()
