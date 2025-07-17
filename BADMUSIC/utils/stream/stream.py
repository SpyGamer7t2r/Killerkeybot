import asyncio
import os
import time
from typing import Union

from pyrogram.types import Message

from config import DURATION_LIMIT
from BADMUSIC import app
from BADMUSIC.core.call import BAD
from BADMUSIC.core.platform import Platform  # Update if Platform defined elsewhere
from BADMUSIC.misc import db
from BADMUSIC.misc.sudoers import SUDOERS
from BADMUSIC.utils.database import is_active_chat, add_active_video_chat
from BADMUSIC.utils.exceptions import AssistantErr
from BADMUSIC.utils.inline.play import stream_markup
from BADMUSIC.utils.stream.downloader import get_youtube_stream

# Example stream function
async def stream(
    client,
    message: Message,
    chat_id: int,
    user_id: int,
    result: dict,
    video: bool,
    streamtype: str
) -> None:
    try:
        title = result["title"]
        duration = result["duration"]
        url = result["url"]
        source = result["source"]
        video_id = result["id"]
        thumbnail = result.get("thumb") or result.get("thumbnail") or "https://telegra.ph/file/3dfd7e1a3eac3085dcd16.jpg"

        if not url:
            raise ValueError("No streamable URL found")

        await BAD.join_call(
            chat_id,
            url,
            video=video,
            stream_type=streamtype,
            title=title,
            thumb=thumbnail,
        )

        await add_active_video_chat(chat_id)

        await message.reply_photo(
            photo=thumbnail,
            caption=f"🎧 **Started Streaming:** `{title}`\n📫 **Requested by:** {message.from_user.mention}",
            reply_markup=stream_markup(video_id, user_id),
        )

    except Exception as e:
        await message.reply(f"⚠️ Error while streaming: `{e}`")