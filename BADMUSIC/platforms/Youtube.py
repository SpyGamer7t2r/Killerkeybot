import re
from youtubesearchpython.__future__ import VideosSearch
from yt_dlp import YoutubeDL

class YouTube:
    async def url(self, message):
        try:
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
            duration = result["duration"]  # e.g., "3:45"
            views = result["viewCount"]["short"]
            thumbnail = result["thumbnails"][0]["url"]
            channel = result["channel"]["name"]
            link = result["link"]
            video_id = result["id"]

            # Convert duration to minutes and seconds
            if ":" in duration:
                parts = duration.split(":")
                if len(parts) == 2:
                    minutes, seconds = map(int, parts)
                elif len(parts) == 3:
                    hours, minutes, seconds = map(int, parts)
                    minutes += hours * 60
                else:
                    minutes, seconds = 0, 0
            else:
                minutes, seconds = 0, 0

            details = {
                "title": title,
                "duration": duration,
                "duration_min": minutes,
                "duration_sec": seconds,
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
                "cookiefile": "cookies.txt",  # ✅ Cookies support
            }
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
            return info.get("entries", [])
        except Exception as e:
            print(f"[YouTube.playlist] Error: {e}")
            return []