import asyncio
import os
import uvicorn
from bot import dp, bot

# ඔයාගේ API/Dashboard file එකේ නම app.py නම් 'from app import app as web_app' ලෙස තියෙන්න දෙන්න.
# වෙන නමක් නම් (උදා: dashboard.py) 'from dashboard import app as web_app' ලෙස මාරු කරන්න.
try:
    from app import app as web_app
except ImportError:
    from api import app as web_app

async def start_bot():
    print("🤖 Telegram Bot එක Start වෙනවා...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(start_bot())
    
    # Server එකෙන් දෙන PORT එක ලබාගැනීම
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 Dashboard Server එක Port {port} එකේ Run වෙනවා...")
    uvicorn.run(web_app, host="0.0.0.0", port=port)