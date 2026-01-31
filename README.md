# Wifi-Inspector 📡

This Python application, "WiFi-Inspector," provides users with information about their connected Wi-Fi network, including SSID, BSSID, and security status. It checks whether the network is secure based on a simplified criterion and displays the result. Use this app to quickly assess the security of your Wi-Fi connection.
And be able to know who is tracking you. And also show networks your device has ever connected to and also current location nearby WiFi networks that it can connect to.

## Features

- **Connected Network Info**: Displays SSID, BSSID, Security type, and security status.
- **Nearby Networks**: Lists available WiFi networks with signal strength and security.
- **Saved Networks**: Shows networks the device has connected to in the past.
- **Devices on Network**: Scans for devices connected to the same network (potential trackers).

## Installation

1. Install Python 3.x if not already installed.

2. Install the necessary libraries:

   ```bash
   pip install -r requirements.txt
   ```

   Note: Scapy may require root privileges for some operations.

3. Run the application:

   ```bash
   sudo python main.py
   ```

   (sudo may be needed for network scanning)

## Usage

- Launch the app and navigate through the tabs.
- Click "Refresh" on each tab to update the information.
- For "Devices on Network", it performs an ARP scan to find connected devices.

## Blacksnowmartin 2023 ©
