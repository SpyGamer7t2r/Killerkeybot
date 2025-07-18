import asyncio
import re
from youtubesearchpython.__future__ import VideosSearch
from yt_dlp import YoutubeDL

YTDL_OPTS = {
    "format": "bestaudio",
    "quiet": True,
    "geo_bypass": True,
    "nocheckcertificate": True,
    "cookiefile": "cookies/cookies.txt",
}

class YouTube:
    def __init__(self):
        self.ytdl = YoutubeDL(YTDL_OPTS)

    async def url(self, link: str):
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(link, download=False))
        return {
            "title": data.get("title"),
            "duration": data.get("duration"),
            "duration_min": round(data.get("duration", 0) / 60, 2),
            "url": data.get("webpage_url"),
            "stream_url": data["url"],
            "thumbnail": data.get("thumbnail"),
            "id": data.get("id"),
        }

    async def track(self, query: str):
        search = VideosSearch(query, limit=1)
        result = (await search.next())["result"]
        if not result:
            return None
        vid = result[0]
        return {
            "title": vid["title"],
            "duration": vid["duration"],
            "duration_min": self._duration_to_min(vid["duration"]),
            "url": vid["link"],
            "id": vid["id"],
            "thumbnail": vid["thumbnails"][0]["url"],
        }

    async def playlist(self, url: str):
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(url, download=False))
        tracks = []
        for entry in data.get("entries", []):
            tracks.append({
                "title": entry.get("title"),
                "duration": entry.get("duration"),
                "duration_min": round(entry.get("duration", 0) / 60, 2),
                "url": entry.get("webpage_url"),
                "id": entry.get("id"),
                "thumbnail": entry.get("thumbnail"),
            })
        return tracks

    def _duration_to_min(self, duration: str) -> float:
        if not duration:
            return 0.0
        parts = list(map(int, duration.split(":")))
        if len(parts) == 3:
            return parts[0] * 60 + parts[1] + parts[2] / 60
        elif len(parts) == 2:
            return parts[0] + parts[1] / 60
        return float(parts[0])
import yt_dlp
from youtubesearchpython.__future__ import VideosSearch


class YouTube:
    def __init__(self):
        self.cookies_path = "cookies/cookies.txt"

    async def url(self, link: str):
        try:
            ydl_opts = {
                "format": "bestaudio/best",
                "quiet": True,
                "noplaylist": True,
                "cookiefile": self.cookies_path,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link, download=False)
            return {
                "title": info.get("title"),
                "duration": info.get("duration"),
                "id": info.get("id"),
                "url": info.get("webpage_url"),
                "thumbnail": info.get("thumbnail"),
                "source": info.get("url"),
            }
        except Exception as e:
            return {"error": str(e)}

    async def track(self, query: str):
        try:
            # Use ytsearch to avoid invalid URL error
            search = VideosSearch(query, limit=1)
            result = (await search.next())["result"][0]
            return await self.url(result["link"])
        except Exception as e:
            return {"error": str(e)}

    async def playlist(self, query: str):
        try:
            search = VideosSearch(query, limit=5)
            results = await search.next()
            links = [video["link"] for video in results["result"]]
            return [await self.url(link) for link in links]
        except Exception as e:
            return {"error": str(e)}