from pyrogram import filters, types
from config import OWNER_ID, DB_NAME, MAX_TRACKERS, URL_REGEX
import aiosqlite
import re
import hashlib
import difflib
from datetime import datetime, timedelta

# Inline Keyboards
def main_menu():
    return types.InlineKeyboardMarkup([
        [types.InlineKeyboardButton("➕ Add Tracker", callback_data="add_tracker"),
         types.InlineKeyboardButton("📋 My Trackers", callback_data="list_trackers")],
        [types.InlineKeyboardButton("⚙️ Settings", callback_data="settings"),
         types.InlineKeyboardButton("❓ Help", callback_data="help")]
    ])

async def register_handlers(client):
    # Owner Commands
    @client.on_message(filters.command("addadmin") & filters.user(OWNER_ID))
    async def add_admin(client, message):
        try:
            target = message.command[1]
            if target.startswith("@"):
                user = await client.get_users(target[1:])
                user_id = user.id
            else:
                user_id = int(target)

            async with aiosqlite.connect(DB_NAME) as db:
                await db.execute('INSERT OR IGNORE INTO admins VALUES (?,?,?)', 
                               (user_id, message.from_user.id, datetime.now()))
                await db.commit()
            await message.reply(f"✅ Admin added: {user_id}")
        except Exception as e:
            await message.reply(f"❌ Error: {str(e)}")

    # Tracking Commands
    @client.on_message(filters.command("track"))
    async def add_tracker(client, message):
        if len(message.command) < 2:
            return await message.reply("Usage: /track <url> [interval]")
        
        url = message.command[1]
        if not re.match(URL_REGEX, url):
            return await message.reply("❌ Invalid URL format!")
        
        interval = int(message.command[2]) if len(message.command) > 2 else CHECK_INTERVAL

        async with aiosqlite.connect(DB_NAME) as db:
            # Check tracker limit
            cursor = await db.execute('SELECT COUNT(*) FROM trackers WHERE user_id=?', (message.from_user.id,))
            count = (await cursor.fetchone())[0]
            if count >= MAX_TRACKERS:
                return await message.reply(f"❌ Tracker limit reached ({MAX_TRACKERS})")

            await db.execute('''INSERT INTO trackers 
                             (url, user_id, interval, next_check)
                             VALUES (?,?,?,?)''',
                             (url, message.from_user.id, interval, datetime.now()))
            await db.commit()
        
        await message.reply(f"✅ Tracking started for:\n{url}\nCheck interval: {interval}s")

    # Help Command with Inline Keyboard
    @client.on_message(filters.command("help"))
    async def help_command(client, message):
        help_text = """
        🌐 **Web Tracker Bot Help**

        **Basic Commands:**
        /start - Show main menu
        /help - Display this message

        **Admin Commands:**
        /track <url> [interval] - Start tracking
        /stats - Show tracking statistics
        """
        await message.reply(help_text, reply_markup=main_menu())

    # Inline Callbacks
    @client.on_callback_query()
    async def handle_callbacks(client, callback):
        if callback.data == "add_tracker":
            await callback.message.edit_text("Send URL to track:", reply_markup=main_menu())
        # Add more callback handlers
