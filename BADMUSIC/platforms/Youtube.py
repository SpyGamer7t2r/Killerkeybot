import re
import aiohttp
from youtubesearchpython.__future__ import VideosSearch
from yt_dlp import YoutubeDL


class YouTube:
    async def track(self, query: str):
        try:
            # Search YouTube
            results = VideosSearch(query, limit=1)
            result = (await results.next())["result"][0]

            title = result["title"]
            duration = result["duration"]
            views = result["viewCount"]["short"]
            thumbnail = result["thumbnails"][0]["url"]
            channel = result["channel"]["name"]
            link = result["link"]
            video_id = result["id"]

            details = {
                "title": title,
                "duration": duration,
                "views": views,
                "thumbnail": thumbnail,
                "channel": channel,
                "link": link,
            }

            return details, video_id
        except Exception as e:
            print(f"[YouTube.track] Error: {e}")
            return None, None

    async def playlist(self, url: str):
        try:
            ydl_opts = {
                "extract_flat": True,
                "quiet": True,
                "force_generic_extractor": True,
            }
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
            return info.get("entries", [])
        except Exception as e:
            print(f"[YouTube.playlist] Error: {e}")
            return []
class YouTube:
    async def url(self, message):
        try:
            # Agar user directly YouTube link bhejta hai
            if message.text:
                urls = re.findall(r"(https?://\S+)", message.text)
                if urls:
                    return urls[0]
            return None
        except Exception as e:
            print(f"[YouTube.url] Error: {e}")
            return None

    async def track(self, query: str):
        try:
            results = VideosSearch(query, limit=1)
            result = (await results.next())["result"][0]

            title = result["title"]
            duration = result["duration"]
            views = result["viewCount"]["short"]
            thumbnail = result["thumbnails"][0]["url"]
            channel = result["channel"]["name"]
            link = result["link"]
            video_id = result["id"]

            details = {
                "title": title,
                "duration": duration,
                "views": views,
                "thumbnail": thumbnail,
                "channel": channel,
                "link": link,
            }

            return details, video_id
        except Exception as e:
            print(f"[YouTube.track] Error: {e}")
            return None, None

    async def playlist(self, url: str):
        try:
            ydl_opts = {
                "extract_flat": True,
                "quiet": True,
                "force_generic_extractor": True,
            }
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
            return info.get("entries", [])
        except Exception as e:
            print(f"[YouTube.playlist] Error: {e}")
            return []