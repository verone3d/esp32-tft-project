"""
WiFi Test - Scan for networks and show info
"""

import network
import time
import machine

def scan_wifi():
    """Scan for WiFi networks."""
    print("=" * 50)
    print("ESP32 WiFi Scanner")
    print("=" * 50)
    
    # Create WiFi interface
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    
    print("\nScanning for WiFi networks...")
    time.sleep(1)
    
    networks = sta.scan()
    
    print(f"\nFound {len(networks)} networks:\n")
    print(f"{'SSID':<32} {'Signal':<8} {'Channel':<8} {'Security'}")
    print("-" * 70)
    
    for net in networks:
        ssid = net[0].decode('utf-8')
        bssid = ':'.join(['%02X' % b for b in net[1]])
        channel = net[2]
        rssi = net[3]
        authmode = net[4]
        hidden = net[5]
        
        # Convert authmode to string
        auth_str = {
            0: "Open",
            1: "WEP",
            2: "WPA-PSK",
            3: "WPA2-PSK",
            4: "WPA/WPA2-PSK",
            5: "WPA2-Enterprise"
        }.get(authmode, "Unknown")
        
        # Signal strength indicator
        if rssi > -50:
            signal = "Excellent"
        elif rssi > -60:
            signal = "Good"
        elif rssi > -70:
            signal = "Fair"
        else:
            signal = "Weak"
        
        print(f"{ssid:<32} {signal:<8} {channel:<8} {auth_str}")
    
    print("\n" + "=" * 50)
    print("Scan complete!")
    print("=" * 50)
    
    # Show MAC address
    mac = sta.config('mac')
    mac_str = ':'.join(['%02X' % b for b in mac])
    print(f"\nYour ESP32 MAC address: {mac_str}")
    
    sta.active(False)

def main():
    """Main program."""
    scan_wifi()

if __name__ == "__main__":
    main()
