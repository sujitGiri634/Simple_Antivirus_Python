import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import threading

def scan_folder():
    folder = filedialog.askdirectory()
    if folder:
        subprocess.run(["python", "folder_scanner.py", "--scan", folder])

def start_monitor():
    def run_monitor():
        subprocess.run(["python", "realtime_monitor.py"])
    threading.Thread(target=run_monitor, daemon=True).start() 
    messagebox.showinfo("Monitor", "Starting real-time monitor...")
    

root = tk.Tk()
root.title("Simple Antivirus")

tk.Button(root, text="Full Scan", command=scan_folder).pack(pady=10)
tk.Button(root, text="Start Monitor", command=start_monitor).pack(pady=10)
tk.Button(root, text="Exit", command=root.quit).pack(pady=10)

root.mainloop()
