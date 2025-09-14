# Simple_Antivirus_Python

A simple antivirus tool built in Python as a **learning project**.
It supports **signature-based scanning** and **real-time file monitoring** with a CLI/GUI interface.

---

## ✨ Features

✅ **Signature-based detection** (SHA-256 hash comparison)
✅ **On-demand folder scan** (scans all files in a directory)
✅ **Real-time monitoring** (detects created, modified, moved, deleted files)
✅ **Logging system** (records scan results and file activity into `logs/`)
✅ **Add signatures manually** (via `add_signature.py`)
✅ **GUI with Tkinter** (simple buttons for scan & monitor)
✅ **Packaged executable** (via PyInstaller)

---

## 📂 Project Structure

```
📁 SimpleAntivirus
│── antivirus.py          # Main menu + GUI
│── folder_scanner.py     # On-demand folder scanner
│── realtime_monitor.py   # Real-time monitoring
│── add_signature.py      # Add malware signatures
│── logger_utils.py       # Central logging utility
│── signatures.json       # Database of known malware hashes
│── logs/                 # Folder for all logs
│── README.md             # Project documentation
```

---

## ⚙️ Installation

1. Clone this repository:

```bash
git clone https://github.com/<your-username>/simple-antivirus.git
cd simple-antivirus
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:

```
watchdog
tkinter
```

*(Tkinter usually comes pre-installed with Python)*

---

## ▶️ Usage

### 1. Add a new malware signature

```bash
python add_signature.py --file test_malware.exe --name "Test Malware"
```

### 2. Run the antivirus (CLI/GUI)

```bash
python antivirus.py
```

Options:

* Full Scan → Scan a selected folder
* Real-time Monitor → Start live monitoring of changes
* Exit → Close the app

### 3. Run standalone `.exe` (after packaging)

```bash
dist/antivirus.exe
```

---

## 📦 Packaging

Use **PyInstaller** to package the antivirus into a single executable:

```bash
pyinstaller --onefile antivirus.py
```

Executable will appear in `dist/`.

---

## 📜 Logs

All logs are stored in `logs/` with timestamped filenames.
Example entry in `realtime_log.txt`:

```
[2025-09-14 12:10:22] created D:\test\sample.exe
[2025-09-14 12:10:24] [ALERT] MODIFIED infected file: D:\test\malware.exe [Test Malware] <sha256>
```

---

## 🧠 Learning Roadmap (Weeks)

* **Week 1** → Hashing + signatures
* **Week 2** → On-demand scanning
* **Week 3** → Real-time monitoring
* **Week 4** → User interface + packaging

---

## Database

It does not contain SHA256 hash vale for all malware. This is onl for college project.

## ⚠️ Disclaimer

This project is **for educational purposes only**.
It is **NOT** a replacement for professional antivirus software.
Use responsibly and do not rely on it for real-world protection.

---


