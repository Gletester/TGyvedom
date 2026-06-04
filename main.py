#!/usr/bin/env python3
"""
Spec Watcher Bot — entry point.
Уведомление комплектатора о новой спецификации в Telegram.
"""
from app import app
from config import PORT

if __name__ == "__main__":
    from watcher import start_polling
    start_polling(interval=10.0)
    app.run(host="0.0.0.0", port=PORT, debug=False)
else:
    # When running via gunicorn, start watcher on import
    from watcher import start_polling
    import threading
    t = threading.Thread(target=lambda: start_polling(interval=10.0), daemon=True)
    t.start()
