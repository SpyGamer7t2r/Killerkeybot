import asyncio
import os
import re
import shutil
import yt_dlp
from BADMUSIC import config
from BADMUSIC.utils.logger import log
from BADMUSIC.utils.helpers import run_subprocess, cookies

class YouTubeAPI:
    def __init__(self):
        self.cookie_path = cookies()

    async def video(self, link: str):
        cmd = [
            "yt-dlp",
            "-g",
            "-f",
            "(bestvideo[ext=mp4][height<=720]+bestaudio[ext=m4a])/best[ext=mp4]",
            "--cookies", self.cookie_path,
            link,
        ]
        try:
            output = await run_subprocess(cmd)
            urls = output.strip().split("\n")  # 🛠 fixed string here
            if len(urls) >= 2:
                return {"video": urls[0], "audio": urls[1]}
            elif len(urls) == 1:
                return {"video": urls[0], "audio": urls[0]}
            return None
        except Exception as e:
            log.warning(f"Failed to fetch direct video links: {e}")
            return None

    async def video_dl(self, link: str, output: str = "downloads/video.mp4"):
        try:
            ydl_opts = {
                "outtmpl": output,
                "quiet": True,
                "format": "(bestvideo[ext=mp4][height<=720]+bestaudio[ext=m4a])/best[ext=mp4]",
                "merge_output_format": "mp4",
                "noplaylist": True,
                "cookies": self.cookie_path,
                "no_warnings": True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
            return output if os.path.exists(output) else None
        except Exception as e:
            log.warning(f"Download failed: {e}")
            return None