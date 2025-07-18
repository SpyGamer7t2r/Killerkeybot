from BADMUSIC.platforms.Youtube import YouTube
from BADMUSIC.utils.stream.stream import stream

youtube = YouTube()

async def yt_stream(client, message, query):
    try:
        result = await youtube.url(query)
        if not result:
            return await message.reply_text("No results found.")

        return await stream(
            client,
            message,
            title=result["title"],
            videoid=result["videoid"],
            user_id=message.from_user.id,
            duration=result["duration_min"],
            streamtype="youtube",
            playmode="Audio",
            query=query,
        )
    except Exception as e:
        await message.reply_text(f"❌ Error: {e}")