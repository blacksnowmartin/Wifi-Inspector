# WiFi Inspector Application

import scapy.all as scapy
import os

def scan_wifi():
    wifi_list = []
    print("Scanning for WiFi networks...")
    networks = scapy.all.Dot11
    iface = "wlan0"  # Change this to your wireless interface
    scapy.sniff(iface=iface, prn=lambda x: wifi_list.append(x), count=10)
    
    return wifi_list

def display_networks(networks):
    print("Available WiFi Networks:")
    for network in networks:
        ssid = network.info.decode('utf-8') if network.info else "Hidden SSID"
        bssid = network.addr2
        print(f"SSID: {ssid}, BSSID: {bssid}")

if __name__ == "__main__":
    networks = scan_wifi()
    display_networks(networks)
