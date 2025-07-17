import os
import asyncio
import yt_dlp
from time import time
from pyrogram import Client, filters
from pyrogram.types import Message
from youtube_search import YoutubeSearch
import requests
from BADMUSIC import app

user_last_message_time = {}
user_command_count = {}

SPAM_THRESHOLD = 2
SPAM_WINDOW_SECONDS = 5

COOKIES_FILE = "cookies/cookies.txt"

@app.on_message(filters.command("song"))
async def download_song(_, message: Message):
    user_id = message.from_user.id
    current_time = time()

    last_message_time = user_last_message_time.get(user_id, 0)
    if current_time - last_message_time < SPAM_WINDOW_SECONDS:
        user_last_message_time[user_id] = current_time
        user_command_count[user_id] = user_command_count.get(user_id, 0) + 1
        if user_command_count[user_id] > SPAM_THRESHOLD:
            warn = await message.reply_text(
                f"**{message.from_user.mention} ᴘʟᴇᴀsᴇ ᴅᴏɴᴛ sᴘᴀᴍ. ᴛʀʏ ᴀɢᴀɪɴ ᴀғᴛᴇʀ 5 sᴇᴄᴏɴᴅs.**"
            )
            await asyncio.sleep(3)
            await warn.delete()
            return
    else:
        user_command_count[user_id] = 1
        user_last_message_time[user_id] = current_time

    query = " ".join(message.command[1:])
    if not query:
        await message.reply("❗ Please provide a song name or YouTube URL.")
        return

    m = await message.reply("🔍 **Searching YouTube...**")
    ydl_opts = {
        "format": "bestaudio[ext=m4a]",
        "noplaylist": True,
        "quiet": True,
        "cookiefile": COOKIES_FILE,
        "outtmpl": "downloads/%(title).70s.%(ext)s"
    }

    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        if not results:
            await m.edit("⚠️ No results found.")
            return

        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"downloads/{title}.jpg"

        # Download thumbnail
        thumb = requests.get(thumbnail, allow_redirects=True)
        with open(thumb_name, "wb") as f:
            f.write(thumb.content)

        duration = results[0]["duration"]
        views = results[0]["views"]
        channel_name = results[0]["channel"]

        await m.edit("📥 **Downloading audio...**")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)
            audio_file = ydl.prepare_filename(info_dict)

        # Convert duration to seconds
        dur = sum(int(x) * 60 ** i for i, x in enumerate(reversed(duration.split(":"))))

        await m.edit("📤 **Uploading...**")
        await message.reply_audio(
            audio_file,
            thumb=thumb_name,
            title=title,
            caption=f"🎵 {title}\n👤 {message.from_user.mention}\n👁 {views}\n📺 {channel_name}",
            duration=dur
        )

        # Cleanup
        os.remove(audio_file)
        os.remove(thumb_name)
        await m.delete()

    except Exception as e:
        await m.edit("❌ **Failed to process query!**")
        print(f"[ERROR - /song] {e}")