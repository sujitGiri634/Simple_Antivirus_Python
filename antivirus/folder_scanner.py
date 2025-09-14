import os
import hashlib
import argparse
import json
from logger_utils import append_log

DB_FILE = "signatures.json"

def get_file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(4096):
            h.update(chunk)
    return h.hexdigest()

def load_db():
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def scan_folder(folder):
    db = load_db()
    infected = []
    total = 0

    for root, _, files in os.walk(folder):
        for name in files:
            path = os.path.join(root, name)
            try:
                sha = get_file_hash(path)
                total += 1
                if sha in db:
                    infected.append((path, db[sha]["name"]))
                    append_log("scan_log.txt", f"[ALERT] Infected file: {path} [{db[sha]['name']}]")
            except Exception as e:
                append_log("scan_log.txt", f"Error scanning {path}: {e}")

    append_log("scan_log.txt", f"Scanned {total} files, {len(infected)} infected")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--scan", "-s", required=True, help="Folder to scan")
    args = p.parse_args()
    scan_folder(args.scan)
