from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN, DB_NAME
import aiosqlite
import asyncio
import subprocess
from threading import Thread

class TrackBot(Client):
    def __init__(self):
        super().__init__("tracker_bot", API_ID, API_HASH, bot_token=BOT_TOKEN)
        self.scheduler = None

    async def start(self):
        await super().start()
        await self.init_db()
        await self.register_handlers()
        print("Bot started!")
        self.scheduler = asyncio.create_task(self.url_checker())

    async def stop(self):
        self.scheduler.cancel()
        await super().stop()

    async def url_checker(self):
        while True:
            await asyncio.sleep(CHECK_INTERVAL)
            # Add your URL checking logic here

    async def init_db(self):
        async with aiosqlite.connect(DB_NAME) as db:
            await db.execute('''CREATE TABLE IF NOT EXISTS trackers(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                interval INTEGER,
                last_hash TEXT,
                next_check DATETIME,
                status TEXT DEFAULT 'active')''')
            await db.execute('''CREATE TABLE IF NOT EXISTS admins(
                user_id INTEGER PRIMARY KEY,
                added_by INTEGER,
                added_at DATETIME DEFAULT CURRENT_TIMESTAMP)''')
            await db.commit()

    async def register_handlers(self):
        from main import register_handlers
        await register_handlers(self)

def run_gunicorn():
    subprocess.run(["gunicorn", "bot:TrackBot", "--bind", "0.0.0.0:8000", "--worker-class", "aiohttp.GunicornWebWorker"])

if __name__ == "__main__":
    bot = TrackBot()
    Thread(target=run_gunicorn).start()
    bot.run()
