import asyncio
from youtubesearchpython.__future__ import VideosSearch
from yt_dlp import YoutubeDL

async def yt_search(query: str):
    try:
        search = VideosSearch(query, limit=1)
        results = (await search.next())["result"]
        if not results:
            return None

        result = results[0]
        return {
            "title": result["title"],
            "duration_min": result.get("duration", "Unknown"),
            "link": result["link"],
            "vidid": result["id"],
            "thumb": result["thumbnails"][0]["url"].split("?")[0],
        }
    except Exception as e:
        return None

async def download_youtube_audio(url: str, cookies: str = "cookies/cookies.txt"):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "downloads/%(id)s.%(ext)s",
        "noplaylist": True,
        "quiet": True,
        "cookies": cookies if os.path.exists(cookies) else None,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(None, lambda: YoutubeDL(ydl_opts).extract_info(url, download=True))
    return {
        "title": data.get("title"),
        "filepath": f"downloads/{data['id']}.mp3",
        "duration": data.get("duration"),
        "thumb": data.get("thumbnail"),
    }