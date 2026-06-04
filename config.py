import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
IGOR_CHAT_ID = os.getenv("IGOR_CHAT_ID", "")
WATCH_FOLDER = os.getenv("WATCH_FOLDER", "./uploads")
BASE_URL = os.getenv("BASE_URL", "http://localhost:8080")
PORT = int(os.getenv("PORT", 8080))

# Ensure watch folder exists
os.makedirs(WATCH_FOLDER, exist_ok=True)
