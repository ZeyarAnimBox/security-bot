import os
import asyncio
from telethon import TelegramClient, events, types
from aiohttp import web

# --- Settings ---
API_ID = 39181090
API_HASH = '956b15e38aa400de2451cb85a67194f7'
BOT_TOKEN = '8633754548:AAGRZFhzVz7QswvwZg4mafyRyNyPtdJFM3I'
CHANNEL_ID = -1002178787818

client = TelegramClient('security_bot', API_ID, API_HASH)

# --- Render Port Binding Fix (Web Server) ---
async def handle(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    # Render ကပေးတဲ့ PORT ကိုသုံးမယ်၊ မရှိရင် 10000 ကိုသုံးမယ်
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Web server started on port {port}")

# --- Start Command ---
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond('မင်္ဂလာပါ Zeyar! Bot က အဆင်ပြေပြေ အလုပ်လုပ်နေပါပြီခင်ဗျာ။')

# --- Security Handler ---
@client.on(events.ChatAction)
async def handler(event):
    if event.user_joined or event.user_added:
        if event.chat_id == CHANNEL_ID:
            user = await event.get_user()
            
            if user.bot:
                await client.kick_participant(CHANNEL_ID, user.id)
                print(f"Kicked a bot: {user.id}")
                return

            try:
                if not user.first_name:
                    await client.kick_participant(CHANNEL_ID, user.id)
                    print(f"Kicked invalid user: {user.id}")
            except Exception as e:
                print(f"Error checking user: {e}")

async def main():
    # Web Server နဲ့ Telegram Client ကို ပြိုင်တူ Run ခြင်း
    await asyncio.gather(
        client.start(bot_token=BOT_TOKEN),
        start_web_server()
    )
    print("Security Bot and Web Server are running...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
