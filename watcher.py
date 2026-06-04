import os
import time
import threading
from pathlib import Path
from config import WATCH_FOLDER, BASE_URL
from bot import notify

_seen_files = set()
_active = False


def _get_all_files() -> set:
    """Return set of all files currently in watch folder."""
    folder = Path(WATCH_FOLDER)
    if not folder.exists():
        return set()
    return {str(p.relative_to(folder)) for p in folder.iterdir() if p.is_file()}


def _build_url(filename: str) -> str:
    """Build direct download URL for a file."""
    from urllib.parse import quote
    safe = quote(filename)
    return f"{BASE_URL.rstrip('/')}/files/{safe}"


def scan_once() -> list:
    """Scan folder and return list of new files detected."""
    global _seen_files
    current = _get_all_files()
    new_files = current - _seen_files
    _seen_files = current
    return sorted(new_files)


def notify_new_files() -> list:
    """Detect and notify about new files. Returns list of notified filenames."""
    new_files = scan_once()
    notified = []
    for fname in new_files:
        url = _build_url(fname)
        print(f"[WATCHER] New file: {fname} -> notifying...")
        notify(fname, url)
        notified.append(fname)
    return notified


def start_polling(interval: float = 5.0) -> threading.Thread:
    """Start background polling thread."""
    global _active, _seen_files
    _seen_files = _get_all_files()  # init with current state
    _active = True

    def _loop():
        global _active
        while _active:
            try:
                notify_new_files()
            except Exception as e:
                print(f"[WATCHER] Error: {e}")
            time.sleep(interval)
        print("[WATCHER] Polling stopped.")

    t = threading.Thread(target=_loop, daemon=True, name="watcher")
    t.start()
    print(f"[WATCHER] Polling started every {interval}s in {WATCH_FOLDER}")
    return t


def stop_polling():
    """Stop background polling."""
    global _active
    _active = False
    print("[WATCHER] Stopping...")
