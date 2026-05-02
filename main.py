# ------------------------- #
# Don't Remove Credit 
# Ask Doubt @AU_Bot_Discussion 
# Owner @Mr_Mohammed_29 
# ------------------------- #
import os
import time
from pyrogram import Client, filters
from config import (
    API_ID,
    API_HASH,
    BOT_TOKEN,
    OWNER_ID,
    MONGO_URI,
    LOG_CHANNEL,
    UPDATE_CHANNEL
)

print("LOG_CHANNEL:", LOG_CHANNEL)
print("UPDATE_CHANNEL:", UPDATE_CHANNEL)

from database import *
from utils import progress_bar
from ffmpeg_utils import add_metadata
from keep_alive import keep_alive

bot = Client(
    "rename-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ---------------- START ----------------
@bot.on_message(filters.command("start"))
async def start(_, msg):
    await msg.reply("𝖈ʜᴇᴄᴋ 𝖎 𝖆ᴍ ʟɪᴠᴇ ⚡")

# ---------------- CAPTION ----------------
@bot.on_message(filters.command("set_caption"))
async def set_caption(_, msg):
    cap = msg.text.split(None, 1)[1]
    await set_user(msg.from_user.id, {"caption": cap})
    await msg.reply("Caption set")

@bot.on_message(filters.command("see_caption"))
async def see_caption(_, msg):
    user = await get_user(msg.from_user.id) or {}
    await msg.reply(user.get("caption", "Not set"))

@bot.on_message(filters.command("del_caption"))
async def del_caption(_, msg):
    await set_user(msg.from_user.id, {"caption": ""})
    await msg.reply("Deleted")

# ---------------- PREFIX / SUFFIX ----------------
@bot.on_message(filters.command("set_prefix"))
async def set_prefix(_, msg):
    p = msg.text.split(None, 1)[1]
    await set_user(msg.from_user.id, {"prefix": p})
    await msg.reply("Prefix set")

@bot.on_message(filters.command("set_suffix"))
async def set_suffix(_, msg):
    s = msg.text.split(None, 1)[1]
    await set_user(msg.from_user.id, {"suffix": s})
    await msg.reply("Suffix set")

# ---------------- METADATA ----------------
@bot.on_message(filters.command("metadata"))
async def metadata(_, msg):
    try:
        _, title, author, desc = msg.text.split(" ", 3)
        await set_user(msg.from_user.id, {
            "metadata": {
                "title": title,
                "author": author,
                "description": desc
            }
        })
        await msg.reply("Metadata saved")
    except:
        await msg.reply("Usage: /metadata title author description")

# ---------------- THUMB ----------------
@bot.on_message(filters.photo)
async def save_thumb(_, msg):
    await set_user(msg.from_user.id, {"thumb": msg.photo.file_id})
    await msg.reply("Thumbnail saved")

# ---------------- RENAME CORE + FFMPEG ----------------
@bot.on_message(filters.document)
async def rename(_, msg):
    user_id = msg.from_user.id
    file = msg.document

    user = await get_user(user_id) or {}

    prefix = user.get("prefix", "")
    suffix = user.get("suffix", "")
    caption = user.get("caption", "")
    meta = user.get("metadata", {})

    new_name = f"{prefix}{file.file_name}{suffix}"

    status = await msg.reply("Downloading...")

    file_path = await msg.download()

    output = f"temp_{new_name}"

    await status.edit("Applying metadata...")

    final = add_metadata(
        file_path,
        output,
        meta.get("title", ""),
        meta.get("author", ""),
        meta.get("description", "")
    )

    await status.edit("Uploading...")

    def prog(current, total):
        try:
            bar = progress_bar(current, total)
            status.edit_text(f"Uploading...\n{bar}")
        except:
            pass

    await msg.reply_document(
        document=final,
        file_name=new_name,
        caption=caption,
        progress=prog
    )

    try:
        os.remove(file_path)
        os.remove(final)
    except:
        pass

    await status.delete()

# ---------------- ADMIN ----------------
def admin(uid):
    return uid == OWNER_ID

@bot.on_message(filters.command("addpremium"))
async def addprem(_, msg):
    if not admin(msg.from_user.id):
        return
    uid = int(msg.text.split()[1])
    await set_user(uid, {"premium": True})
    await msg.reply("Premium added")

@bot.on_message(filters.command("remove_premium"))
async def remprem(_, msg):
    if not admin(msg.from_user.id):
        return
    uid = int(msg.text.split()[1])
    await set_user(uid, {"premium": False})
    await msg.reply("Removed")

@bot.on_message(filters.command("status"))
async def status(_, msg):
    await msg.reply("Bot running 24/7 ⚡")

# ---------------- RUN ----------------
keep_alive()

print("BOT STARTED 🚀")
bot.run()

# ------------------------- #
# Don't Remove Credit 
# Ask Doubt @AU_Bot_Discussion 
# Owner @Mr_Mohammed_29 
# ------------------------- #
