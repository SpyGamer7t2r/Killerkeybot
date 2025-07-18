import asyncio
import re
from yt_dlp import YoutubeDL
from youtubesearchpython.__future__ import VideosSearch
from BADMUSIC.platforms.Spotify import Spotify
from BADMUSIC.platforms.Apple import Apple

class YouTube:
    def __init__(self):
        self.cookies_path = "cookies/cookies.txt"
        self.ytdl_opts = {
            "format": "bestaudio/best",
            "quiet": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "cookiefile": self.cookies_path,
            "default_search": "ytsearch",
        }

    async def url(self, link: str):
        try:
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(
                None,
                lambda: YoutubeDL(self.ytdl_opts).extract_info(link, download=False),
            )

            # Fix for playlist or ytsearch results
            if "entries" in data:
                data = data["entries"][0]

            return {
                "title": data.get("title", "Unknown Title"),
                "duration": data.get("duration", 0),
                "duration_min": round(data.get("duration", 0) / 60, 2),
                "url": data.get("webpage_url"),
                "stream_url": data.get("url"),
                "thumbnail": self._resize_thumb(data.get("thumbnail")),
                "id": data.get("id", ""),
            }
        except Exception as e:
            return {"error": f"❌ Error: {str(e)}"}

    async def track(self, query: str):
        return await self.url(query)

    async def playlist(self, query: str):
        try:
            search = VideosSearch(query, limit=5)
            results = await search.next()
            links = [video["link"] for video in results["result"]]
            return [await self.url(link) for link in links]
        except Exception as e:
            return {"error": f"❌ Error: {str(e)}"}

    async def smart_track(self, link_or_query: str):
        if "spotify.com/track" in link_or_query:
            spotify = Spotify()
            details = await spotify.track(link_or_query)
            return await self.track(f"{details.get('title')} {details.get('artist')}")
        elif "music.apple.com" in link_or_query:
            apple = Apple()
            details = await apple.track(link_or_query)
            return await self.track(details.get("title"))
        elif "youtube.com" in link_or_query or "youtu.be" in link_or_query:
            return await self.url(link_or_query)
        else:
            return await self.track(link_or_query)

    def _resize_thumb(self, thumb_url):
        if not thumb_url:
            return None
        return re.sub(r"(\d+)x(\d+)", "480x360", thumb_url)