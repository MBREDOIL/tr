from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN, DB_NAME
from main import register_handlers, init_db
import asyncio
import subprocess
from threading import Thread

class TrackBot(Client):
    def __init__(self):
        super().__init__("tracker_bot", API_ID, API_HASH, bot_token=BOT_TOKEN)
        self.scheduler = None

    async def start(self):
        await super().start()
        await init_db()
        await register_handlers(self)
        print("Bot started!")
        self.scheduler = asyncio.create_task(self.url_checker())

    async def stop(self):
        self.scheduler.cancel()
        await super().stop()

    async def url_checker(self):
        while True:
            await asyncio.sleep(CHECK_INTERVAL)
            # Add your URL checking logic here

def run_gunicorn():
    subprocess.run(["gunicorn", "bot:TrackBot", "--bind", "0.0.0.0:8000", "--worker-class", "aiohttp.GunicornWebWorker"])

if __name__ == "__main__":
    bot = TrackBot()
    Thread(target=run_gunicorn).start()
    bot.run()
