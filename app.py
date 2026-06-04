import os
import atexit
from flask import Flask, request, render_template, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from config import WATCH_FOLDER, BASE_URL, PORT
from bot import notify
from watcher import start_polling, stop_polling

app = Flask(__name__)
app.secret_key = os.urandom(24).hex()
app.config["MAX_CONTENT_LENGTH"] = 200 * 1024 * 1024  # 200 MB
app.config["UPLOAD_FOLDER"] = os.path.abspath(WATCH_FOLDER)
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# ── Background watcher ──────────────────────────────────────────────────
_watcher_thread = None

def _start_watcher():
    global _watcher_thread
    _watcher_thread = start_polling(interval=10.0)

atexit.register(stop_polling)

# ── Routes ──────────────────────────────────────────────────────────────

@app.route("/")
def index():
    """Upload page."""
    files = []
    for f in sorted(os.listdir(app.config["UPLOAD_FOLDER"])):
        fpath = os.path.join(app.config["UPLOAD_FOLDER"], f)
        if os.path.isfile(fpath):
            size = os.path.getsize(fpath)
            files.append({"name": f, "size": _fmt_size(size)})
    return render_template("index.html", files=files, base_url=BASE_URL.rstrip("/"))


@app.route("/upload", methods=["POST"])
def upload_file():
    """Handle file upload from Андрей."""
    if "file" not in request.files:
        flash("Файл не выбран", "error")
        return redirect(url_for("index"))

    f = request.files["file"]
    if f.filename == "":
        flash("Файл не выбран", "error")
        return redirect(url_for("index"))

    filename = secure_filename(f.filename)
    if not filename:
        flash("Недопустимое имя файла", "error")
        return redirect(url_for("index"))

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    # Save file
    f.save(filepath)
    print(f"[APP] Saved: {filename} ({os.path.getsize(filepath)} bytes)")

    # Notify Igor via Telegram
    file_url = f"{BASE_URL.rstrip('/')}/files/{filename}"
    notify(filename, file_url)

    flash(f"Спецификация «{filename}» загружена, Игорь оповещён.", "success")
    return redirect(url_for("index"))


@app.route("/files/<path:filename>")
def download_file(filename):
    """Serve uploaded files."""
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=False)


# ── Health / Info ───────────────────────────────────────────────────────

@app.route("/health")
def health():
    return {"status": "ok", "files": len(os.listdir(app.config["UPLOAD_FOLDER"]))}


# ── Helpers ─────────────────────────────────────────────────────────────

def _fmt_size(bytes_: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if bytes_ < 1024:
            return f"{bytes_:.1f} {unit}"
        bytes_ /= 1024
    return f"{bytes_:.1f} TB"


# ── Entry ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    _start_watcher()
    app.run(host="0.0.0.0", port=PORT, debug=False)
