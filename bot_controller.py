# ====== Detection Alerts to Admins ======
from modules.main import app_bot
from modules.store import db
from pyrogram import filters
from config import PRIVATE_ADMINS

async def alert_admins(text):
    for admin_id in PRIVATE_ADMINS:
        try:
            await app_bot.send_message(admin_id, text)
        except Exception as e:
            print(f"[ALERT ERROR] Failed to send alert to {admin_id}: {e}")

BIO_KEYWORDS = ["t.me/", "discord.gg", "instagram.com", "facebook.com", "wa.me", "snapchat.com"]

@app_bot.on_message(filters.group & filters.text)
async def abuse_auto_delete(client, message):
    chat_id = message.chat.id
    user = message.from_user
    if not user or user.id in PRIVATE_ADMINS:
        return
    member = await client.get_chat_member(chat_id, user.id)
    if member.status in ["administrator", "creator"]:
        return
    if any(word in message.text.lower() for word in ["chutiya","bhosdike","lund"]):  # example
        try:
            await message.delete()
            warn = await message.reply_text(f"⚠️ {user.mention} Abusive content removed!", quote=True)
            await asyncio.sleep(5)
            await warn.delete()
        except Exception as e:
            print(f"[ABUSE Handler ERROR] Failed to delete message from {user.id} in chat {chat_id}: {e}")
            await alert_admins(f"❌ Failed to delete message from {user.mention} ({user.id}) in {chat_id}: {e}")

@app_bot.on_message(filters.group & filters.text)
async def bio_link_detect(client, message):
    chat_id = message.chat.id
    user = message.from_user
    if not user:
        return
    text = message.text.lower()
    if any(keyword in text for keyword in BIO_KEYWORDS):
        try:
            await message.delete()
            await alert_admins(f"⚠️ {user.mention} ({user.id}) posted a link/bio in chat {chat_id}: {message.text}")
        except Exception as e:
            print(f"[BIO Handler ERROR] Failed to delete message from {user.id} in chat {chat_id}: {e}")
            await alert_admins(f"❌ Failed to delete link/bio message from {user.mention} ({user.id}) in {chat_id}: {e}")
