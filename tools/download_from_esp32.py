"""
Download all files from ESP32
Retrieves all files from the ESP32 device
"""

import sys
import subprocess
from pathlib import Path


def run_ampy_command(port, command):
    """Run ampy command and return output."""
    try:
        cmd = ["ampy", "--port", port] + command.split()
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return result.stdout, result.returncode
    except subprocess.TimeoutExpired:
        return None, -1
    except Exception as e:
        print(f"Error: {e}")
        return None, -1


def list_files(port, path="/"):
    """List files on ESP32."""
    output, code = run_ampy_command(port, f"ls {path}")
    if code == 0 and output:
        return [line.strip() for line in output.strip().split('\n') if line.strip()]
    return []


def download_file(port, remote_path, local_path):
    """Download a file from ESP32."""
    print(f"  Downloading: {remote_path}")
    try:
        cmd = ["ampy", "--port", port, "get", remote_path]
        result = subprocess.run(cmd, capture_output=True, timeout=10)
        
        if result.returncode == 0:
            # Create parent directory if needed
            local_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file
            with open(local_path, 'wb') as f:
                f.write(result.stdout)
            
            print(f"    ✓ Saved to: {local_path}")
            return True
        else:
            print(f"    ✗ Failed: {result.stderr.decode()}")
            return False
    except Exception as e:
        print(f"    ✗ Error: {e}")
        return False


def download_all(port, output_dir="downloaded_code"):
    """Download all files from ESP32."""
    print("=" * 70)
    print("ESP32 FILE DOWNLOADER")
    print("=" * 70)
    print(f"Port: {port}")
    print(f"Output: {output_dir}")
    print()
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Common files to try
    common_files = [
        "boot.py",
        "main.py",
        "config.py",
        "wifi_config.py",
    ]
    
    # Common directories
    common_dirs = [
        "/lib",
        "/images",
        "/data",
    ]
    
    downloaded = 0
    failed = 0
    
    # Try to download common files
    print("Downloading common files...")
    for filename in common_files:
        local_file = output_path / filename
        if download_file(port, filename, local_file):
            downloaded += 1
        else:
            failed += 1
    
    # Try to list and download from root
    print("\nScanning root directory...")
    files = list_files(port, "/")
    for file in files:
        if file not in common_files and not file.startswith('/'):
            local_file = output_path / file
            if download_file(port, file, local_file):
                downloaded += 1
            else:
                failed += 1
    
    # Try common directories
    for dir_path in common_dirs:
        print(f"\nScanning {dir_path}...")
        files = list_files(port, dir_path)
        for file in files:
            remote_path = f"{dir_path}/{file}"
            local_file = output_path / dir_path.strip('/') / file
            if download_file(port, remote_path, local_file):
                downloaded += 1
            else:
                failed += 1
    
    # Summary
    print()
    print("=" * 70)
    print("DOWNLOAD COMPLETE")
    print("=" * 70)
    print(f"Downloaded: {downloaded} files")
    print(f"Failed:     {failed} files")
    print(f"Location:   {output_path.absolute()}")
    print()


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("ESP32 File Downloader")
        print()
        print("Usage: python download_from_esp32.py <COM_PORT> [output_dir]")
        print()
        print("Examples:")
        print("  python download_from_esp32.py COM3")
        print("  python download_from_esp32.py COM3 my_backup")
        print()
        print("This will download all files from your ESP32 to the specified directory.")
        sys.exit(1)
    
    port = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "downloaded_code"
    
    # Check if ampy is installed
    try:
        subprocess.run(["ampy", "--help"], capture_output=True)
    except FileNotFoundError:
        print("Error: ampy not found")
        print("Install with: pip install adafruit-ampy")
        sys.exit(1)
    
    download_all(port, output_dir)


if __name__ == "__main__":
    main()
