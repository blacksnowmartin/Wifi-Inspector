# WiFi Inspector Application

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import socket
from scapy.all import ARP, Ether, srp

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "192.168.1.100"  # fallback

def get_connected_wifi():
    try:
        result = subprocess.run(['nmcli', '-t', '-f', 'active,ssid,bssid,security', 'device', 'wifi'], capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')
        for line in lines:
            if line.startswith('yes:'):
                parts = line.split(':')
                ssid = parts[1] if len(parts) > 1 else ""
                bssid = parts[2] if len(parts) > 2 else ""
                security = parts[3] if len(parts) > 3 else ""
                secure = "Secure" if security in ["WPA2", "WPA3"] else "Not Secure"
                return ssid, bssid, security, secure
        return "Not connected", "", "", "N/A"
    except Exception as e:
        return "Error", "", "", str(e)

def scan_nearby_wifi():
    try:
        result = subprocess.run(['nmcli', '-t', '-f', 'ssid,bssid,signal,security', 'device', 'wifi', 'list'], capture_output=True, text=True)
        networks = []
        for line in result.stdout.strip().split('\n'):
            if line:
                parts = line.split(':')
                if len(parts) >= 4:
                    ssid = parts[0]
                    bssid = parts[1]
                    signal = parts[2]
                    security = parts[3]
                    secure = "Secure" if security in ["WPA2", "WPA3"] else "Not Secure"
                    networks.append({'ssid': ssid, 'bssid': bssid, 'signal': signal, 'security': security, 'secure': secure})
        return networks
    except Exception as e:
        return []

def get_saved_networks():
    try:
        result = subprocess.run(['nmcli', '-t', '-f', 'name,type', 'connection'], capture_output=True, text=True)
        saved = []
        for line in result.stdout.strip().split('\n'):
            if ':wifi' in line:
                name = line.split(':')[0]
                saved.append(name)
        return saved
    except Exception as e:
        return []

def scan_devices_on_network():
    try:
        ip = get_local_ip()
        ip_range = ip.rsplit('.', 1)[0] + '.0/24'
        arp = ARP(pdst=ip_range)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether / arp
        result = srp(packet, timeout=3, verbose=0)[0]
        devices = []
        for sent, received in result:
            devices.append({'ip': received.psrc, 'mac': received.hwsrc})
        return devices
    except Exception as e:
        return []

class WifiInspectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WiFi Inspector")
        self.root.geometry("800x600")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)

        self.connected_frame = ttk.Frame(self.notebook)
        self.nearby_frame = ttk.Frame(self.notebook)
        self.saved_frame = ttk.Frame(self.notebook)
        self.devices_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.connected_frame, text='Connected Network')
        self.notebook.add(self.nearby_frame, text='Nearby Networks')
        self.notebook.add(self.saved_frame, text='Saved Networks')
        self.notebook.add(self.devices_frame, text='Devices on Network')

        self.setup_connected_tab()
        self.setup_nearby_tab()
        self.setup_saved_tab()
        self.setup_devices_tab()

        self.refresh_all()

    def setup_connected_tab(self):
        self.connected_tree = ttk.Treeview(self.connected_frame, columns=('Value',), show='headings')
        self.connected_tree.heading('Value', text='Value')
        self.connected_tree.pack(fill='both', expand=True)

        ttk.Button(self.connected_frame, text="Refresh", command=self.refresh_connected).pack()

    def setup_nearby_tab(self):
        self.nearby_tree = ttk.Treeview(self.nearby_frame, columns=('SSID', 'BSSID', 'Signal', 'Security', 'Secure'), show='headings')
        self.nearby_tree.heading('SSID', text='SSID')
        self.nearby_tree.heading('BSSID', text='BSSID')
        self.nearby_tree.heading('Signal', text='Signal')
        self.nearby_tree.heading('Security', text='Security')
        self.nearby_tree.heading('Secure', text='Secure')
        self.nearby_tree.pack(fill='both', expand=True)

        ttk.Button(self.nearby_frame, text="Refresh", command=self.refresh_nearby).pack()

    def setup_saved_tab(self):
        self.saved_listbox = tk.Listbox(self.saved_frame)
        self.saved_listbox.pack(fill='both', expand=True)

        ttk.Button(self.saved_frame, text="Refresh", command=self.refresh_saved).pack()

    def setup_devices_tab(self):
        self.devices_tree = ttk.Treeview(self.devices_frame, columns=('IP', 'MAC'), show='headings')
        self.devices_tree.heading('IP', text='IP Address')
        self.devices_tree.heading('MAC', text='MAC Address')
        self.devices_tree.pack(fill='both', expand=True)

        ttk.Button(self.devices_frame, text="Refresh", command=self.refresh_devices).pack()

    def refresh_connected(self):
        for item in self.connected_tree.get_children():
            self.connected_tree.delete(item)
        ssid, bssid, security, secure = get_connected_wifi()
        self.connected_tree.insert('', 'end', values=(f"SSID: {ssid}",))
        self.connected_tree.insert('', 'end', values=(f"BSSID: {bssid}",))
        self.connected_tree.insert('', 'end', values=(f"Security: {security}",))
        self.connected_tree.insert('', 'end', values=(f"Status: {secure}",))

    def refresh_nearby(self):
        for item in self.nearby_tree.get_children():
            self.nearby_tree.delete(item)
        networks = scan_nearby_wifi()
        for net in networks:
            self.nearby_tree.insert('', 'end', values=(net['ssid'], net['bssid'], net['signal'], net['security'], net['secure']))

    def refresh_saved(self):
        self.saved_listbox.delete(0, tk.END)
        saved = get_saved_networks()
        for net in saved:
            self.saved_listbox.insert(tk.END, net)

    def refresh_devices(self):
        for item in self.devices_tree.get_children():
            self.devices_tree.delete(item)
        devices = scan_devices_on_network()
        for dev in devices:
            self.devices_tree.insert('', 'end', values=(dev['ip'], dev['mac']))

    def refresh_all(self):
        self.refresh_connected()
        self.refresh_nearby()
        self.refresh_saved()
        self.refresh_devices()

if __name__ == "__main__":
    root = tk.Tk()
    app = WifiInspectorApp(root)
    root.mainloop()
