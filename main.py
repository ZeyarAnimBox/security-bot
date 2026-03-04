import os
import asyncio
from telethon import TelegramClient, events, Button
from aiohttp import web

# --- Settings ---
API_ID = 39181090
API_HASH = '956b15e38aa400de2451cb85a67194f7'
BOT_TOKEN = '8633754548:AAGRZFhzVz7QswvwZg4mafyRyNyPtdJFM3I'
CHANNEL_ID = -1002178787818
ADMIN_ID = 5522052096

client = TelegramClient('security_bot', API_ID, API_HASH)

# --- Render Port Binding Fix ---
async def handle(request):
    return web.Response(text="OK")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

# --- Start Command with Menu Button ---
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    if event.sender_id == ADMIN_ID:
        buttons = [[Button.text("🔍 ID ဖြင့် လူရှာရန်", resize=True)]]
        await event.respond('မင်္ဂလာပါ Zeyar! Bot က အဆင်သင့်ဖြစ်နေပါပြီ။\n\nChannel ထဲက လူဟောင်းတွေကို ရှာချင်ရင် ID နံပါတ်ကို ဒီအတိုင်း ရိုက်ပို့ပေးပါခင်ဗျာ။', buttons=buttons)

# --- Handle Menu Button Click ---
@client.on(events.NewMessage(pattern='🔍 ID ဖြင့် လူရှာရန်'))
async def ask_id(event):
    if event.sender_id == ADMIN_ID:
        await event.respond("ရှာဖွေလိုသည့် User ရဲ့ **ID နံပါတ်** ကို ရိုက်ထည့်ပေးပါခင်ဗျာ။\n(ဥပမာ - `1919806454`)")

# --- Enhanced User Details Function (Search in Channel) ---
async def get_user_details(user_id):
    try:
        uid = int(user_id)
        # ၁။ Channel ထဲမှာ အဲဒီ ID ရှိမရှိ အရင်စစ်ဆေးပြီး အချက်အလက်ယူခြင်း
        participant = await client.get_permissions(CHANNEL_ID, uid)
        user = await client.get_entity(uid)
        
        f_name = user.first_name if user.first_name else "None"
        l_name = user.last_name if user.last_name else "None"
        
        return (
            f"🔍 **User Found in Channel!**\n\n"
            f"👤 **First Name:** {f_name}\n"
            f"👤 **Last Name:** {l_name}\n"
            f"🆔 **ID:** `{user.id}`\n"
            f"🔗 **Username:** @{user.username if user.username else 'None'}\n"
            f"🖼 **Profile:** [Click to View Profile](tg://user?id={user.id})"
        )
    except ValueError:
        return "❌ ID နံပါတ် အမှားဖြစ်နေပါသည်။ ဂဏန်းများသာ ထည့်ပေးပါ။"
    except Exception as e:
        # Channel ထဲမှာ မရှိရင် သို့မဟုတ် ရှာမတွေ့ရင် ပြမည့်စာ
        return f"❌ ရှာမတွေ့ပါ။ အကြောင်းရင်း- {e}\n(ထိုသူသည် Channel ထဲမှာ မရှိခြင်း သို့မဟုတ် Bot က ရှာမရခြင်း ဖြစ်နိုင်ပါသည်)"

# --- Check User by ID Handler ---
@client.on(events.NewMessage)
async def check_handler(event):
    if event.sender_id != ADMIN_ID or event.text.startswith('/start') or event.text == "🔍 ID ဖြင့် လူရှာရန်":
        return

    # ID နံပါတ် သီးသန့်ဖြစ်စေ၊ /check ပါသည်ဖြစ်စေ ရှာပေးခြင်း
    text = event.text.replace('/check', '').strip()
    if text.isdigit():
        response = await get_user_details(text)
        await event.respond(response)

# --- Inline Button Callback Handler ---
@client.on(events.CallbackQuery(pattern=b'check_(.*)'))
async def callback_handler(event):
    user_id = event.data_match.group(1).decode('utf-8')
    response = await get_user_details(user_id)
    await event.respond(response)

# --- Security Handler & Notification ---
@client.on(events.ChatAction)
async def handler(event):
    if (event.user_joined or event.user_added) and event.chat_id == CHANNEL_ID:
        user = await event.get_user()
        
        f_name = user.first_name if user.first_name else "None"
        l_name = user.last_name if user.last_name else "None"
        check_button = [Button.inline("🔎 အသေးစိတ်စစ်ဆေးရန်", data=f"check_{user.id}")]
        
        user_info = (
            f"👤 **First Name:** {f_name}\n"
            f"👤 **Last Name:** {l_name}\n"
            f"🆔 **ID:** `{user.id}`\n"
            f"🔗 **Username:** @{user.username if user.username else 'None'}"
        )

        if user.bot:
            await client.kick_participant(CHANNEL_ID, user.id)
            await client.send_message(ADMIN_ID, f"🚫 **Kicked a Bot!**\n\n{user_info}", buttons=check_button)
            return

        if not user.first_name:
            await client.kick_participant(CHANNEL_ID, user.id)
            await client.send_message(ADMIN_ID, f"🚫 **Kicked Invalid User (No Name)!**\n\n{user_info}", buttons=check_button)
        else:
            await client.send_message(ADMIN_ID, f"✅ **New Member Joined!**\n\n{user_info}", buttons=check_button)

async def main():
    await asyncio.gather(client.start(bot_token=BOT_TOKEN), start_web_server())
    print("Bot is running...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
