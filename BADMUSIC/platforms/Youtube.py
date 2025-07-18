import asyncio
from youtubesearchpython.__future__ import VideosSearch
from yt_dlp import YoutubeDL


class YouTube:
    def __init__(self):
        self.cookies_path = "cookies/cookies.txt"
        self.ytdl_opts = {
            "format": "bestaudio/best",
            "quiet": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "cookiefile": self.cookies_path,
        }

    async def url(self, link: str):
        try:
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(
                None,
                lambda: YoutubeDL(self.ytdl_opts).extract_info(link, download=False),
            )
            return {
                "title": data.get("title"),
                "duration": data.get("duration"),
                "duration_min": round(data.get("duration", 0) / 60, 2),
                "url": data.get("webpage_url"),
                "stream_url": data["url"],
                "thumbnail": data.get("thumbnail"),
                "id": data.get("id"),
            }
        except Exception as e:
            return {"error": str(e)}

    async def track(self, query: str):
        try:
            search = VideosSearch(query, limit=1)
            results = await search.next()
            if not results["result"]:
                return {"error": "No results found"}
            vid = results["result"][0]
            return await self.url(vid["link"])
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