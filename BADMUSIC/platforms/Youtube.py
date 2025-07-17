import asyncio
import glob
import os
import random
import re
from typing import Union

from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from youtubesearchpython.__future__ import VideosSearch
from yt_dlp import YoutubeDL

from config import TIME_ZONE
from BADMUSIC.utils.database import is_on_off
from BADMUSIC.utils.formatters import time_to_seconds, seconds_to_min
from BADMUSIC.utils.decorators import asyncify


def cookies() -> str:
    folder_path = os.path.join(os.getcwd(), "cookies")
    txt_files = glob.glob(os.path.join(folder_path, "*.txt"))
    if not txt_files:
        raise FileNotFoundError("No .txt cookie files found in cookies folder.")
    return os.path.join("cookies", os.path.basename(random.choice(txt_files)))


async def shell_cmd(cmd: str) -> str:
    proc = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    out, err = await proc.communicate()
    return (out or err).decode()


class YouTube:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.listbase = "https://youtube.com/playlist?list="

    async def exists(self, link: str, videoid: Union[bool, str] = None) -> bool:
        if videoid:
            link = self.base + link
        return bool(re.search(self.regex, link))

    @asyncify
    def url(self, message_1: Message) -> Union[str, None]:
        messages = [message_1]
        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)

        for message in messages:
            entities = message.entities or message.caption_entities
            if entities:
                for entity in entities:
                    if entity.type == MessageEntityType.TEXT_LINK:
                        return entity.url
                    elif entity.type == MessageEntityType.URL:
                        text = message.text or message.caption
                        return text[entity.offset : entity.offset + entity.length]
        return None

    async def details(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            title = result["title"]
            duration_min = result["duration"]
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            vidid = result["id"]
            duration_sec = int(time_to_seconds(duration_min)) if duration_min else 0
            return title, duration_min, duration_sec, thumbnail, vidid

    async def title(self, link: str, videoid: Union[bool, str] = None) -> str:
        if videoid:
            link = self.base + link
        results = VideosSearch(link.split("&")[0], limit=1)
        return (await results.next())["result"][0]["title"]

    async def duration(self, link: str, videoid: Union[bool, str] = None) -> str:
        if videoid:
            link = self.base + link
        results = VideosSearch(link.split("&")[0], limit=1)
        return (await results.next())["result"][0]["duration"]

    async def thumbnail(self, link: str, videoid: Union[bool, str] = None) -> str:
        if videoid:
            link = self.base + link
        results = VideosSearch(link.split("&")[0], limit=1)
        return (await results.next())["result"][0]["thumbnails"][0]["url"].split("?")[0]

    async def video(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        link = link.split("&")[0]
        cmd = [
            "yt-dlp",
            "-g",
            "-f",
            "bestaudio[ext=m4a]/bestaudio",
            "--cookies", cookies(),
            link,
        ]
        proc = await asyncio.create_subprocess_exec(
            *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        if stdout:
            return 1, stdout.decode().split("\n")[0]
        return 0, stderr.decode()

    async def playlist(self, link: str, limit: int = 30, videoid: Union[bool, str] = None):
        if videoid:
            link = self.listbase + link
        link = link.split("&")[0]
        cmd = (
            f"yt-dlp -i --compat-options no-youtube-unavailable-videos "
            f"--get-id --flat-playlist --playlist-end {limit} --skip-download \"{link}\""
        )
        playlist = await shell_cmd(cmd)
        return [vid for vid in playlist.strip().split("\n") if vid]