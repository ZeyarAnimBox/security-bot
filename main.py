import os
import asyncio
from telethon import TelegramClient, events, types

# --- Settings ---
API_ID = 39181090
API_HASH = '956b15e38aa400de2451cb85a67194f7'
BOT_TOKEN = '8633754548:AAGRZFhzVz7QswvwZg4mafyRyNyPtdJFM3I'
CHANNEL_ID = -1002178787818

client = TelegramClient('security_bot', API_ID, API_HASH)

# --- Start Command (အသစ်ထည့်သွင်းထားသောအပိုင်း) ---
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    # Bot အလုပ်လုပ်မလုပ် စမ်းသပ်ရန်အတွက် ပြန်စာပို့ခိုင်းခြင်း
    await event.respond('မင်္ဂလာပါ Zeyar! Bot က အဆင်ပြေပြေ အလုပ်လုပ်နေပါပြီခင်ဗျာ။')

# --- Security Handler (မူရင်းအတိုင်း) ---
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
                full_user = await client(types.functions.users.GetFullUserRequest(id=user.id))
                if not user.first_name:
                    await client.kick_participant(CHANNEL_ID, user.id)
                    print(f"Kicked invalid user: {user.id}")
            except Exception as e:
                print(f"Error checking user: {e}")

async def main():
    await client.start(bot_token=BOT_TOKEN)
    print("Security Bot is running...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
