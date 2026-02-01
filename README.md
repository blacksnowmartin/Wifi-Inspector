# Wifi-Inspector 📡

This Python application, "WiFi-Inspector," provides users with information about their connected Wi-Fi network, including SSID, BSSID, and security status. It checks whether the network is secure based on a simplified criterion and displays the result. Use this app to quickly assess the security of your Wi-Fi connection.
And be able to know who is tracking you. And also show networks your device has ever connected to and also current location nearby WiFi networks that it can connect to.

## Features

- **Connected Network Info**: Displays SSID, BSSID, Security type, and security status.
- **Nearby Networks**: Lists available WiFi networks with signal strength and security.
- **Saved Networks**: Shows networks the device has connected to in the past.
- **Devices on Network**: Scans for devices connected to the same network (potential trackers).

## Installation

1. Ensure you have Python 3 installed.
2. Install required dependencies:
   ```bash
   sudo apt update
   sudo apt install python3-scapy
   ```

## Usage

Run the script:
```bash
python3 wifi_inspector.py
```

For scanning devices on the network, you may need to run with sudo:
```bash
sudo python3 wifi_inspector.py
```

## Blacksnowmartin 2023 ©
