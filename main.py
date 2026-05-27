# ------------------------- #
# Don't Remove Credit 
# Ask Doubt @AU_Bot_Discussion 
# Owner @Mr_Mohammed_29 
# ------------------------- #
import os
import time
import asyncio
import ffmpeg
import psutil
import datetime

def log_event(text: str):
    with open("bot_logs.txt", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now()}] {text}\n")

if not os.path.exists("downloads"):
    os.makedirs("downloads")

if not os.path.exists("thumbs"):
    os.makedirs("thumbs")

START_TIME = time.time()

# ------------------------- #
def get_uptime():
    seconds = int(time.time() - START_TIME)
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{h}h {m}m {s}s"


def get_memory():
    process = psutil.Process(os.getpid())
    mem = process.memory_info().rss / (1024 * 1024)
    return f"{mem:.2f} MB"


async def get_ping():
    start = time.time()
    await asyncio.sleep(0)
    end = time.time()
    return f"{round((end - start) * 1000)} ms"

# ------------------------- #

from PIL import Image
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.enums import ChatMemberStatus

active_tasks = {}

# ---------------- FORCE SUB ---------------- #

# -------- MAX FILE LIMIT -------- #

MAX_FILE_SIZE = 2097152000  # 2GB 

FORCE_SUB_CHANNEL = None
FREE_MODE = True

user_mode = {}

download_last_edit = 0
upload_last_edit = 0

def parse_duration(value: str):
    value = value.lower().strip()

    if value.endswith("hr"):
        return int(value[:-2]) * 3600

    if value.endswith("h"):
        return int(value[:-1]) * 3600

    if value.endswith("d"):
        return int(value[:-1]) * 86400

    if value.endswith("w"):
        return int(value[:-1]) * 604800

    if value.endswith("m"):
        return int(value[:-1]) * 2592000  # 30 days approx

    if value.endswith("y"):
        return int(value[:-1]) * 31536000

    return None

# ------------------------- #

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_home_text(user):
    return (
        f"Hᴇʏ {user.mention} ♡\n\n"
        "Wᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ᴍᴏꜱᴛ ᴀᴅᴠᴀɴᴄᴇᴅ Jɪɴᴡᴏᴏ Sᴜɴɢ Rᴇɴᴀᴍᴇ Bᴏᴛ!\n\n"
        "» ᴡɪᴛʜ ᴍʏ ᴘᴏᴡᴇʀꜰᴜʟ ꜰᴇᴀᴛᴜʀᴇꜱ, ʏᴏᴜ ᴄᴀɴ:\n"
        "○ Aᴅᴅ ᴄᴜsᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ ᴀɴᴅ ᴛʜᴜᴍʙɴᴀɪʟ\n"
        "○ ᴀɴᴅ ᴀʟsᴏ ᴄᴀɴ sᴇᴛ ᴘʀᴇғɪx ᴀɴᴅ sᴜғғɪx ᴏɴ ʏᴏᴜʀ ғɪʟᴇs.⚡️\n\n"
        "๏ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʜᴏᴡ ᴛᴏ ᴜsᴇ ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ᴍʏ ᴄᴏᴍᴍᴀɴᴅs..\n\n"
        "›› ᴛʜɪs ʙᴏᴛ ɪs ᴅᴇᴘʟᴏʏᴇᴅ ʙʏ: <a href='https://t.me/Mr_Mohammed_29'>ᴍᴏʜᴀᴍᴍᴇᴅ</a>"
    )


def get_home_buttons():
    update_url = UPDATE_CHANNEL

    if not update_url or not isinstance(update_url, str) or not update_url.startswith("http"):
        update_url = "https://t.me/Anime_UpdatesAU"

    return InlineKeyboardMarkup([
        [InlineKeyboardButton("• ᴍʏ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs •", callback_data='help')],
        [
            InlineKeyboardButton('ᴜᴘᴅᴀᴛᴇs', url=update_url),
            InlineKeyboardButton('sᴜᴘᴘᴏʀᴛ', url="https://t.me/AU_Bot_Discussion")
        ],
        [
            InlineKeyboardButton('ᴀʙᴏᴜᴛ', callback_data='about'),
            InlineKeyboardButton('sᴏᴜʀᴄᴇ', callback_data='source')
        ]
    ])

from pyrogram.types import CallbackQuery

from config import (
    API_ID,
    API_HASH,
    BOT_TOKEN,
    OWNER_ID,
    MONGO_URI,
    LOG_CHANNEL,
    UPDATE_CHANNEL
)

ADMINS = [OWNER_ID]

user_files = {}

print("LOG_CHANNEL:", LOG_CHANNEL)
print("UPDATE_CHANNEL:", UPDATE_CHANNEL)

from database import *

dump_channels = {}

from utils import progress_bar
from ffmpeg_utils import add_metadata
from keep_alive import keep_alive

def humanbytes(size):
    if not size:
        return "0 B"

    power = 1024
    n = 0
    Dic_powerN = {0: 'B', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}

    while size >= power and n < len(Dic_powerN) - 1:
        size /= power
        n += 1

    return str(round(size, 2)) + " " + Dic_powerN[n]

def time_formatter(seconds):
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h}h {m}m {s}s"

import re

def safe_name(name):
    return re.sub(r'[\\\\/:*?"<>|]', '_', name)

async def get_thumbnail(bot, user_thumb, is_video, file_path, user_id):

    if user_thumb:
        path = await bot.download_media(user_thumb, file_name=f"thumb_{user_id}.jpg")
        return path

    if is_video:
        thumb_path = f"thumb_{user_id}.jpg"

        try:
            (
                ffmpeg
                .input(file_path, ss=1)
                .output(thumb_path, vframes=1)
                .run(overwrite_output=True, quiet=True)
            )
            return thumb_path
        except:
            return None

    return None

def calc_progress(current, total, start_time, last_current=0, last_time=0):
    now = time.time()

    diff = max(now - start_time, 0.1)

    # percentage
    percent = (current / total) * 100 if total else 0

    # smoother speed (difference based)
    speed = (current - last_current) / (now - last_time) if last_time else current / diff
    speed = max(speed, 0)

    # ETA safer calculation
    remaining = total - current
    eta = remaining / speed if speed > 0 else 0

    return percent, speed, eta
# ------------------------- #

def smart_thumb(path):
    try:
        size = os.path.getsize(path)

        # If already small → use directly
        if size <= 200 * 1024:
            return path

        # Else compress
        img = Image.open(path).convert("RGB")
        img.thumbnail((320, 320))
        img.save(path, "JPEG", quality=80)

        return path
    except:
        return None
# ------------------------- #

def generate_video_thumb(video_path, output):
    try:
        (
            ffmpeg
            .input(video_path, ss=1)
            .output(output, vframes=1)
            .run(overwrite_output=True)
        )
        return output
    except:
        return None

#---------------------------#

def get_video_metadata(path):
    try:
        probe = ffmpeg.probe(path)
        video_stream = next(
            (s for s in probe["streams"] if s["codec_type"] == "video"),
            None
        )

        duration = int(float(probe["format"]["duration"])) if "duration" in probe["format"] else 0
        width = int(video_stream["width"]) if video_stream else 0
        height = int(video_stream["height"]) if video_stream else 0

        return duration, width, height
    except Exception as e:
        print("Metadata Error:", e)
        return 0, 0, 0

# ------------------------- #

bot = Client(
    "rename-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=120,
    sleep_threshold=15,
    max_concurrent_transmissions=10
)

# ---------------- CHECK FORCE SUB ---------------- #

async def check_force_sub(client, user_id):

    # If no force sub enabled
    if not FORCE_SUB_CHANNEL:
        return True

    try:
        member = await client.get_chat_member(
            FORCE_SUB_CHANNEL,
            user_id
        )

        # User joined
        if member.status in [
            ChatMemberStatus.MEMBER,
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ]:
            return True

        return False

    except Exception as e:
        print("FORCE SUB ERROR:", e)
        return False

# ---------------- FORCE SUB COMMANDS ---------------- #

@bot.on_message(filters.private & filters.command("fsub"))
async def add_fsub(client, message):

    global FORCE_SUB_CHANNEL

    if message.from_user.id not in ADMINS:
        return

    if len(message.command) < 2:
        return await message.reply_text(
            "ᴛᴇxᴛ ᴡɪᴛʜ\n/fsub Cʜᴀɴɴᴇʟ_Usᴇʀɴᴀᴍᴇ"
        )

    channel = message.command[1]

    if not channel.startswith("@"):
        channel = "@" + channel

    FORCE_SUB_CHANNEL = channel

    await message.reply_text(
        f"✅ Fᴏʀᴄᴇ Sᴜʙsᴄʀɪʙᴇᴅ Cʜᴀɴɴᴇʟ Aᴅᴅᴇᴅ\n\nCʜᴀɴɴᴇʟ : {channel}"
    )


@bot.on_message(filters.private & filters.command("nofsub"))
async def remove_fsub(client, message):

    global FORCE_SUB_CHANNEL

    if message.from_user.id not in ADMINS:
        return

    FORCE_SUB_CHANNEL = None

    await message.reply_text(
        "✅ Fᴏʀᴄᴇ Sᴜʙsᴄʀɪʙᴇᴅ Cʜᴀɴɴᴇʟ Rᴇᴍᴏᴠᴇᴅ"
    )

# ---------------- FREE MODE ---------------- #

@bot.on_message(filters.private & filters.command("freemode"))
async def free_mode(client, message):

    global FREE_MODE

    if message.from_user.id not in ADMINS:
        return

    FREE_MODE = True

    await message.reply_text(
        "✅ Fʀᴇᴇ Mᴏᴅᴇ Eɴᴀʙʟᴇᴅ\n\n ○ Nᴏᴡ Usᴇʀs Cᴀɴ Usᴇ Tʜᴇ Bᴏᴛ ○"
    )


@bot.on_message(filters.private & filters.command("disablemode"))
async def disable_mode(client, message):

    global FREE_MODE

    if message.from_user.id not in ADMINS:
        return

    FREE_MODE = False

    await message.reply_text(
        "🚫 Fʀᴇᴇ Mᴏᴅᴇ Dɪsᴀʙʟᴇᴅ\n\n ○ Nᴏᴡ Usᴇʀs Cᴀɴɴᴏᴛ Usᴇ Tʜᴇ Bᴏᴛ ○"
    )

# ---------------- START ----------------
@bot.on_message(filters.command("start"))
async def start(client, message):

    # ---------------- DISABLE MODE ---------------- #

    if not FREE_MODE:

        if message.from_user.id not in ADMINS:
            return await message.reply_text(
                "🚫 Fʀᴇᴇ Mᴏᴅᴇ Dɪsᴀʙʟᴇᴅ Bʏ Oᴡɴᴇʀ\n\n ● Nᴏᴡ Yᴏᴜ Cᴀɴɴᴏᴛ Usᴇ Tʜɪs Bᴏᴛ ●"
            )

    # ---------------- FORCE SUB CHECK ---------------- #

    if message.from_user.id not in ADMINS:

        joined = await check_force_sub(client, message.from_user.id)

        if joined is False:
           buttons = InlineKeyboardMarkup([
               [
                   InlineKeyboardButton(
                       "● Jᴏɪɴ Nᴏᴡ ●",
                       url=f"https://t.me/{FORCE_SUB_CHANNEL.replace('@', '')}"
                   )
               ]
           ])

           return await message.reply_text(
               "›› ‼️ ʟᴏᴏᴋs ʟɪᴋᴇ ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ ᴊᴏɪɴᴇᴅ ᴛᴏ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ ʏᴇᴛ, sᴜʙsᴄʀɪʙᴇ ɴᴏw.",
               reply_markup=buttons
           )

    try:
        if await is_banned(message.from_user.id):
            return await message.reply("🚫 Yᴏᴜ Aʀᴇ Bᴀɴɴᴇᴅ.")

        await add_user(message.from_user.id)

        log_event(f"User started bot: {message.from_user.id}")

        user = message.from_user

        # ---------------- ANIMATION ----------------
        try:
            m = await message.reply_text("Sʜᴀᴅᴏᴡ Oғ Mᴏɴᴀʀᴄʜ. . .")
            await asyncio.sleep(0.5)
            await m.edit_text("🎊")
            await asyncio.sleep(0.5)
            await m.edit_text("⚡")
            await asyncio.sleep(0.5)
            await m.edit_text("Jɪɴᴡᴏᴏ Sᴜɴɢ...")
            await asyncio.sleep(0.5)
            await m.delete()
        except Exception as e:
            print("ANIMATION ERROR:", e)

        # ---------------- MAIN MESSAGE ----------------
        try:
            await message.reply_text(
                get_home_text(user),
                reply_markup=get_home_buttons(),
                parse_mode=ParseMode.HTML
            )
        except Exception as e:
            print("HOME UI ERROR:", e)

            # 🔥 fallback if buttons fail
            await message.reply_text(
                get_home_text(user),
                reply_markup=get_home_buttons(),
                parse_mode=ParseMode.HTML
            )

    except Exception as e:
        print("START ERROR:", e)
# ---------------- CAPTION ----------------
@bot.on_message(filters.command("set_caption"))
async def set_caption(_, msg):

    if await is_banned(msg.from_user.id):
        return await msg.reply("🚫 Yᴏᴜ Aʀᴇ Bᴀɴɴᴇᴅ.")

    if len(msg.command) < 2:
        return await msg.reply(
            "Gɪᴠᴇ Tʜᴇ Cᴀᴘᴛɪᴏɴ\n\nExᴀᴍᴘʟᴇ:- /set_caption Welcome To Jinwoo Rename Bot @Anime_UpdatesAU"
        )

    cap = msg.text.split(None, 1)[1]
    await set_user(msg.from_user.id, {"caption": cap})
    await msg.reply("Cᴀᴘᴛɪᴏɴ Sᴀᴠᴇᴅ ✅️")

@bot.on_message(filters.command("see_caption"))
async def see_caption(_, msg):

    user = await get_user(msg.from_user.id) or {}

    caption = user.get("caption")

    if not caption:
        caption = "Nᴏ Cᴀᴘᴛɪᴏɴ Is Tʜᴇʀᴇ, Aᴅᴅ Nᴏᴡ"

    await msg.reply(caption)

@bot.on_message(filters.command("del_caption"))
async def del_caption(_, msg):
    await set_user(msg.from_user.id, {"caption": ""})
    await msg.reply("❌️ Cᴀᴘᴛɪᴏɴ Dᴇʟᴇᴛᴇᴅ")

# ---------------- PREFIX / SUFFIX ----------------
@bot.on_message(filters.command("set_prefix"))
async def set_prefix(_, msg):

    if len(msg.command) < 2:
        return await msg.reply("Gɪᴠᴇ Tʜᴇ Pʀᴇғɪx Lɪᴋᴇ Tʜɪs\n\nExᴀᴍᴘʟᴇ:- /set_prefix @Anime_UpdatesAU")

    text = msg.text.split(None, 1)[1]
    await set_user(msg.from_user.id, {"prefix": text})
    await msg.reply("Pʀᴇғɪx Sᴀᴠᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ✨")


@bot.on_message(filters.command("set_suffix"))
async def set_suffix(_, msg):

    if len(msg.command) < 2:
        return await msg.reply("Gɪᴠᴇ Tʜᴇ Sᴜғғɪx Lɪᴋᴇ Tʜɪs\n\nExᴀᴍᴘʟᴇ:- /set_prefix @Anime_UpdatesAU")

    text = msg.text.split(None, 1)[1]
    await set_user(msg.from_user.id, {"suffix": text})
    await msg.reply("Sᴜғғɪx Sᴀᴠᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ✨")


@bot.on_message(filters.command("see_prefix"))
async def see_prefix(_, msg):

    user = await get_user(msg.from_user.id) or {}
    prefix = user.get("prefix")

    if not prefix:
        return await msg.reply("Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Aɴʏ Pʀᴇғɪx Tᴏ Sᴇᴇ")

    await msg.reply(f"Current prefix: `{prefix}`")


@bot.on_message(filters.command("del_prefix"))
async def del_prefix(_, msg):

    await set_user(msg.from_user.id, {"prefix": ""})
    await msg.reply("Pʀᴇғɪx Dᴇʟᴇᴛᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ ⚡️")


@bot.on_message(filters.command("see_suffix"))
async def see_suffix(_, msg):

    user = await get_user(msg.from_user.id) or {}
    suffix = user.get("suffix")

    if not suffix:
        return await msg.reply("Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Aɴʏ Sᴜғғɪx Tᴏ Sᴇᴇ")

    await msg.reply(f"Current suffix: `{suffix}`")


@bot.on_message(filters.command("del_suffix"))
async def del_suffix(_, msg):

    await set_user(msg.from_user.id, {"suffix": ""})
    await msg.reply("Sᴜғғɪx Dᴇʟᴇᴛᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ ⚡️")

# ---------------- AUTO RENAME ---------------- #

@bot.on_message(filters.command("autorename"))
async def autorename_cmd(_, msg):

    if len(msg.command) < 2:
        return await msg.reply(
            "Pʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ʀᴇɴᴀᴍᴇ ᴛᴇᴍᴘʟᴀᴛᴇ\n\n"
            "➤ Example:\n"
            "/autorename One Piece [S{season} E{episode}] [{quality}] [{audio}] x264 ESubs Anime_UpdatesAU\n\n"
            "Nᴏᴛᴇ: Dᴏɴ'ᴛ ᴘᴜᴛ .mkv ᴏʀ .mp4 ᴀᴛ ᴛʜᴇ ᴇɴᴅ."
        )

    template = msg.text.split(None, 1)[1]

    await set_user(
        msg.from_user.id,
        {
            "autorename": template,
            "episode": 1
        }
    )

    await msg.reply_text(
        f"✅ Aᴜᴛᴏ Rᴇɴᴀᴍᴇ Sᴀᴠᴇᴅ\n\n`{template}`"
    )


@bot.on_message(filters.command("see_autorename"))
async def see_autorename(_, msg):

    user = await get_user(msg.from_user.id) or {}

    template = user.get("autorename")

    if not template:
        return await msg.reply(
            "❌ Nᴏ Aᴜᴛᴏ Rᴇɴᴀᴍᴇ Tᴇᴍᴘʟᴀᴛᴇ Sᴇᴛ"
        )

    episode = user.get("episode", 1)

    await msg.reply(
        f"📄 Aᴜᴛᴏ Rᴇɴᴀᴍᴇ Tᴇᴍᴘʟᴀᴛᴇ:\n\n"
        f"`{template}`\n\n"
        f"📌 Nᴇxᴛ Eᴘɪsᴏᴅᴇ: `{episode}`"
    )


@bot.on_message(filters.command("del_autorename"))
async def del_autorename(_, msg):

    await set_user(
        msg.from_user.id,
        {
            "autorename": "",
            "episode": 1
        }
    )

    await msg.reply(
        "❌ Aᴜᴛᴏ Rᴇɴᴀᴍᴇ Dᴇʟᴇᴛᴇᴅ"
    )

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

    buttons = InlineKeyboardMarkup([
        [
        InlineKeyboardButton("Hᴏᴍᴇ", callback_data="home"),
        InlineKeyboardButton("Cʟᴏsᴇ", callback_data="close")
        ]
    ])

    await msg.reply(
        text,
        reply_markup=buttons,
        disable_web_page_preview=True
    )

# ---------------- METADATA SETTERS ----------------
@bot.on_message(filters.command("settitle"))
async def settitle(_, msg):

    if len(msg.command) < 2:
        return await msg.reply("Gɪᴠᴇ Tʜᴇ Tɪᴛʟᴇ\n\nExᴀᴍᴩʟᴇ:- /settitle Encoded By @Anime_UpdatesAU")

    text = msg.text.split(None, 1)[1]
    await set_user(msg.from_user.id, {"title": text})
    await msg.reply("✅ Tɪᴛʟᴇ Sᴀᴠᴇᴅ")


@bot.on_message(filters.command("setauthor"))
async def setauthor(_, msg):

    if len(msg.command) < 2:
        return await msg.reply("Gɪᴠᴇ Tʜᴇ Aᴜᴛʜᴏʀ\n\nExᴀᴍᴩʟᴇ:- /setauthor @Anime_UpdatesAU")

    text = msg.text.split(None, 1)[1]
    await set_user(msg.from_user.id, {"author": text})
    await msg.reply("✅ Aᴜᴛʜᴏʀ Sᴀᴠᴇᴅ")


@bot.on_message(filters.command("setartist"))
async def setartist(_, msg):

    if len(msg.command) < 2:
        return await msg.reply("Gɪᴠᴇ Tʜᴇ Aʀᴛɪꜱᴛ\n\nExᴀᴍᴩʟᴇ:- /setartist @Anime_UpdatesAU")

    text = msg.text.split(None, 1)[1]
    await set_user(msg.from_user.id, {"artist": text})
    await msg.reply("✅ Aʀᴛɪꜱᴛ Sᴀᴠᴇᴅ")


@bot.on_message(filters.command("setaudio"))
async def setaudio(_, msg):

    if len(msg.command) < 2:
        return await msg.reply("Gɪᴠᴇ Tʜᴇ Aᴜᴅɪᴏ Tɪᴛʟᴇ\n\nExᴀᴍᴩʟᴇ:- /setaudio @Anime_UpdatesAU")

    text = msg.text.split(None, 1)[1]
    await set_user(msg.from_user.id, {"audio": text})
    await msg.reply("✅ Aᴜᴅɪᴏ Sᴀᴠᴇᴅ")


@bot.on_message(filters.command("setsubtitle"))
async def setsubtitle(_, msg):

    if len(msg.command) < 2:
        return await msg.reply("Gɪᴠᴇ Tʜᴇ Sᴜʙᴛɪᴛʟᴇ Tɪᴛʟᴇ\n\nExᴀᴍᴩʟᴇ:- /setsubtitle @Anime_UpdatesAU")

    text = msg.text.split(None, 1)[1]
    await set_user(msg.from_user.id, {"subtitle": text})
    await msg.reply("✅ Sᴜʙᴛɪᴛʟᴇ Sᴀᴠᴇᴅ")


@bot.on_message(filters.command("setvideo"))
async def setvideo(_, msg):

    if len(msg.command) < 2:
        return await msg.reply("Gɪᴠᴇ Tʜᴇ Vɪᴅᴇᴏ Tɪᴛʟᴇ\n\nExᴀᴍᴩʟᴇ:- /setvideo Encoded by @Anime_UpdatesAU")

    text = msg.text.split(None, 1)[1]
    await set_user(msg.from_user.id, {"video": text})
    await msg.reply("✅ Vɪᴅᴇᴏ Mᴇᴛᴀᴅᴀᴛᴀ Sᴀᴠᴇᴅ")

# ---------------- SEE METADATA ---------------- #

@bot.on_message(filters.command("see_metadata"))
async def see_metadata(_, msg):

    user = await get_user(msg.from_user.id) or {}

    title = user.get("title", "Not Set")
    author = user.get("author", "Not Set")
    artist = user.get("artist", "Not Set")
    audio = user.get("audio", "Not Set")
    subtitle = user.get("subtitle", "Not Set")
    video = user.get("video", "Not Set")

    text = f"""
📂 Sᴀᴠᴇᴅ Mᴇᴛᴀᴅᴀᴛᴀ

━━━━━━━━━━━━━━━

🎬 Title:
`{title}`

👤 Author:
`{author}`

🎨 Artist:
`{artist}`

🎵 Audio:
`{audio}`

💬 Subtitle:
`{subtitle}`

📹 Video:
`{video}`

━━━━━━━━━━━━━━━
"""

    await msg.reply_text(text)

# ------------------------- #
# Don't Remove Credit 
# Ask Doubt @AU_Bot_Discussion 
# Owner @Mr_Mohammed_29 
# ------------------------- #

# ---------------- DUMP CHANNEL ---------------- #

@bot.on_message(filters.command("setdump"))
async def set_dump(_, msg):

    if len(msg.command) < 2:
        return await msg.reply(
            "Usage:\n/setdump -100xxxxxxxxxx"
        )

    channel_id = msg.command[1]

    dump_channels[msg.from_user.id] = channel_id

    await msg.reply(
        f"✅ Dump Channel Saved\n\nID: `{channel_id}`"
    )

@bot.on_message(filters.command("chkdump"))
async def chk_dump(_, msg):

    channel_id = dump_channels.get(msg.from_user.id)

    if not channel_id:
        return await msg.reply("❌ No Dump Channel Added")

    await msg.reply(
        f"📦 Current Dump Channel:\n`{channel_id}`"
    )

@bot.on_message(filters.command("deldump"))
async def del_dump(_, msg):

    if msg.from_user.id in dump_channels:
        del dump_channels[msg.from_user.id]

    await msg.reply("✅ Dump Channel Deleted")

# ---------------- UPLOAD SYSTEM ---------------- #

upload_modes = {}
upload_bots = {}

@bot.on_message(filters.command("ub"))
async def upload_settings(_, msg):

    user_id = msg.from_user.id

    mode = upload_modes.get(user_id, "main").upper()

    selected_bot = upload_bots.get(user_id)

    if selected_bot:
        selected_text = "Token Set ✅"
    else:
        selected_text = "Not Set ❌"

    dump_id = dump_channels.get(user_id, "Not set")

    text = f"""
Cʜᴏᴏsᴇ ᴡʜɪᴄʜ ʙᴏᴛ sʜᴏᴜʟᴅ ᴜᴘʟᴏᴀᴅ ᴛʜᴇ ғɪɴɪsʜᴇᴅ ғɪʟᴇ

Modes:
• Main: All Renamed File upload via This Bot
• Personal: select your personal Upload bot for uploading files

• Current mode: {mode}
• Selected Upload: {selected_text}
• Dump channel: {dump_id}

Checks:
Main mode needs main bot access if you use dump so first make the bot admin!
Personal mode needs both main bot and chosen upload bot as admins in your dump channel
"""

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                f"MAIN {'✅' if mode == 'MAIN' else ''}",
                callback_data="ub_main"
            ),

            InlineKeyboardButton(
                f"PERSONAL {'✅' if mode == 'PERSONAL' else ''}",
                callback_data="ub_personal"
            )
        ],
        [
            InlineKeyboardButton(
                "UPLOAD BOTS",
                callback_data="ub_bots"
            )
        ],
        [
            InlineKeyboardButton(
                "ADD BOT",
                callback_data="ub_add"
            ),

            InlineKeyboardButton(
                "DELETE BOT",
                callback_data="ub_delete"
            )
        ],
        [
            InlineKeyboardButton(
                "CLOSE",
                callback_data="close"
            )
        ]
    ])

    await msg.reply_text(
        text,
        reply_markup=buttons
    )


# ---------------- ADD PERSONAL BOT ---------------- #

@bot.on_message(filters.command("addbot"))
async def add_bot(_, msg):

    user_id = msg.from_user.id

    if len(msg.command) < 2:
        return await msg.reply(
            "Usage:\n/addbot BOT_TOKEN"
        )

    token = msg.command[1]

    upload_bots[user_id] = token

    await msg.reply(
        "✅ Personal Upload Bot Saved"
    )


# ---------------- DELETE BOT ---------------- #

@bot.on_message(filters.command("delbot"))
async def del_bot(_, msg):

    user_id = msg.from_user.id

    if user_id in upload_bots:
        del upload_bots[user_id]

    await msg.reply(
        "❌ Personal Upload Bot Deleted"
    )

# ---------------- THUMB ----------------
@bot.on_message(filters.photo)
async def save_thumb(_, msg):

    await set_user(msg.from_user.id, {"thumb": msg.photo.file_id})
    await msg.reply("✅️ Tʜᴜᴍʙɴᴀɪʟ Sᴀᴠᴇᴅ")


@bot.on_message(filters.command("view_thumb"))
async def view_thumb(_, msg):

    user = await get_user(msg.from_user.id) or {}
    if user.get("thumb"):
        await msg.reply_photo(user["thumb"])
    else:
        await msg.reply("😔 Yᴏᴜ Dᴏɴ'ᴛ Hᴀᴠᴇ Aɴy Tʜᴜᴍʙɴᴀɪʟ")


@bot.on_message(filters.command("del_thumb"))
async def del_thumb(_, msg):

    await set_user(msg.from_user.id, {"thumb": ""})
    await msg.reply("❌️ Tʜᴜᴍʙɴᴀɪʟ Dᴇʟᴇᴛᴇᴅ")

# ---------------- FILE / VIDEO CHOOSER ----------------
@bot.on_message(filters.document | filters.video)
async def choose(_, msg):

    if await is_banned(msg.from_user.id):
        return await msg.reply("🚫 Yᴏᴜ Aʀᴇ Bᴀɴɴᴇᴅ.")
        # -------- FILE SIZE CHECK -------- #

    media = msg.document or msg.video

    if media.file_size > MAX_FILE_SIZE:
        return await msg.reply_text(
            f"❌ Fɪʟᴇ Tᴏᴏ Lᴀʀɢᴇ\n\n"
            f"📦 Mᴀx Sᴜᴘᴘᴏʀᴛᴇᴅ Sɪᴢᴇ: 2GB\n"
            f"📁 Yᴏᴜʀ Fɪʟᴇ: {humanbytes(media.file_size)}"
        )

    user_files[msg.from_user.id] = msg

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📄 𝗗𝗼𝗰𝘂𝗺𝗲𝗻𝘁", callback_data="file"),
            InlineKeyboardButton("🎬 𝗩𝗶𝗱𝗲𝗼 𝗠𝗼𝗱𝗲", callback_data="video")
        ]
    ])

    await msg.reply("𝗦𝗲𝗹𝗲𝗰𝘁 𝗧𝗵𝗲 𝗢𝘂𝘁𝗽𝘂𝘁 𝗙𝗶𝗹𝗲 𝗧𝘆𝗽𝗲:", reply_markup=buttons)

#---------- Cancel ------------#
@bot.on_message(filters.command("cancel"))
async def cancel_cmd(_, msg):
    user_id = msg.from_user.id

    if user_id in active_tasks and active_tasks[user_id]:
        active_tasks[user_id] = False
        await msg.reply("❌ Pʀᴏᴄᴇss Cᴀɴᴄᴇʟʟᴇᴅ Sᴜᴄᴄᴇssғᴜʟʟʏ")
    else:
        await msg.reply("⚠️ Nᴏ Aᴄᴛɪᴠᴇ Tᴀsᴋ Tᴏ Cᴀɴᴄᴇʟ")

#----------- Status ------------#

@bot.on_message(filters.command("status"))
async def status(_, msg):

    if msg.from_user.id != OWNER_ID:
        return 

    users_count = await users.count_documents({})

    if not await get_premium_status(msg.from_user.id):
        premium = "No"
    else:
        premium = "Yes"

    ping = await get_ping()

    text = f"""
📊 𝗕𝗼𝘁 𝗦𝘁𝗮𝘁𝘂𝘀

👥 Usᴇʀs: {users_count}
⏱ Uᴘᴛɪᴍᴇ: {get_uptime()}
⚡ Pɪɴɢ: {ping}
🧠 Mᴇᴍᴏʀʏ Usᴀɢᴇ: {get_memory()}
🧾 Vᴇʀsɪᴏɴ: v3.0
"""

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Rᴇғʀᴇsʜ", callback_data="status_refresh")]
    ])

    await msg.reply_text(text, reply_markup=buttons)

# ----------- BAN | UNBAN -------------- #

def is_admin(uid):
    return uid == OWNER_ID


@bot.on_message(filters.command("ban"))
async def ban(_, msg):

    if not is_admin(msg.from_user.id):
        return

    if len(msg.command) < 2:
        return await msg.reply(
            "Usage:\n/ban user_id"
        )

    try:
        uid = int(msg.command[1])

    except:
        return await msg.reply("❌ Invalid User ID")

    await set_user(uid, {"banned": True})

    log_event(f"User banned: {uid}")

    await msg.reply(f"🚫 User `{uid}` banned successfully")


@bot.on_message(filters.command("unban"))
async def unban(_, msg):

    if not is_admin(msg.from_user.id):
        return

    if len(msg.command) < 2:
        return await msg.reply(
            "Usage:\n/unban user_id"
        )

    try:
        uid = int(msg.command[1])

    except:
        return await msg.reply("❌ Invalid User ID")

    await set_user(uid, {"banned": False})

    log_event(f"User unbanned: {uid}")

    await msg.reply(f"✅ User `{uid}` unbanned successfully")
# ------------LOGS------------- #
@bot.on_message(filters.command("logs"))
async def logs(_, msg):

    if msg.from_user.id != OWNER_ID:
        return await msg.reply("❌ 𝗬𝗼𝘂 𝗮𝗿𝗲 𝗻𝗼𝘁 𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝘁𝗼 𝘂𝘀𝗲 𝘁𝗵𝗶𝘀 𝗰𝗼𝗺𝗺𝗮𝗻𝗱")

    try:
        with open("bot_logs.txt", "r", encoding="utf-8") as f:
            data = f.read()[-3000:]  # last logs only

        await msg.reply(f"📜 𝗕𝗢𝗧 𝗟𝗢𝗚𝗦:\n\n```{data}```")

    except:
        await msg.reply("𝗡𝗢 𝗟𝗢𝗚𝗦 𝗙𝗢𝗨𝗡𝗗 ❌")

# -------------BROADCAST------------ #
@bot.on_message(filters.command("broadcast"))
async def broadcast(_, msg):

    if msg.from_user.id != OWNER_ID:
        return

    if len(msg.command) < 2:
        return await msg.reply("𝗍𝗒𝗉𝖾 𝗐𝗂𝗍𝗁 /broadcast 𝗆𝖾𝗌𝗌𝖺𝗀𝖾")

    text = msg.text.split(None, 1)[1]

    total = 0
    success = 0
    failed = 0

    await msg.reply("⏳️ 𝖡𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍 𝖲𝗍𝖺𝗋𝗍𝖾𝖽.....")

    try:
        users_list = await get_all_users()   

        for user in users_list:              
            total += 1
            try:
                await bot.send_message(user["_id"], text)
                success += 1
            except:
                failed += 1

        await msg.reply(
            f"✅ 𝗕𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁 𝗖𝗼𝗺𝗽𝗹𝗲𝘁𝗲𝗱\n\n"
            f"◇ Tᴏᴛᴀʟ Usᴇʀs: {total}\n"
            f"◇ Sᴜᴄᴄᴇssғᴜʟ: {success}\n"
            f"◇ Uɴsᴜᴄᴄᴇssғᴜʟ: {failed}"
        )

    except Exception as e:
        await msg.reply(f"❌ 𝗕𝗿𝗼𝗮𝗱𝗰𝗮𝘀𝘁 𝗘𝗿𝗿𝗼𝗿: {e}")

# ---------- Callback --------------- #
@bot.on_callback_query()
async def cb(_, query: CallbackQuery):

    data = query.data

    try:

        if data == "home":

            user = query.from_user

            try:
                await query.message.edit_text(
                    get_home_text(user),
        reply_markup=get_home_buttons(),
                    parse_mode=ParseMode.HTML
                )
            except:
                await query.message.edit_text(
                    get_home_text(user),
        reply_markup=get_home_buttons()
                )

        elif data == "about":

            text = """

        ⍟───[ MY ᴅᴇᴛᴀɪʟꜱ ]───⍟

        Pʀᴏɢʀᴀᴍᴇʀ : <a href="https://t.me/Mr_Mohammed_29">ᴍᴏʜᴀᴍᴍᴇᴅ</a>
        ꜰᴏᴜɴᴅᴇʀ ᴏꜰ : <a href="https://t.me/Anime_UpdatesAU">ᴀɴɪᴍᴇ ᴜᴘᴅᴀᴛᴇs</a>
        Lɪʙʀᴀʀʏ : <a href="https://pypi.org/project/Pyrogram/">Pyʀᴏɢʀᴀᴍ 2.0</a>
        Lᴀɴɢᴜᴀɢᴇ : <a href="https://www.python.org/downloads/">Pʏᴛʜᴏɴ 𝟹</a>
        Dᴀᴛᴀʙᴀsᴇ : <a href="https://www.mongodb.com/">ᴍᴏɴɢᴏ ᴅʙ</a>
        ᴄʜᴀɴɴᴇʟ : <a href="https://t.me/Anime_UpdatesAU">ᴀɴɪᴍᴇ ᴜᴘᴅᴀᴛᴇs</a>
        ᴍʏ ꜱᴇʀᴠᴇʀ : <a href="https://t.me/AU_Bot_Discussion">ʙᴏᴛs sᴇʀᴠᴇʀ</a>
        ʙᴜɪʟᴅ sᴛᴀᴛᴜs : <a href="https://t.me/Anime_UpdatesAU">ᴠ3 [sᴛᴀʙʟᴇ]</a>
        """

            await query.message.edit_text(
                text,

        reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🏠 Hᴏᴍᴇ", callback_data="home")],
                    [InlineKeyboardButton("❌ Cʟᴏsᴇ", callback_data="close")]
                    ]),
                    disable_web_page_preview=True,
                    parse_mode=ParseMode.HTML
            )

        elif data == "source":
            await query.answer()
            await query.message.edit_text(
                "• 𝗥𝗲𝗽𝗼 •",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔗 𝗢𝗽𝗲𝗻 𝗦𝗼𝘂𝗿𝗰𝗲", url="https://github.com/MD-Developer-yt/Rename-Bot-2GB")]
             ])
            )

        elif data == "help":

            text = """
        𝗛𝗘𝗥𝗘 𝗜𝗦 𝗧𝗛𝗘 𝗛𝗘𝗟𝗣 𝗙𝗢𝗥 𝗠𝗬 𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦

        ›› 𝗛𝗼𝘄 𝗧𝗼 𝗦𝗲𝘁 𝗖𝗮𝗽𝘁𝗶𝗼𝗻

        ⦿ /set_caption - 𝖴𝗌𝖾 𝖳𝗁𝗂𝗌 𝖢𝗈𝗆𝗆𝖺𝗇𝖽 𝖳𝗈 𝖲𝖾𝗍 𝖸𝗈𝗎𝗋 𝖢𝖺𝗉𝗍𝗂𝗈𝗇
        ⦿ /see_caption - 𝖴𝗌𝖾 𝖳𝗁𝗂𝗌 𝖢𝗈𝗆𝗆𝖺𝗇𝖽 𝖳𝗈 𝖲𝖾𝖾 𝖸𝗈𝗎𝗋 𝖢𝖺𝗉𝗍𝗂𝗈𝗇
        ⦿ /del_caption - 𝖴𝗌𝖾 𝖳𝗁𝗂𝗌 𝖢𝗈𝗆𝗆𝖺𝗇𝖽 𝖳𝗈 𝖣𝖾𝗅𝖾𝗍𝖾 𝖸𝗈𝗎𝗋 𝖢𝖺𝗉𝗍𝗂𝗈𝗇

        ›› 𝗛𝗼𝘄 𝗧𝗼 𝗦𝗲𝘁 𝗧𝗵𝘂𝗺𝗯𝗻𝗮𝗶𝗹

        ⦿ 𝖸𝗈𝗎 𝖢𝖺𝗇 𝖠𝖽𝖽 𝖢𝗎𝗌𝗍𝗈𝗆 𝖳𝗁𝗎𝗆𝖻𝗇𝖺𝗂𝗅 𝖲𝗂𝗆𝗉𝗅𝗒 𝖡𝗒 𝖲𝖾𝗇𝖽𝗂𝗇𝗀 𝖠 𝖯𝗁𝗈𝗍𝗈 𝖳𝗈 𝖬𝖾
        ⦿ /view_thumb - 𝖲𝖾𝖾 𝖸𝗈𝗎𝗋 𝖳𝗁𝗎𝗆𝖻𝗇𝖺𝗂𝗅
        ⦿ /del_thumb - 𝖣𝖾𝗅𝖾𝗍𝖾 𝖸𝗈𝗎𝗋 𝖳𝗁𝗎𝗆𝖻𝗇𝖺𝗂𝗅

        ›› 𝗛𝗼𝘄 𝗧𝗼 𝗦𝗲𝘁 𝗣𝗿𝗲𝗳𝗶𝘅 & 𝗦𝘂𝗳𝗳𝗶𝘅

        ⦿ /set_prefix - ᴛᴏ ꜱᴇᴛ ᴀ ᴄᴜꜱᴛᴏᴍ ᴘʀᴇғɪx.
        ⦿ /see_prefix - ᴛᴏ ᴠɪᴇᴡ ʏᴏᴜʀ ᴄᴜꜱᴛᴏᴍ ᴘʀᴇғɪx
        ⦿ /del_prefix - ᴛᴏ ᴅᴇʟᴇᴛᴇ ʏᴏᴜʀ ᴄᴜꜱᴛᴏᴍ ᴘʀᴇғɪx

        ⦿ /set_suffix - ᴛᴏ ꜱᴇᴛ ᴀ ᴄᴜꜱᴛᴏᴍ ꜱᴜғғɪx.
        ⦿ /see_suffix - ᴛᴏ ᴠɪᴇᴡ ʏᴏᴜʀ ᴄᴜꜱᴛᴏᴍ ꜱᴜғғɪx.
        ⦿ /del_suffix - ᴛᴏ ᴅᴇʟᴇᴛᴇ ʏᴏᴜʀ ᴄᴜꜱᴛᴏᴍ ꜱᴜғғɪx.

        ›› 𝗛𝗼𝘄 𝗧𝗼 𝗦𝗲𝘁 𝗖𝘂𝘀𝘁𝗼𝗺 𝗠𝗲𝘁𝗮𝗱𝗮𝘁𝗮

        ⦿ /metadata - 𝖴𝗌𝖾 𝖳𝗁𝗂𝗌 𝖢𝗈𝗆𝗆𝖺𝗇𝖽 𝖳𝗈 𝖲𝖾𝗍 𝖢𝗎𝗌𝗍𝗈𝗆 𝖬𝖾𝗍𝖺𝖽𝖺𝖺
        """

            await query.message.edit_text(
                text,
        reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🏠 Hᴏᴍᴇ", callback_data="home")],
                    [InlineKeyboardButton("❌ Cʟᴏsᴇ", callback_data="close")]
                ])
            )

        elif data == "status_refresh":

            if query.from_user.id != OWNER_ID:
                return await query.answer("❌ 𝗬𝗼𝘂 𝗮𝗿𝗲 𝗻𝗼𝘁 𝗮𝘂𝘁𝗵𝗼𝗿𝗶𝘇𝗲𝗱 𝘁𝗼 𝘂𝘀𝗲 𝘁𝗵𝗶𝘀 𝗰𝗼𝗺𝗺𝗮𝗻𝗱", show_alert=True)

            await query.answer()

            users_count = await users.count_documents({})

            if not await get_premium_status(query.from_user.id):
                premium = "No"
            else:
                premium = "Yes"

            ping = await get_ping()

            text = f"""
        📊 𝗕𝗼𝘁 𝗦𝘁𝗮𝘁𝘂𝘀

        👥 Usᴇʀs: {users_count}
        ⏱ Uᴘᴛɪᴍᴇ: {get_uptime()}
        ⚡ Pɪɴɢ: {ping}
        🧠 Mᴇᴍᴏʀʏ Usᴀɢᴇ: {get_memory()}
        🧾 Vᴇʀsɪᴏɴ: v3.0
        """

            await query.message.edit_text(
                text,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Refresh", callback_data="status_refresh")]
                ])
            )

        elif data == "owner":
            await query.message.edit_text(f"👑 Owner ID: {OWNER_ID}")

        # ---------------- UPLOAD MODE CALLBACKS ---------------- #

        elif data == "ub_main":

            upload_modes[query.from_user.id] = "main"

            await query.answer(
                "Main Upload Mode Enabled"
            )

            mode = "MAIN"

            selected_bot = upload_bots.get(query.from_user.id)

            if selected_bot:
                selected_text = "Token Set ✅"
            else:
                selected_text = "Not Set ❌"

            dump_id = dump_channels.get(
                query.from_user.id,
                "Not set"
            )

            text = f"""
        Cʜᴏᴏsᴇ ᴡʜɪᴄʜ ʙᴏᴛ sʜᴏᴜʟᴅ ᴜᴘʟᴏᴀᴅ ᴛʜᴇ ғɪɴɪsʜᴇᴅ ғɪʟᴇ

        Modes:
        • Main: All Renamed File upload via This Bot
        • Personal: select your personal Upload bot for uploading files

        • Current mode: {mode}
        • Selected Upload: {selected_text}
        • Dump channel: {dump_id}

        Checks:
        Main mode needs main bot access if you use dump so first make the bot admin!
        Personal mode needs both main bot and chosen upload bot as admins in your dump channel
        """

            buttons = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "MAIN ✅",
                        callback_data="ub_main"
                    ),
 
                    InlineKeyboardButton(
                        "PERSONAL",
                        callback_data="ub_personal"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "UPLOAD BOTS",
                        callback_data="ub_bots"
                    )
                ],
                 
                [
                    InlineKeyboardButton(
                        "ADD BOT",
                        callback_data="ub_add"
                    ),
 
                    InlineKeyboardButton(
                        "DELETE BOT",
                        callback_data="ub_delete"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "CLOSE",
                        callback_data="close"
                    )
                ]
            ])

            await query.message.edit_text(
                text,
                reply_markup=buttons
            )


        elif data == "ub_personal":

            upload_modes[query.from_user.id] = "personal"

            await query.answer(
                "Personal Upload Mode Enabled"
            )

            mode = "PERSONAL"
   
            selected_bot = upload_bots.get(query.from_user.id)

            if selected_bot:
                selected_text = "Token Set ✅"
            else:
                selected_text = "Not Set ❌"

            dump_id = dump_channels.get(
                query.from_user.id,
                "Not set"
            )
 
            text = f"""
        Cʜᴏᴏsᴇ ᴡʜɪᴄʜ ʙᴏᴛ sʜᴏᴜʟᴅ ᴜᴘʟᴏᴀᴅ ᴛʜᴇ ғɪɴɪsʜᴇᴅ ғɪʟᴇ

        Modes:
        • Main: All Renamed File upload via This Bot
        • Personal: select your personal Upload bot for uploading files

        • Current mode: {mode}
        • Selected Upload: {selected_text}
        • Dump channel: {dump_id}

        Checks:
        Main mode needs main bot access if you use dump so first make the bot admin!
        Personal mode needs both main bot and chosen upload bot as admins in your dump channel
        """
 
            buttons = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "MAIN",
                        callback_data="ub_main"
                    ),
 
                    InlineKeyboardButton(
                        "PERSONAL ✅",
                        callback_data="ub_personal"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "UPLOAD BOTS",
                        callback_data="ub_bots"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "ADD BOT",
                        callback_data="ub_add"
                    ),

                    InlineKeyboardButton(
                        "DELETE BOT",
                        callback_data="ub_delete"
                    )
                ],
                [
                    InlineKeyboardButton(
                        "CLOSE",
                        callback_data="close"
                    )
                ]
            ])

            await query.message.edit_text(
                text,
                reply_markup=buttons
            )


        elif data == "ub_bots":

            selected_bot = upload_bots.get(query.from_user.id)

            if selected_bot:
                text = "✅ Personal Upload Bot Added"
            else:
                text = "❌ No Personal Upload Bot Added"

            await query.answer()

            await query.message.reply_text(text)


        elif data == "ub_add":

            await query.answer()

            await query.message.reply_text(
                "Send:\n/addbot BOT_TOKEN"
            )


        elif data == "ub_delete":

            user_id = query.from_user.id

            if user_id in upload_bots:
                del upload_bots[user_id]

            await query.answer(
                "Personal Upload Bot Deleted"
            )

            await query.message.reply_text(
                "❌ Personal Upload Bot Deleted"
            )

        elif data == "close":
            await query.message.delete()

        elif data.startswith("lb_"):

                    period = data.split("_")[1]

                    text = await generate_leaderboard(period)

                    buttons = InlineKeyboardMarkup([
                        [
                            InlineKeyboardButton("📅 Today", callback_data="lb_today"),
                            InlineKeyboardButton("📆 Weekly", callback_data="lb_weekly")
                        ],
                        [
                            InlineKeyboardButton("🗓 Monthly", callback_data="lb_monthly"),
                            InlineKeyboardButton("🏆 All Time", callback_data="lb_alltime")
                        ]
                    ])

                    await query.message.edit_text(
                        text,
                        reply_markup=buttons
                    )  

        elif data.startswith("cancel_"):

            uid = int(data.split("_")[1])

            active_tasks[uid] = False

            await query.message.edit_text("𝗣𝗿𝗼𝗰𝗲𝘀𝘀 𝗖𝗮𝗻𝗰𝗲𝗹𝗹𝗲𝗱")
            return

     # ----------- Callback -------------- #

        elif data in ["file", "video"]:

            user_id = query.from_user.id  
            user_mode[user_id] = data

            if await is_banned(user_id):
                return await query.answer("🚫 𝗕𝗮𝗻𝗻𝗲𝗱 𝗨𝘀𝗲𝗿", show_alert=True)

            if user_id not in user_files:
                return await query.answer("Eʀʀᴏʀ ‼️ Sᴇɴᴅ Fɪʟᴇ Aɢᴀɪɴ", show_alert=True)

            msg = user_files[user_id]  

            mode = user_mode.get(user_id, "file")

            active_tasks[user_id] = True

            file = msg.document or msg.video
            is_video = (
                msg.video is not None or
                (msg.document and str(msg.document.mime_type).startswith("video"))
            )  

            log_event(f"User {user_id} uploaded file: {file.file_name}")

            await query.message.edit_text(
                "📥 Dᴏᴡɴʟᴏᴀᴅɪɴɢ...",
        reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Cᴀɴᴄᴇʟ", callback_data=f"cancel_{user_id}")]
                ])
            )

            start_time = time.time()
            last_edit = 0

            async def dprog(current, total):

                global download_last_edit

                if not active_tasks.get(user_id):
                    raise Exception("Cancelled")

                now = time.time()

                # 🔥 prevent too frequent edits
                if now - download_last_edit < 1:
                    return
                download_last_edit = now

                percent, speed, eta = calc_progress(current, total, start_time)

                filled = int(percent / 10)
                bar = "⬢" * filled + "⬡" * (10 - filled)

                text = f"""
{bar}
📥 Dᴏᴡɴʟᴏᴀᴅɪɴɢ...

» 𝗗𝗼𝗻𝗲 : {round(percent, 1)}%
» 𝗦𝗶𝘇𝗲 : {humanbytes(current)} | {humanbytes(total)}
» 𝗦𝗽𝗲𝗲𝗱 : {humanbytes(speed)}/s
» 𝗘𝗧𝗔 : {time_formatter(eta)}
"""

                try:
                    await query.message.edit_text(text, parse_mode=ParseMode.HTML)
                except:
                    pass

            try:
                file_path = await msg.download(file_name=file.file_name, progress=dprog)
            except Exception as e:
                await query.message.edit_text("❌ Download Cancelled")
                return

            user = await get_user(user_id) or {}

            prefix = user.get("prefix", "")
            suffix = user.get("suffix", "")
            caption = user.get("caption", "")

            original_name = file.file_name if hasattr(file, "file_name") else "video.mp4"

            original_name = safe_name(original_name)

            base_name, ext = os.path.splitext(original_name)

            # -------- AUTO RENAME -------- #

            autorename = user.get("autorename", "")
            episode_no = int(user.get("episode", 1))

            quality = "Unknown"
            audio = "Unknown"

            name_lower = base_name.lower()

            # -------- QUALITY DETECT -------- #

            quality_list = [
                "480p",
                "720p",
                "1080p",
                "HDRip",
                "2160p",
                "4k"
            ]

            for q in quality_list:
                if q.lower() in name_lower:
                   quality = q
                   break

            # -------- AUDIO DETECT -------- #

            audio_list = [
                "Hindi",
                "Tamil",
                "Telugu",
                "English",
                "Japanese",
                "Chinese",
                "Malayalam",
                "Kannada",
                "Dual Audio",
                "Multi"
            ]

            for a in audio_list:
                if a.lower() in name_lower:
                    audio = a
                    break

            # -------- USE AUTO RENAME -------- #

            if autorename:

                try:

                    new_base = autorename.format(
                        season="01",
                        episode=str(episode_no).zfill(2),
                        quality=quality,
                        audio=audio
                    )

                    new_name = f"{new_base}{ext}"

                    # save next episode number
                    await set_user(
                        user_id,
                        {
                            "episode": episode_no + 1
                        }
                    )

                except Exception as e:

                    print("Autorename Error:", e)

                    if caption:
                        new_name = f"{caption}{ext}"
                    else:
                        new_name = f"{prefix}{base_name}{suffix}{ext}"

            # -------- NORMAL RENAME -------- #

            else:

                if caption:
                    new_name = f"{caption}{ext}"
                else:
                    new_name = f"{prefix}{base_name}{suffix}{ext}"
            output = f"temp_{user_id}_{new_name}"

            if any([
                user.get("title"),
                user.get("author"),
                user.get("artist"),
                user.get("audio"),
                user.get("subtitle"),
                user.get("video")
            ]):
                final = add_metadata(
                    file_path,
                    output,
                    user.get("title", ""),
                    user.get("author", ""),
                    user.get("artist", ""),
                    user.get("audio", ""),
                    user.get("subtitle", ""),
                    user.get("video", "")
                )
            else:
                final = file_path

            if not os.path.exists(final) or os.path.getsize(final) < 100000:
                final = file_path

            thumb = user.get("thumb")

        # -------- THUMB FIX -------- #
            thumb_path = None
            try:
                thumb_path = await get_thumbnail(
                    bot,
                    thumb,
                    is_video,
                    file_path,
                    user_id
                )
            except Exception as e:
                print("Thumbnail Error:", e)
                thumb_path = None

            # fallback safety
            if not thumb_path or not os.path.exists(thumb_path):
                thumb_path = None

        # -------- UPLOAD START -------- #
            await query.message.edit_text("📤 Uᴘʟᴏᴀᴅɪɴɢ sᴛᴀʀᴛᴇᴅ...")

            duration, width, height = (0, 0, 0)

            duration, width, height = get_video_metadata(final)

            start_time = time.time()
            last_edit = 0

            async def prog(current, total):

                global upload_last_edit

                if not active_tasks.get(user_id):
                    raise Exception("Cancelled")

                now = time.time()

                # 🔥 prevent spam edits
                if now - upload_last_edit < 1:
                    return
                upload_last_edit = now

                percent, speed, eta = calc_progress(current, total, start_time)

                filled = int(percent / 10)
                bar = "⬢" * filled + "⬡" * (10 - filled)

                text = f"""
{bar}
📤 Uᴘʟᴏᴀᴅɪɴɢ...

» 𝗗𝗼𝗻𝗲 : {round(percent, 1)}%
» 𝗦𝗶𝘇𝗲 : {humanbytes(current)} | {humanbytes(total)}
» 𝗦𝗽𝗲𝗲𝗱 : {humanbytes(speed)}/s
» 𝗘𝗧𝗔 : {time_formatter(eta)}
"""

                try:
                    await query.message.edit_text(text, parse_mode=ParseMode.HTML)
                except:
                    pass
           # -------- SEND FILE -------- #
            try:

               # -------- VIDEO MODE -------- #
                if mode == "video":

                    await msg.reply_video(
                        video=final,
                        caption=caption,
                        thumb=thumb_path,
                        duration=duration,
                        width=width,
                        height=height,
                        supports_streaming=True,
                        has_spoiler=False,
                        progress=prog
                    )

                    dump_id = dump_channels.get(user_id)

                    if dump_id:
                        try:
                            await bot.send_video(
                                chat_id=int(dump_id),
                                video=final,
                                caption=caption,
                                thumb=thumb_path,
                                duration=duration,
                                width=width,
                                height=height,
                                supports_streaming=True,
                            )

                        except Exception as e:
                            print("Dump Error:", e)

               # -------- DOCUMENT MODE -------- #
                else:

                    await msg.reply_document(
                        document=final,
                        file_name=new_name,
                        caption=caption,
                        thumb=thumb_path,
                        progress=prog
                    )

                    dump_id = dump_channels.get(user_id)

                    if dump_id:
                        try:
                            await bot.send_document(
                                chat_id=int(dump_id),
                                document=final,
                                file_name=new_name,
                                caption=caption,
                                thumb=thumb_path
                            )

                        except Exception as e:
                            print("Dump Error:", e)

            except Exception as e:

                await query.message.edit_text(
                    f"❌ Uᴘʟᴏᴀᴅ Cᴀɴᴄᴇʟʟᴇᴅ\n\n{str(e)}"
                )
                return

                try:
                    await query.message.edit_text(
                        "Eʀʀᴏʀ ‼️, Cᴏɴᴛᴀᴄᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ @Mr_Mohammed_29"
                    )

                except:
                    pass

                return


            # -------- CLEANUP -------- #

            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                if os.path.exists(final):
                    os.remove(final)
            except Exception:
                pass

            try:
                if thumb_path and os.path.exists(thumb_path):
                    os.remove(thumb_path)
            except Exception:
                pass

            # -------- UPDATE LEADERBOARD -------- #

            leaderboard_data["today"][user_id] += 1
            leaderboard_data["weekly"][user_id] += 1
            leaderboard_data["monthly"][user_id] += 1
            leaderboard_data["alltime"][user_id] += 1

            await query.message.delete()
            active_tasks.pop(user_id, None)
            user_mode.pop(user_id, None)

    except Exception as e:

        if "MESSAGE_NOT_MODIFIED" in str(e):
            return

        print("Callback Error:", e)

# ---------------- LEADERBOARD DATA ---------------- #

from collections import defaultdict

leaderboard_data = {
    "today": defaultdict(int),
    "weekly": defaultdict(int),
    "monthly": defaultdict(int),
    "alltime": defaultdict(int)
}

# ---------------- LEADERBOARD FUNCTION ---------------- #

async def generate_leaderboard(period):

    data = leaderboard_data.get(period, {})

    sorted_users = sorted(
        data.items(),
        key=lambda x: x[1],
        reverse=True
    )[:20]

    total_files = sum(data.values())

    text = f"📈 Lᴇᴀᴅᴇʀʙᴏᴀʀᴅ: {period.upper()}\n\n"
    text += "Tᴏᴘ 𝟸𝟶 Usᴇʀs Wɪᴛʜ Mᴏsᴛ Fɪʟᴇs Sᴏʀᴛᴇᴅ:\n\n"

    for uid, count in sorted_users:

        try:
            user = await bot.get_users(uid)

            name = user.first_name

            if len(name) > 25:
                name = name[:25]

        except:
            name = "Unknown"

        text += f"👤 « {name} » {count}\n"

    text += f"\nTᴏᴛᴀʟ Sᴏʀᴛᴇᴅ Fɪʟᴇs: {total_files}"

    return text


# ---------------- LEADERBOARD COMMAND ---------------- #

@bot.on_message(filters.private & filters.command("leaderboard"))
async def leaderboard(_, msg):

    text = await generate_leaderboard("today")

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📅 Today", callback_data="lb_today"),
            InlineKeyboardButton("📆 Weekly", callback_data="lb_weekly")
        ],
        [
            InlineKeyboardButton("🗓 Monthly", callback_data="lb_monthly"),
            InlineKeyboardButton("🏆 All Time", callback_data="lb_alltime")
        ]
    ])

    await msg.reply_text(
        text,
        reply_markup=buttons
    )
# ---------------- USER INFO ---------------- #

@bot.on_message(filters.private & filters.command("info"))
async def user_info(_, msg):

    user = msg.from_user

    try:
        photos = await bot.get_chat_photos(user.id, limit=1)
        has_photo = "ʏᴇs 🌠"
    except:
        has_photo = "ɴᴏ ❌"

    bio_text = "Nᴏ Bɪᴏ"

    try:
        full = await bot.get_users(user.id)

        if hasattr(full, "bio") and full.bio:
            bio_text = full.bio

    except:
        pass

    username = f"@{user.username}" if user.username else "Nᴏɴᴇ"

    text = f"""
👤 ᴜsᴇʀ ɪɴғᴏ
━━━━━━━━━━━━━━━
➣ ᴜsᴇʀ ɪᴅ: {user.id}
➣ ɴᴀᴍᴇ: {user.first_name}
➣ ᴜsᴇʀɴᴀᴍᴇ: {username}
➣ ʟᴀsᴛ sᴇᴇɴ: ⏱ ʀᴇᴄᴇɴᴛʟʏ
➣ ᴅᴀᴛᴀᴄᴇɴᴛᴇʀ ɪᴅ: {user.dc_id if user.dc_id else "Unknown"}
➣ ʟᴀɴɢᴜᴀɢᴇ: {user.language_code if user.language_code else "Unknown"}
━━━━━━━━━━━━━━━
➣ sᴄᴀᴍ ᴀᴄᴄᴏᴜɴᴛ: {"ʏᴇs ❌" if user.is_scam else "ɴᴏ ☑️"}
➣ ғᴀᴋᴇ ᴀᴄᴄᴏᴜɴᴛ: {"ʏᴇs ❌" if user.is_fake else "ɴᴏ ☑️"}
➣ ᴘʀᴏғɪʟᴇ ᴘɪᴄᴛᴜʀᴇ: {has_photo}
━━━━━━━━━━━━━━━
➣ ʙɪᴏ: {bio_text}
"""

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🌐 Vɪᴇᴡ Pʀᴏғɪʟᴇ",
                url=f"https://t.me/{user.username}"
            )
        ]
    ])

    await msg.reply_text(
        text,
        reply_markup=buttons
        )

# ---------------- DONATE ---------------- #

@bot.on_message(filters.private & filters.command("donate"))
async def donate(_, msg):

    text = """
💖 Sᴜᴘᴘᴏʀᴛ Tʜᴇ Bᴏᴛ

Iғ Yᴏᴜ Lɪᴋᴇ Tʜɪs Bᴏᴛ Aɴᴅ Wᴀɴᴛ
Tᴏ Sᴜᴘᴘᴏʀᴛ Tʜᴇ Dᴇᴠᴇʟᴏᴘᴇʀ,
Yᴏᴜ Cᴀɴ Dᴏɴᴀᴛᴇ ❤️

━━━━━━━━━━━━━━━

➣ ᴜᴘɪ ɪᴅ:
<code>mohammed.1006@superyes</code>

➣ ǫʀ ᴄᴏᴅᴇ:
<a href='https://telegra.ph/file/2197f68092b7161075d2d-34f98b9f2e12216868.jpg'>Click Here</a>

━━━━━━━━━━━━━━━

Aғᴛᴇʀ Pᴀʏᴍᴇɴᴛ Sᴇɴᴅ Sᴄʀᴇᴇɴsʜᴏᴛ
Tᴏ Dᴇᴠᴇʟᴏᴘᴇʀ
"""

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "💬 Cᴏɴᴛᴀᴄᴛ Dᴇᴠᴇʟᴏᴘᴇʀ",
                url="https://t.me/Mr_Mohammed_29"
            )
        ]
    ])

    await msg.reply_text(
        text,
        reply_markup=buttons,
        disable_web_page_preview=True
    )


# ---------------- CHAT ID ---------------- #

@bot.on_message(filters.private & filters.command("chatid"))
async def chatid(_, msg):

    text = f"""
🆔 Cʜᴀᴛ Iɴғᴏ

━━━━━━━━━━━━━━━
➣ Usᴇʀ ID: `{msg.from_user.id}`
➣ Cʜᴀᴛ ID: `{msg.chat.id}`
━━━━━━━━━━━━━━━
"""

    await msg.reply_text(text)

# ---------------- RUN ----------------
keep_alive()

print("BOT STARTED 🚀")
bot.run()

# ------------------------- #
# Don't Remove Credit 
# Ask Doubt @AU_Bot_Discussion 
# Owner @Mr_Mohammed_29 
# ------------------------- #
