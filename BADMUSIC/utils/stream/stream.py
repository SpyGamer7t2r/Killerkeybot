import os
import asyncio

from BADMUSIC import app
from BADMUSIC.core.call import BAD
from BADMUSIC.utils.database import is_video_allowed
from config import DURATION_LIMIT

from BADMUSIC.platforms import PlaTForms  # ✅ Corrected import
platform = PlaTForms()


async def stream(
    client,
    m,
    streamtype,
    playertype,
    videoid,
    user_id,
    query,
    chat_id,
    duration,
    link,
    streamcall,
    spotify=None,
):
    try:
        if streamtype == "telegram":
            details, videoid = await platform.telegram.track(m)
        elif streamtype == "soundcloud":
            details, videoid = await platform.soundcloud.track(link)
        elif streamtype == "youtube":
            details, videoid = await platform.youtube.track(link)
        elif streamtype == "spotify":
            details, videoid = await platform.spotify.track(link)
        elif streamtype == "apple":
            details, videoid = await platform.apple.track(link)
        elif streamtype == "saavn":
            details, videoid = await platform.saavn.track(link)
        elif streamtype == "resso":
            details, videoid = await platform.resso.track(link)
        elif streamtype == "carbon":
            details, videoid = await platform.carbon.track(link)
        else:
            await m.reply_text("❌ Invalid stream source!")
            return

        # ✅ Prevent KeyError if 'thumb' is missing
        thumbnail = details.get("thumb") or "https://te.legra.ph/file/36c2ff5d9c8fba9c221bc.jpg"

        title = details.get("title", "Unknown Title")
        link = details.get("link", "")
        duration_min = details.get("duration_min", "0:00")

        # Here you would call the streaming function
        await BAD.play_stream(chat_id, videoid, streamcall)

        # Optional: Send success message
        await m.reply_photo(
            photo=thumbnail,
            caption=f"🎶 Now Playing: {title}\n⏱ Duration: {duration_min}",
        )
    except Exception as e:
        await m.reply_text(f"🚫 Failed to stream.\n\n**Error:** `{str(e)}`")