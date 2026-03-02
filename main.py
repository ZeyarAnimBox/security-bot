import os
import asyncio
from telethon import TelegramClient, events, types

# --- Settings ---
API_ID = 39181090
API_HASH = '956b15e38aa400de2451cb85a67194f7'
BOT_TOKEN = '8633754548:AAGRZFhzVz7QswvwZg4mafyRyNyPtdJFM3I'
CHANNEL_ID = -1002178787818

client = TelegramClient('security_bot', API_ID, API_HASH)

@client.on(events.ChatAction)
async def handler(event):
    # လူသစ်ဝင်လာတာကို စစ်ဆေးခြင်း
    if event.user_joined or event.user_added:
        if event.chat_id == CHANNEL_ID:
            user = await event.get_user()
            
            # User ရဲ့ အချက်အလက်ကို စစ်ဆေးခြင်း
            if user.bot:
                await client.kick_participant(CHANNEL_ID, user.id)
                print(f"Kicked a bot: {user.id}")
                return

            try:
                # User ရဲ့ Full Info ကို ဆွဲထုတ်ကြည့်ခြင်း
                full_user = await client(types.functions.users.GetFullUserRequest(id=user.id))
                
                if not user.first_name:
                    await client.kick_participant(CHANNEL_ID, user.id)
                    print(f"Kicked invalid user: {user.id}")
            except Exception as e:
                print(f"Error checking user: {e}")

async def main():
    # Bot ကို စတင်နှိုးခြင်း
    await client.start(bot_token=BOT_TOKEN)
    print("Security Bot is running...")
    # Bot ကို အမြဲတမ်း အလုပ်လုပ်နေစေခြင်း
    await client.run_until_disconnected()

if __name__ == '__main__':
    # Python 3.14 ရဲ့ Event Loop ပြဿနာကို ဖြေရှင်းရန် asyncio.run သုံးခြင်း
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
