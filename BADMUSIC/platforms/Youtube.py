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

            # Handle playlists or multiple entries
            if "entries" in data:
                data = data["entries"][0]

            # Safely extract fields with defaults
            title = data.get("title") or "Unknown Title"
            duration = data.get("duration") or 0
            stream_url = data.get("url")
            webpage_url = data.get("webpage_url")
            thumbnail = self._resize_thumb(data.get("thumbnail"))
            video_id = data.get("id") or ""

            if not stream_url or not title:
                return {"error": "❌ Failed to extract valid video info."}

            return {
                "title": title,
                "duration": duration,
                "duration_min": round(duration / 60, 2),
                "url": webpage_url,
                "stream_url": stream_url,
                "thumbnail": thumbnail,
                "id": video_id,
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
        try:
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
        except Exception as e:
            return {"error": f"❌ Error: {str(e)}"}

    def _resize_thumb(self, thumb_url):
        if not thumb_url:
            return None
        return re.sub(r"(\d+)x(\d+)", "480x360", thumb_url)