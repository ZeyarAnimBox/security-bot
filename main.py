import os
import asyncio
from telethon import TelegramClient, events, types
from aiohttp import web

# --- Settings ---
API_ID = 39181090
API_HASH = '956b15e38aa400de2451cb85a67194f7'
BOT_TOKEN = '8633754548:AAGRZFhzVz7QswvwZg4mafyRyNyPtdJFM3I'
CHANNEL_ID = -1002178787818
ADMIN_ID = 5522052096

client = TelegramClient('security_bot', API_ID, API_HASH)

# --- Render Port Binding Fix (Web Server) ---
async def handle(request):
    # Cron-job output too large error ကို ရှင်းရန် "OK" လို့ပဲ အတိုချုံး ပြန်ပို့ပါမယ်
    return web.Response(text="OK")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Web server started on port {port}")

# --- Start Command ---
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond('မင်္ဂလာပါ Zeyar! Bot က အဆင်ပြေပြေ အလုပ်လုပ်နေပါပြီခင်ဗျာ။')

# --- Security Handler & Notification ---
@client.on(events.ChatAction)
async def handler(event):
    if event.user_joined or event.user_added:
        if event.chat_id == CHANNEL_ID:
            user = await event.get_user()
            user_info = f"👤 Name: {user.first_name}\n🆔 ID: `{user.id}`\n🔗 Username: @{user.username if user.username else 'None'}"
            
            # ၁။ Bot အကောင့်ဖြစ်နေလျှင်
            if user.bot:
                await client.kick_participant(CHANNEL_ID, user.id)
                await client.send_message(ADMIN_ID, f"🚫 **Kicked a Bot!**\n\n{user_info}")
                return

            # ၂။ နာမည်မပါသော အကောင့်ဖြစ်နေလျှင်
            try:
                if not user.first_name:
                    await client.kick_participant(CHANNEL_ID, user.id)
                    await client.send_message(ADMIN_ID, f"🚫 **Kicked Invalid User (No Name)!**\n\n{user_info}")
                else:
                    # ၃။ ပုံမှန် User ဝင်လာလျှင် Zeyar ဆီ Notification ပို့ခြင်း
                    await client.send_message(ADMIN_ID, f"✅ **New Member Joined!**\n\n{user_info}")
            except Exception as e:
                print(f"Error checking user: {e}")

async def main():
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
