# ------------------------- #
# Don't Remove Credit 
# Ask Doubt @AU_Bot_Discussion 
# Owner @Mr_Mohammed_29 
# ------------------------- #
import os
import time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
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

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🏠 Home", callback_data="home"),
            InlineKeyboardButton("ℹ️ About", callback_data="about")
        ],
        [
            InlineKeyboardButton("📖 Help", callback_data="help"),
            InlineKeyboardButton("📢 Updates", url=UPDATE_CHANNEL)
        ],
        [
            InlineKeyboardButton("👑 Owner", callback_data="owner"),
            InlineKeyboardButton("❌ Close", callback_data="close")
        ]
    ])

    await msg.reply(
        "🤖 **Welcome To Jinwoo Rename Bot**\n\nSend files to rename with metadata support.",
        reply_markup=buttons
    )
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

    text = """
ᴍᴀɴᴀɢɪɴɢ ᴍᴇᴛᴀᴅᴀᴛᴀ ғᴏʀ ʏᴏᴜʀ ᴠɪᴅᴇᴏs ᴀɴᴅ ғɪʟᴇs

ᴠᴀʀɪᴏᴜꜱ ᴍᴇᴛᴀᴅᴀᴛᴀ:

- ᴛɪᴛʟᴇ: Descriptive title of the media.
- ᴀᴜᴛʜᴏʀ: The creator or owner of the media.
- ᴀʀᴛɪꜱᴛ: The artist associated with the media.
- ᴀᴜᴅɪᴏ: Title or description of audio content.
- ꜱᴜʙᴛɪᴛʟᴇ: Title of subtitle content.
- ᴠɪᴅᴇᴏ: Title or description of video content.

ᴄᴏᴍᴍᴀɴᴅꜱ:

➜ /settitle
➜ /setauthor
➜ /setartist
➜ /setaudio
➜ /setsubtitle
➜ /setvideo

ᴇxᴀᴍᴘʟᴇ: /settitle My Video
"""

    await msg.reply(text)

# ---------------- METADATA SETTERS ----------------
@bot.on_message(filters.command("setartist"))
async def setartist(_, msg):
    if len(msg.command) < 2:
        return await msg.reply("Usage: /setartist Name")

    artist = msg.text.split(None, 1)[1]
    await set_user(msg.from_user.id, {"artist": artist})
    await msg.reply("Artist saved")


@bot.on_message(filters.command("setaudio"))
async def setaudio(_, msg):
    if len(msg.command) < 2:
        return await msg.reply("Usage: /setaudio Audio Title")

    audio = msg.text.split(None, 1)[1]
    await set_user(msg.from_user.id, {"audio": audio})
    await msg.reply("Audio saved")


@bot.on_message(filters.command("setsubtitle"))
async def setsubtitle(_, msg):
    if len(msg.command) < 2:
        return await msg.reply("Usage: /setsubtitle Subtitle")

    subtitle = msg.text.split(None, 1)[1]
    await set_user(msg.from_user.id, {"subtitle": subtitle})
    await msg.reply("Subtitle saved")


@bot.on_message(filters.command("setvideo"))
async def setvideo(_, msg):
    if len(msg.command) < 2:
        return await msg.reply("Usage: /setvideo Video Title")

    video = msg.text.split(None, 1)[1]
    await set_user(msg.from_user.id, {"video": video})
    await msg.reply("Video metadata saved")

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

    file_path = await msg.download(file_name=file.file_name)

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

# ---------- Callback --------------- #
@bot.on_callback_query()
async def cb(_, query):

    data = query.data

    if data == "home":
        await query.message.edit_text("🏠 Home Menu")

    elif data == "about":
        await query.message.edit_text("ℹ️ Rename Bot with Metadata + FFmpeg Engine")

    elif data == "help":
        await query.message.edit_text(
            "📖 Help:\n\n/set_caption\n/set_prefix\n/set_suffix\n/metadata"
        )

    elif data == "owner":
        await query.message.edit_text(f"👑 Owner ID: {OWNER_ID}")

    elif data == "close":
        await query.message.delete()

# ---------------- RUN ----------------
keep_alive()

print("BOT STARTED 🚀")
bot.run()

# ------------------------- #
# Don't Remove Credit 
# Ask Doubt @AU_Bot_Discussion 
# Owner @Mr_Mohammed_29 
# ------------------------- #
