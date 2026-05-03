# ------------------------- #
# Don't Remove Credit 
# Ask Doubt @AU_Bot_Discussion 
# Owner @Mr_Mohammed_29 
# ------------------------- #
import os
import time
import asyncio
import ffmpeg
from PIL import Image
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
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
            return await message.reply("🚫 You are banned from using this bot.")

        await add_user(message.from_user.id)
    
        user = message.from_user

    try:
        m = await message.reply_text("Jɪɴᴡᴏᴏ Sᴜɴɢ . .")
        await asyncio.sleep(0.5)
        await m.edit_text("🎊")
        await asyncio.sleep(0.5)
        await m.edit_text("⚡")
        await asyncio.sleep(0.5)
        await m.edit_text("Mᴀsᴛᴇʀ...")
        await asyncio.sleep(0.4)
        await m.delete()

        # sticker
        try:
            await message.reply_sticker(
                "CAACAgUAAxkBAAEXm-JplJOyujCdKOZhh8m5gC4BJpW52AACaxwAA2epVnjNNttcc5jLHgQ"
            )
        except:
            pass

        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("• ᴍʏ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs •", callback_data='help')],
            [
                InlineKeyboardButton('• ᴜᴘᴅᴀᴛᴇs', url=UPDATE_CHANNEL),
                InlineKeyboardButton('sᴜᴘᴘᴏʀᴛ •', url=UPDATE_CHANNEL)
            ],
            [
                InlineKeyboardButton('• ᴀʙᴏᴜᴛ', callback_data='about'),
                InlineKeyboardButton('sᴏᴜʀᴄᴇ •', callback_data='source')
            ]
        ])

        await message.reply_text(
            f"👋 Hello {user.mention}\n\n🤖 Welcome to Rename Bot\nSend file to start.",
            reply_markup=buttons,
            disable_web_page_preview=True
        )

    except Exception as e:
        print("START ERROR:", e)
# ---------------- CAPTION ----------------
@bot.on_message(filters.command("set_caption"))
async def set_caption(_, msg):

    if await is_banned(msg.from_user.id):
        return await msg.reply("🚫 You are banned from using this bot.")
        
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
@bot.on_message(filters.command("see_prefix"))
async def see_prefix(_, msg):
    user = await get_user(msg.from_user.id) or {}
    prefix = user.get("prefix")

    if not prefix:
        return await msg.reply("Prefix is not set ❌")

    await msg.reply(f"Current prefix: `{prefix}`")


@bot.on_message(filters.command("del_prefix"))
async def del_prefix(_, msg):
    await set_user(msg.from_user.id, {"prefix": ""})
    await msg.reply("Prefix deleted ✔")


@bot.on_message(filters.command("see_suffix"))
async def see_suffix(_, msg):
    user = await get_user(msg.from_user.id) or {}
    suffix = user.get("suffix")

    if not suffix:
        return await msg.reply("Suffix is not set ❌")

    await msg.reply(f"Current suffix: `{suffix}`")


@bot.on_message(filters.command("del_suffix"))
async def del_suffix(_, msg):
    await set_user(msg.from_user.id, {"suffix": ""})
    await msg.reply("Suffix deleted ✔")

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

# -----------MY PlAN-------------- #
@bot.on_message(filters.command("myplan"))
async def myplan(_, msg):
    user = await get_user(msg.from_user.id) or {}
    status = "Premium" if user.get("premium") else "Free"
    await msg.reply(f"Your plan: {status}")

@bot.on_message(filters.command("plans"))
async def plans(_, msg):
    await msg.reply("Upgrade to Premium Plan 🚀")

# ---------------- METADATA SETTERS ----------------
@bot.on_message(filters.command("settitle"))
async def settitle(_, msg):
    if len(msg.command) < 2:
        return await msg.reply("Usage: /settitle text")

    text = msg.text.split(None, 1)[1]
    await set_user(msg.from_user.id, {"title": text})
    await msg.reply("Title is saved ✔")


@bot.on_message(filters.command("setauthor"))
async def setauthor(_, msg):
    if len(msg.command) < 2:
        return await msg.reply("Usage: /setauthor text")

    text = msg.text.split(None, 1)[1]
    await set_user(msg.from_user.id, {"author": text})
    await msg.reply("Author is saved ✔")


@bot.on_message(filters.command("setartist"))
async def setartist(_, msg):
    if len(msg.command) < 2:
        return await msg.reply("Usage: /setartist text")

    text = msg.text.split(None, 1)[1]
    await set_user(msg.from_user.id, {"artist": text})
    await msg.reply("Artist is saved ✔")


@bot.on_message(filters.command("setaudio"))
async def setaudio(_, msg):
    if len(msg.command) < 2:
        return await msg.reply("Usage: /setaudio text")

    text = msg.text.split(None, 1)[1]
    await set_user(msg.from_user.id, {"audio": text})
    await msg.reply("Audio is saved ✔")


@bot.on_message(filters.command("setsubtitle"))
async def setsubtitle(_, msg):
    if len(msg.command) < 2:
        return await msg.reply("Usage: /setsubtitle text")

    text = msg.text.split(None, 1)[1]
    await set_user(msg.from_user.id, {"subtitle": text})
    await msg.reply("Subtitle is saved ✔")


@bot.on_message(filters.command("setvideo"))
async def setvideo(_, msg):
    if len(msg.command) < 2:
        return await msg.reply("Usage: /setvideo text")

    text = msg.text.split(None, 1)[1]
    await set_user(msg.from_user.id, {"video": text})
    await msg.reply("Video metadata is saved ✔")
# ---------------- THUMB ----------------
@bot.on_message(filters.photo)
async def save_thumb(_, msg):
    await set_user(msg.from_user.id, {"thumb": msg.photo.file_id})
    await msg.reply("Thumbnail saved ✔")


@bot.on_message(filters.command("view_thumb"))
async def view_thumb(_, msg):
    user = await get_user(msg.from_user.id) or {}
    if user.get("thumb"):
        await msg.reply_photo(user["thumb"])
    else:
        await msg.reply("No thumbnail found")


@bot.on_message(filters.command("del_thumb"))
async def del_thumb(_, msg):
    await set_user(msg.from_user.id, {"thumb": ""})
    await msg.reply("Thumbnail deleted ✔")

# ---------------- FILE / VIDEO CHOOSER ----------------
@bot.on_message(filters.document | filters.video)
async def choose(_, msg):
    
    user_files[msg.from_user.id] = msg
    
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📄 File Mode", callback_data="file"),
            InlineKeyboardButton("🎬 Video Mode", callback_data="video")
        ]
    ])

    await msg.reply("Choose mode:", reply_markup=buttons)

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

# ----------- BAN | UNBAN -------------- #
def is_admin(uid):
    return uid == OWNER_ID

@bot.on_message(filters.command("ban"))
async def ban(_, msg):
    if not is_admin(msg.from_user.id):
        return
    uid = int(msg.text.split()[1])
    await set_user(uid, {"banned": True})
    await msg.reply("User banned")

@bot.on_message(filters.command("unban"))
async def unban(_, msg):
    if not is_admin(msg.from_user.id):
        return
    uid = int(msg.text.split()[1])
    await set_user(uid, {"banned": False})
    await msg.reply("User unbanned")

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

    users_list = users.find({})

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
            await query.message.edit_text("🏠 Home Menu")

        elif data == "about":
            await query.message.edit_text(
                "ℹ️ Rename Bot\n\n"
                "Features:\n"
                "• File Rename\n"
                "• Metadata Engine\n"
                "• Thumbnail Support\n"
                "• FFmpeg Processing"
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
            await query.message.edit_text(
                "📖 Help Menu\n\n"
                "/set_caption\n"
                "/set_prefix\n"
                "/set_suffix\n"
                "/metadata"
            )

        elif data == "owner":
            await query.message.edit_text(f"👑 Owner ID: {OWNER_ID}")

        elif data == "close":
            await query.message.delete()
            
        elif data in ["file", "video"]:

            user_id = query.from_user.id

            if user_id not in user_files:
                return await query.answer("Send file again ❌", show_alert=True)

            msg = user_files[user_id]
            file = msg.document or msg.video

            await query.message.edit_text("⬡⬡⬡⬡⬡⬡⬡⬡⬡⬡\n📥 Downloading...")

            start_time = time.time()

            async def dprog(current, total):
                try:
                    now = time.time()
                    diff = now - start_time

                    percent = current * 100 / total
                    speed = current / diff if diff > 0 else 0
                    eta = (total - current) / speed if speed > 0 else 0

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

                except:
                    pass

            file_path = await msg.download(file_name=file.file_name, progress=dprog)

            user = await get_user(user_id) or {}

            prefix = user.get("prefix", "")
            suffix = user.get("suffix", "")
            caption = user.get("caption", "")

            original_name = file.file_name if hasattr(file, "file_name") else "video.mp4"
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
            thumb_path = None

            # If user set thumb
            if thumb:
                thumb_path = await bot.download_media(thumb, file_name=f"thumb_{user_id}.jpg")
                thumb_path = smart_thumb(thumb_path)

            # If no thumb and video → auto generate
            elif data == "video":
                thumb_path = f"auto_thumb_{user_id}.jpg"
                thumb_path = generate_video_thumb(file_path, thumb_path)

            await query.message.edit_text("⬡⬡⬡⬡⬡⬡⬡⬡⬡⬡\n📤 Uploading...")

            start_time = time.time()

            async def prog(current, total):
                try:
                    now = time.time()
                    diff = now - start_time

                    percent = current * 100 / total
                    speed = current / diff if diff > 0 else 0
                    eta = (total - current) / speed if speed > 0 else 0

                    filled = int(percent / 10)
                    bar = "⬢" * filled + "⬡" * (10 - filled)

                    text = f"""{bar}

            <b>» Done</b> : {round(percent, 2)}%
            <b>» Size</b> : {humanbytes(current)} | {humanbytes(total)}
            <b>» Speed</b> : {humanbytes(speed)}/s
            <b>» ETA</b> : {time_formatter(eta)}
            """

                    await query.message.edit_text(text)

                except:
                    pass

            if data == "video":
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

            try:
                if thumb_path and os.path.exists(thumb_path):
                   os.remove(thumb_path)
            except:
                pass

            try:
                await query.message.delete()
            except:
                pass

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
