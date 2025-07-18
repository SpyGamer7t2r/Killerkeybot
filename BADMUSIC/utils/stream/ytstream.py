from BADMUSIC.platforms.Youtube import YouTube
from BADMUSIC.utils.stream.stream import stream

youtube = YouTube()

async def yt_stream(client, message, query):
    try:
        result = await youtube.track(query)

        if not result or "title" not in result or "stream_url" not in result:
            await message.reply_text(f"❌ Debug Info:\n{result}")
            return

        # Optional: Short debug info
        await message.reply_text(
            f"✅ Title: {result.get('title')}\n"
            f"🕒 Duration: {result.get('duration')} sec\n"
            f"🔗 Stream URL: {bool(result.get('stream_url'))}"
        )

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
        await message.reply_text(f"❌ Error: {str(e)[:400]}")