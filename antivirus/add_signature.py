import json
import hashlib
import argparse
import os

DB_FILE = "signatures.json"

def get_file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(4096):
            h.update(chunk)
    return h.hexdigest()

def add_signature(file_path, name):
    db = {}
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            db = json.load(f)

    sha = get_file_hash(file_path)
    db[sha] = {"name": name}

    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(db, f, indent=2)

    print(f"Added signature: {name} {sha}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--file", "-f", required=True, help="File to add to DB")
    p.add_argument("--name", "-n", required=True, help="Malware family name")
    args = p.parse_args()
    add_signature(args.file, args.name)
