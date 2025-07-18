from BADMUSIC.platforms.Youtube import YouTube
from BADMUSIC.utils.stream.stream import stream

youtube = YouTube()

async def yt_stream(client, message, query):
    try:
        result = await youtube.track(query)
        if not result or "title" not in result:
            return await message.reply_text("❌ YouTube track not found or invalid format.")

        return await stream(
            client,
            message,
            title=result["title"],
            videoid=result["id"],
            user_id=message.from_user.id,
            duration=result.get("duration") or result.get("duration_min"),
            streamtype="youtube",
            playmode="Audio",
            query=query,
        )
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")