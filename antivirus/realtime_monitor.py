import hashlib
import json
import pathlib
import time
import os
import argparse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from logger_utils import append_log

DB_FILE = "signatures.json"
STABILITY_CHECKS = 3
STABILITY_INTERVAL = 0.5
MAX_WORKERS = 4
LOG_FILE = "realtime_log.txt"

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def load_db():
    try:
        return json.loads(pathlib.Path(DB_FILE).read_text())
    except FileNotFoundError:
        return {}

def get_file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(4096):
            h.update(chunk)
    return h.hexdigest()

def is_file_stable(path, checks=STABILITY_CHECKS, interval=STABILITY_INTERVAL):
    try:
        last = os.path.getsize(path)
    except Exception:
        return False
    for _ in range(checks):
        time.sleep(interval)
        try:
            cur = os.path.getsize(path)
        except Exception:
            return False
        if cur != last:
            last = cur
            continue
    return True

class MonitorHandler(FileSystemEventHandler):
    def __init__(self, db, executor):
        super().__init__()
        self.db = db
        self.executor = executor
        self.recent = {}
        self.recent_ttl = 5.0

    def _schedule_check(self, path, action):
        if os.path.basename(path) == "realtime_log.txt":
            return  # 🚫 Ignore changes to log file itself

        t = time.time()
        last = self.recent.get(path, 0)
        if t - last < self.recent_ttl:
            return
        self.recent[path] = t
        self.executor.submit(self._check_file, path, action)

    def on_created(self, event):
        if event.is_directory:
            return
        if os.path.basename(event.src_path) == LOG_FILE:
            return    
        append_log(LOG_FILE, f"created {event.src_path}")
        print(f"[{now()}] created {event.src_path}")
        self._schedule_check(event.src_path, "created")

    def on_modified(self, event):
        if event.is_directory:
            return
        if os.path.basename(event.src_path) == LOG_FILE:
            return
        append_log(LOG_FILE, f"modified {event.src_path}")
        print(f"[{now()}] modified {event.src_path}")
        self._schedule_check(event.src_path, "modified")

    def on_moved(self, event):
        if event.is_directory:
            return
        if os.path.basename(event.dest_path) == LOG_FILE:
            return
        append_log(LOG_FILE, f"moved {event.dest_path}")
        print(f"[{now()}] moved {event.dest_path}")
        self._schedule_check(event.dest_path, "moved")

    def on_deleted(self, event):
        if event.is_directory:
            return
        if os.path.basename(event.src_path) == LOG_FILE:
            return
        append_log(LOG_FILE, f"deleted {event.src_path}")
        print(f"[{now()}] deleted {event.src_path}")

    def _check_file(self, path, action):
        try:
            if not os.path.isfile(path):
                return

            stable = is_file_stable(path)
            if not stable:
                return

            sha = get_file_hash(path)
            if sha in self.db:
                meta = self.db[sha]
                name = meta.get("name", "unknown")
                msg = f"[ALERT] {action.upper()} infected file: {path} [{name}] {sha}"
                print(f"[{now()}] {msg}")
                append_log(LOG_FILE, msg)
        except Exception as e:
            append_log(LOG_FILE, f"Error checking {path}: {e}")

def main(path_to_watch):
    db = load_db()
    print(f"[{now()}] Loaded {len(db)} signatures")
    append_log(LOG_FILE, f"monitor started on {os.path.abspath(path_to_watch)}")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        event_handler = MonitorHandler(db, executor)
        observer = Observer()
        observer.schedule(event_handler, path=path_to_watch, recursive=True)
        observer.start()
        print(f"[{now()}] Monitoring {os.path.abspath(path_to_watch)} (Ctrl+C to stop)")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print(f"[{now()}] Stopping monitor...")
            observer.stop()
        observer.join()
    append_log(LOG_FILE, "monitor stopped")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--path", "-p", default=".", help="Folder to monitor")
    args = p.parse_args()
    main(args.path)
