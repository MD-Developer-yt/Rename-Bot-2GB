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


def get_ping():
    return "200 ms"  

# ------------------------- #

from PIL import Image
from pyrogram import Client, filters

active_tasks = {}

import time

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
        "›› ᴛʜɪs ʙᴏᴛ ɪs ᴅᴇᴘʟᴏʏᴇᴅ ʙʏ: <a href='https://t.me/Mr_Mohammed_29'>ᴍᴏʜᴀᴍᴍᴇᴅ</a>",
    )


def get_home_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("• ᴍʏ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs •", callback_data='help')],
        [
            InlineKeyboardButton('ᴜᴘᴅᴀᴛᴇs', url=UPDATE_CHANNEL),
            InlineKeyboardButton('sᴜᴘᴘᴏʀᴛ', url=UPDATE_CHANNEL)
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

user_files = {}

print("LOG_CHANNEL:", LOG_CHANNEL)
print("UPDATE_CHANNEL:", UPDATE_CHANNEL)

from database import *
from utils import progress_bar
from ffmpeg_utils import add_metadata
from keep_alive import keep_alive

def humanbytes(size):
    if not size:
        return "0 B"
    power = 2**10
    n = 0
    Dic_powerN = {0: 'B', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
    while size > power:
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

def get_thumbnail(bot, user_thumb, is_video, file_path, user_id):

    import os

    if user_thumb:
        path = bot.download_media(user_thumb, file_name=f"thumb_{user_id}.jpg")
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

def calc_progress(current, total, start_time):
    now = time.time()
    diff = max(now - start_time, 0.1)

    percent = (current / total) * 100
    speed = current / diff
    eta = (total - current) / speed if speed > 0 else 0

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

# ------------------------- #

bot = Client(
    "rename-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ---------------- START ----------------
@bot.on_message(filters.command("start"))
async def start(_, message):

    if await is_banned(message.from_user.id):
        return await message.reply("🚫 Yᴏᴜ Aʀᴇ Bᴀɴɴᴇᴅ.")

    await add_user(message.from_user.id)

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
    except:
        pass

    await message.reply_text(
        get_home_text(user),
        reply_markup=get_home_buttons(),
        parse_mode="html"
    )

    except Exception as e:
        print("START ERROR:", e)
# ---------------- CAPTION ----------------
@bot.on_message(filters.command("set_caption"))
async def set_caption(_, msg):

    if await is_banned(msg.from_user.id):
        return await msg.reply("🚫 Yᴏᴜ Aʀᴇ Bᴀɴɴᴇᴅ.")
        
    cap = msg.text.split(None, 1)[1]
    await set_user(msg.from_user.id, {"caption": cap})
    await msg.reply("Cᴀᴘᴛɪᴏɴ Sᴀᴠᴇᴅ ✅️")

@bot.on_message(filters.command("see_caption"))
async def see_caption(_, msg):
    user = await get_user(msg.from_user.id) or {}
    await msg.reply(user.get("caption", "Nᴏ Cᴀᴘᴛɪᴏɴ Is Tʜᴇʀᴇ, Aᴅᴅ Nᴏᴡ"))

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

# -----------MY PlAN-------------- #
@bot.on_message(filters.command("myplan"))
async def myplan(_, msg):

    user = await get_user(msg.from_user.id) or {}
    status = "Premium" if user.get("premium") else "Free"

    if status == "Premium":
        text = f"✨ ʜᴇʏ {msg.from_user.first_name},\n\n"
        text += "💎 Yᴏᴜ ᴄᴜʀʀᴇɴᴛʟʏ ʜᴀᴠᴇ ᴀɴ ᴀᴄᴛɪᴠᴇ **Pʀᴇᴍɪᴜᴍ Pʟᴀɴ** ✔\n"
        text += "❤️ Tʜᴀɴᴋs Fᴏʀ Bᴜʏɪɴɢ Pʀᴇᴍɪᴜᴍ!"

    else:
        text = f"ʜᴇʏ {msg.from_user.first_name},\n\n"
        text += "𝒀𝒐𝒖 𝑫𝒐 𝑵𝒐𝒕 𝑯𝒂𝒗𝒆 𝑨𝒏𝒚 𝑨𝒄𝒕𝒊𝒗𝒆 𝑷𝒓𝒆𝒎𝒊𝒖𝒎 𝒑𝒍𝒂𝒏𝒔,\n"
        text += "𝑰𝒇 𝒀𝒐𝒖 𝑾𝒂𝒏𝒕 𝑻𝒐 𝑻𝒂𝒌𝒆 𝑷𝒓𝒆𝒎𝒊𝒖𝒎 𝑻𝒉𝒆𝒏 𝑪𝒍𝒊𝒄𝒌 𝑶𝒏 𝑩𝒆𝒍𝒐𝒘 𝑩𝒖𝒕𝒕𝒐𝒏 👇"

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("○ Bᴜʏ Pʀᴇᴍɪᴜᴍ ○", url="https://t.me/Mr_Mohammed_29")
        ]
    ])

# ------------ plans ---------------#
@bot.on_message(filters.command("plans"))
async def plans(_, msg):

    text = f"""
👋 ʜᴇʏ {msg.from_user.first_name},

🎁 ᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇs :

››  ᴜɴʟɪᴍɪᴛᴇᴅ ʀᴇɴᴀᴍɪɴɢ: ɴᴏ ʟɪᴍɪᴛꜱ ᴏɴ ꜰɪʟᴇꜱ  
››  ᴇᴀʀʟʏ ᴀᴄᴄᴇꜱꜱ: ᴛʀʏ ɴᴇᴡ ꜰᴇᴀᴛᴜʀᴇꜱ ꜰɪʀꜱᴛ  
››  ꜰᴀꜱᴛᴇʀ ꜱᴘᴇᴇᴅ: Qᴜɪᴄᴋᴇʀ ᴅᴏᴡɴʟᴏᴀᴅꜱ ᴀɴᴅ ᴜᴘʟᴏᴀᴅꜱ  

➛ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴀᴄᴛɪᴠᴇ ᴘʟᴀɴ ʙʏ ᴜꜱɪɴɢ : /myplan
"""

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("○ Uᴘɢʀᴀᴅᴇ Tᴏ Pʀᴇᴍɪᴜᴍ ○", url="https://t.me/Mr_Mohammed_29")
        ]
    ])

    await msg.reply(text, reply_markup=buttons)
    
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
        
    user_files[msg.from_user.id] = msg
    
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📄 𝗗𝗼𝗰𝘂𝗺𝗲𝗻𝘁", callback_data="file"),
            InlineKeyboardButton("🎬 𝗩𝗶𝗱𝗲𝗼 𝗠𝗼𝗱𝗲", callback_data="video")
        ]
    ])

    await msg.reply("𝗦𝗲𝗹𝗲𝗰𝘁 𝗧𝗵𝗲 𝗢𝘂𝘁𝗽𝘂𝘁 𝗙𝗶𝗹𝗲 𝗧𝘆𝗽𝗲:", reply_markup=buttons)

# ---------------- ADMIN ----------------
def admin(uid):
    return uid == OWNER_ID

@bot.on_message(filters.command("addpremium"))
async def addprem(_, msg):

    if not admin(msg.from_user.id):
        return

    if len(msg.command) < 3:
        return await msg.reply("𝗿𝗲𝗽𝗹𝘆 𝘄𝗶𝘁𝗵 /addpremium 𝘂𝘀𝗲𝗿 𝗶𝗱 𝗱𝘂𝗿𝗮𝘁𝗶𝗼𝗻 (𝟭𝗵𝗿, 𝟳𝗱, 𝟯𝟬𝗱, 𝟭𝘆𝗿)")

    uid = int(msg.text.split()[1])
    duration = msg.text.split()[2]

    seconds = parse_duration(duration)

    if not seconds:
        return await msg.reply("𝗜𝗻𝘃𝗮𝗹𝗶𝗱 𝗙𝗼𝗿𝗺𝗮𝘁 ❌ 𝗨𝘀𝗲 : 1hr / 7d / 30d / 1y")

    expiry = int(time.time()) + seconds

    await set_user(uid, {
        "premium": True,
        "premium_expiry": expiry
    })

    await msg.reply(f"""
🎉 𝗬𝗼𝘂 𝗮𝗿𝗲 𝗻𝗼𝘄 𝗮 𝗣𝗿𝗲𝗺𝗶𝘂𝗺 𝗨𝘀𝗲𝗿!

👤 Usᴇʀ ID: {uid}
⏳ Dᴜʀᴀᴛɪᴏɴ: {duration}
🕒 Exᴘɪʀᴇs Iɴ: {duration}

✨ Sᴛᴀᴛᴜs: 𝗣𝗿𝗲𝗺𝗶𝘂𝗺 𝗔𝗰𝘁𝗶𝘃𝗮𝘁𝗲𝗱 ✅️
""")

@bot.on_message(filters.command("remove_premium"))
async def remprem(_, msg):
    if not admin(msg.from_user.id):
        return
    uid = int(msg.text.split()[1])
    await set_user(uid, {"premium": False})
    await msg.reply("𝗣𝗿𝗲𝗺𝗶𝘂𝗺 𝗥𝗲𝗺𝗼𝘃𝗲𝗱")

@bot.on_message(filters.command("status"))
async def status(_, msg):

    users_count = await users.count_documents({})
    
    if not await get_premium_status(msg.from_user.id):
        premium = "No"
    else:
        premium = "Yes"

    text = f"""
📊 𝗕𝗼𝘁 𝗦𝘁𝗮𝘁𝘂𝘀

👥 Usᴇʀs: {users_count}
⏱ Uᴘᴛɪᴍᴇ: {get_uptime()}
⚡ Pɪɴɢ: {get_ping()}
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
    uid = int(msg.text.split()[1])
    await set_user(uid, {"banned": True})
    await msg.reply("‼️ 𝗨𝘀𝗲𝗿 𝗜𝘀 𝗕𝗮𝗻𝗻𝗲𝗱")

@bot.on_message(filters.command("unban"))
async def unban(_, msg):
    if not is_admin(msg.from_user.id):
        return
    uid = int(msg.text.split()[1])
    await set_user(uid, {"banned": False})
    await msg.reply("😁 𝗨𝘀𝗲𝗿 𝗜𝘀 𝗨𝗻𝗯𝗮𝗻𝗻𝗲𝗱")

# ------------LOGS------------- #
@bot.on_message(filters.command("logs"))
async def logs(_, msg):
    if msg.from_user.id != OWNER_ID:
        return
    await msg.reply("Logs system active (connect DB logging if needed)")

# -------------BROADCAST------------ #
@bot.on_message(filters.command("broadcast"))
async def broadcast(_, msg):

    if msg.from_user.id != OWNER_ID:
        return

    if len(msg.command) < 2:
        return await msg.reply("Usage: /broadcast message")

    text = msg.text.split(None, 1)[1]

    total = 0
    success = 0
    failed = 0

    users_list = get_all_users()

    async for user in users_list:
        total += 1
        try:
            await bot.send_message(user["_id"], text)
            success += 1
        except:
            failed += 1

    await msg.reply(
        f"📢 Broadcast Completed ✔\n\n"
        f"◇ Total Users: {total}\n"
        f"◇ Successful: {success}\n"
        f"◇ Unsuccessful: {failed}"
    )
# ---------- Callback --------------- #
@bot.on_callback_query()
async def cb(_, query: CallbackQuery):

    data = query.data

    try:

        if data == "home":

            user = query.from_user

            await query.message.edit_text(
                get_home_text(user),
                reply_markup=get_home_buttons(),
                parse_mode="html"
            )
            
        elif data == "about":

            text = """

        ⍟───[ MY ᴅᴇᴛᴀɪʟꜱ ]───⍟

        Pʀᴏɢʀᴀᴍᴇʀ : <a href="https://t.me/Mr_Mohammed_29">ᴍᴏʜᴀᴍᴍᴇᴅ</a>
        ꜰᴏᴜɴᴅᴇʀ ᴏꜰ : <a href="https://t.me/Anime_UpdatesAU">ᴀɴɪᴍᴇ ᴜᴘᴅᴀᴛᴇs</a>
        Lɪʙʀᴀʀʏ : <a href="https://pypi.org/project/Pyrogram/">Pyʀᴏɢʀᴀᴍ 2.0</a>
        Lᴀɴɢᴜᴀɢᴇ : <a href="https://www.python.org/downloads/">Pʏᴛʜᴏɴ 𝟹</a>
        Dᴀᴛᴀʙᴀsᴇ : <a href="https://www.mongodb.com/">ᴍᴏɴɢᴏ ᴅʙ</a>
        ᴄʜᴀɴɴᴇʟ : <a href="https://t.me/Anime_Updates">ᴀɴɪᴍᴇ ᴜᴘᴅᴀᴛᴇs</a>
        ᴍʏ ꜱᴇʀᴠᴇʀ : <a href="https://t.me/AU_Bot_Discussion">ʙᴏᴛs sᴇʀᴠᴇʀ</a>
        ʙᴜɪʟᴅ sᴛᴀᴛᴜs : <a href="https://t.me/Anime_UpdatesAU">ᴠ3 [sᴛᴀʙʟᴇ]</a>
        """

            await query.message.edit_text(
                text,
                
        reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🏠 Home", callback_data="home")],
                    [InlineKeyboardButton("❌ Close", callback_data="close")]
                    ]),
                    disable_web_page_preview=True,
                    parse_mode="html"
            )

        elif data == "source":
            await query.answer()
            await query.message.edit_text(
                "💻 Source Code",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔗 Open Source", url="https://github.com/Naruto-Uzumaki-Yt/rename-bot")]
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
                    [InlineKeyboardButton("🏠 Home", callback_data="home")],
                    [InlineKeyboardButton("❌ Close", callback_data="close")]
                ])
            )

        elif data == "status_refresh":

            users_count = await users.count_documents({})

            text = f"""
        📊 𝗕𝗼𝘁 𝗦𝘁𝗮𝘁𝘂𝘀

        👥 Usᴇʀs: {users_count}
        ⏱ Uᴘᴛɪᴍᴇ: {get_uptime()}
        ⚡ Pɪɴɢ: {get_ping()}
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

        elif data == "close":
            await query.message.delete()

        elif data.startswith("cancel_"):

            uid = int(data.split("_")[1])

            active_tasks[uid] = False

            await query.message.edit_text("❌ Process Cancelled")
            return
            
     # ----------- Callback -------------- #
            
        elif data in ["file", "video"]:

            user_id = query.from_user.id  

            if await is_banned(user_id):
                return await query.answer("🚫 Banned user", show_alert=True)

            if user_id not in user_files:
                return await query.answer("Send file again ❌", show_alert=True)

            msg = user_files[user_id]   

            active_tasks[user_id] = True
 
            file = msg.document or msg.video
            is_video = msg.video is not None  

            await query.message.edit_text(
                "⬡⬡⬡⬡⬡⬡⬡⬡⬡⬡\n📥 Downloading...",
        reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("❌ Cancel", callback_data=f"cancel_{user_id}")]
                ])
            )

            start_time = time.time()

            async def dprog(current, total):
                if not active_tasks.get(user_id):
                    raise Exception("Cancelled")

                now = time.time()
                diff = now - start_time

                percent, speed, eta = calc_progress(current, total, start_time)

                filled = int(percent / 10)
                bar = "⬢" * filled + "⬡" * (10 - filled)

                text = f"""{bar}
 📥 Downloading...

<b>» Done</b> : {round(percent, 2)}%
<b>» Size</b> : {humanbytes(current)} | {humanbytes(total)}
<b>» Speed</b> : {humanbytes(speed)}/s
<b>» ETA</b> : {time_formatter(eta)}
"""

                await query.message.edit_text(text)

            file_path = await msg.download(file_name=file.file_name, progress=dprog)

            user = await get_user(user_id) or {}

            prefix = user.get("prefix", "")
            suffix = user.get("suffix", "")
            caption = user.get("caption", "")

            original_name = file.file_name if hasattr(file, "file_name") else "video.mp4"

            original_name = safe_name(original_name)

            new_name = f"{prefix}{original_name}{suffix}"
            output = f"temp_{user_id}_{original_name}"
            
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

            thumb = user.get("thumb")

            thumb_path = get_thumbnail(
                bot,
                thumb,
                is_video,
                file_path,
                user_id
            )

            await query.message.edit_text("⬡⬡⬡⬡⬡⬡⬡⬡⬡⬡\n📤 Uploading...")

            start_time = time.time()

            async def prog(current, total):
                if not active_tasks.get(user_id):
                    return

                now = time.time()
                diff = now - start_time

                percent, speed, eta = calc_progress(current, total, start_time)

                filled = int(percent / 10)
                bar = "⬢" * filled + "⬡" * (10 - filled)

                text = f"""{bar}

<b>» Done</b> : {round(percent, 2)}%
<b>» Size</b> : {humanbytes(current)} | {humanbytes(total)}
<b>» Speed</b> : {humanbytes(speed)}/s
<b>» ETA</b> : {time_formatter(eta)}
"""

                await query.message.edit_text(text)

            if is_video:
                await msg.reply_video(
                    video=final,
                    caption=caption,
                    thumb=thumb_path,
                    progress=prog
                )
            else:
                await msg.reply_document(
                    document=final,
                    file_name=new_name,
                    caption=caption,
                    thumb=thumb_path,
                    progress=prog
                )

            try:
                os.remove(file_path)
                os.remove(final)
            except:
                pass

            if thumb_path and os.path.exists(thumb_path):
                os.remove(thumb_path)

            await query.message.delete()
            active_tasks.pop(user_id, None)

    except Exception as e:
        print("Callback Error:", e)
        await query.answer("Error ⚠️", show_alert=True)
                
# ---------------- RUN ----------------
keep_alive()

print("BOT STARTED 🚀")
bot.run()

# ------------------------- #
# Don't Remove Credit 
# Ask Doubt @AU_Bot_Discussion 
# Owner @Mr_Mohammed_29 
# ------------------------- #
