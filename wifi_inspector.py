import subprocess
import scapy.all as scapy

def get_connected_network():
    try:
        result = subprocess.run(['nmcli', 'dev', 'wifi'], capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')
        for line in lines[1:]:  # skip header
            if line.startswith('*'):
                parts = line.split()
                if len(parts) >= 10:
                    ssid = parts[2]
                    bssid = parts[1]
                    security = ' '.join(parts[9:])
                    secure = 'Secure' if 'WPA' in security else 'Not Secure'
                    return {'ssid': ssid, 'bssid': bssid, 'security': security, 'status': secure}
    except Exception as e:
        print(f"Error getting connected network: {e}")
        return None

def get_nearby_networks():
    try:
        result = subprocess.run(['nmcli', 'dev', 'wifi'], capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')
        networks = []
        for line in lines[1:]:  # skip header
            parts = line.split()
            if len(parts) >= 10:
                ssid = parts[2]
                bssid = parts[1]
                signal = parts[7]
                security = ' '.join(parts[9:])
                networks.append({'ssid': ssid, 'bssid': bssid, 'signal': signal, 'security': security})
        return networks
    except Exception as e:
        print(f"Error getting nearby networks: {e}")
        return []

def get_saved_networks():
    try:
        result = subprocess.run(['nmcli', 'connection', 'show'], capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')
        saved = []
        for line in lines[1:]:  # skip header
            parts = line.split()
            if len(parts) >= 3 and parts[2] == 'wifi':
                ssid = parts[0]
                saved.append(ssid)
        return saved
    except Exception as e:
        print(f"Error getting saved networks: {e}")
        return []

def get_network_range():
    try:
        result = subprocess.run(['ip', 'route'], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if 'default' not in line and 'via' not in line and line.strip():
                parts = line.split()
                if len(parts) >= 3:
                    network = parts[0]
                    return network
    except Exception as e:
        print(f"Error getting network range: {e}")
        return None

def scan_devices(network):
    try:
        arp_request = scapy.ARP(pdst=network)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
        devices = []
        for element in answered_list:
            device = {'ip': element[1].psrc, 'mac': element[1].hwsrc}
            devices.append(device)
        return devices
    except Exception as e:
        print(f"Error scanning devices: {e}")
        return []

def main():
    print("WiFi Inspector 📡")
    print("==================")
    connected = get_connected_network()
    if connected:
        print(f"Connected Network: {connected['ssid']}")
        print(f"BSSID: {connected['bssid']}")
        print(f"Security: {connected['security']}")
        print(f"Status: {connected['status']}")
    else:
        print("No connected network found.")

    print("\nNearby Networks:")
    nearby = get_nearby_networks()
    for net in nearby:
        print(f"SSID: {net['ssid']}, Signal: {net['signal']}, Security: {net['security']}")

    print("\nSaved Networks:")
    saved = get_saved_networks()
    for s in saved:
        print(s)

    print("\nDevices on Network (Potential Trackers):")
    network = get_network_range()
    if network:
        devices = scan_devices(network)
        for dev in devices:
            print(f"IP: {dev['ip']}, MAC: {dev['mac']}")
    else:
        print("Could not determine network range.")

if __name__ == "__main__":
    main()