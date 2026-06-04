import asyncio
import aiohttp
from config import BOT_TOKEN, IGOR_CHAT_ID

async def send_telegram(filename: str, file_url: str) -> bool:
    """Send notification to Igor via Telegram. Returns True on success."""
    if not BOT_TOKEN or not IGOR_CHAT_ID:
        print("[BOT] Missing BOT_TOKEN or IGOR_CHAT_ID")
        return False

    message = (
        f"\U0001f4e6 <b>Новая спецификация на закупку</b>\n\n"
        f"\U0001f4c4 Файл: <code>{filename}</code>\n"
        f"\U0001f517 <a href='{file_url}'>Открыть спецификацию</a>\n\n"
        f"\u23f3 Игорь, приступай к закупке."
    )

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": IGOR_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                data = await resp.json()
                if data.get("ok"):
                    print(f"[BOT] Notification sent for {filename}")
                    return True
                else:
                    print(f"[BOT] API error: {data}")
                    return False
    except Exception as e:
        print(f"[BOT] Error: {e}")
        return False


def notify(filename: str, file_url: str) -> None:
    """Synchronous wrapper for async send."""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(send_telegram(filename, file_url))
        loop.close()
    except Exception as e:
        print(f"[BOT] Loop error: {e}")
