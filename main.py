import os
from telethon import TelegramClient, events, types

# --- Settings ---
API_ID = 39181090
API_HASH = '956b15e38aa400de2451cb85a67194f7'
BOT_TOKEN = '8633754548:AAGRZFhzVz7QswvwZg4mafyRyNyPtdJFM3I'
CHANNEL_ID = -1002178787818

client = TelegramClient('security_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

@client.on(events.ChatAction)
async def handler(event):
    # လူသစ်ဝင်လာတာကို စစ်ဆေးခြင်း
    if event.user_joined or event.user_added:
        if event.chat_id == CHANNEL_ID:
            user = await event.get_user()
            
            # User ရဲ့ အချက်အလက်ကို စစ်ဆေးခြင်း
            # တကယ်လို့ User က Bot ဖြစ်နေရင် ဒါမှမဟုတ် လက္ခဏာမကောင်းရင်
            if user.bot:
                await client.kick_participant(CHANNEL_ID, user.id)
                print(f"Kicked a bot: {user.id}")
                return

            # အောက်ပါ စစ်ဆေးမှုက Fake App/Userbot သမားတွေကို တားဆီးဖို့ပါ
            try:
                # User ရဲ့ Full Info ကို ဆွဲထုတ်ကြည့်ခြင်း
                full_user = await client(types.functions.users.GetFullUserRequest(id=user.id))
                
                # အကယ်၍ User က Official App မဟုတ်ဘဲ Script နဲ့ဝင်ရင် 
                # အချို့သော အချက်အလက်တွေက ပုံမှန်မဟုတ်ဘဲ ဖြစ်နေတတ်ပါတယ်
                if not user.first_name:
                    await client.kick_participant(CHANNEL_ID, user.id)
                    print(f"Kicked invalid user: {user.id}")
            except Exception as e:
                print(f"Error checking user: {e}")

print("Security Bot is running...")
client.run_until_disconnected()