import asyncio
import os

from pyrogram.types import InlineKeyboardMarkup
from config import DURATION_LIMIT, LOGGER_ID
from BADMUSIC import app, Platform, db, SUDOERS, BAD
from BADMUSIC.utils.database import is_active_chat, put_queue
from BADMUSIC.utils.exceptions import AssistantErr
from BADMUSIC.utils.inline.play import stream_markup, close_markup
from BADMUSIC.utils.thumbnails import gen_thumb, gen_qthumb

async def stream(
    _,
    mystic,
    message,
    chat_id,
    original_chat_id,
    user_id,
    user_name,
    result,
    streamtype,
    video=False,
    forceplay=False,
):
    if streamtype == "telegram":
        title = result.get("title", "Telegram File")
        duration_min = result.get("duration_min", "00:00")
        file_path = result.get("file")
        thumb = result.get("thumb", "https://te.legra.ph/file/6e5291ab3c5f5d5c04241.jpg")

        if await is_active_chat(chat_id):
            await put_queue(
                chat_id,
                original_chat_id,
                file_path,
                title,
                duration_min,
                user_name,
                "telegram",
                user_id,
                "video" if video else "audio",
            )
            position = len(db.get(chat_id)) - 1
            qimg = thumb
            run = await app.send_photo(
                original_chat_id,
                photo=qimg,
                caption=_["queue_4"].format(
                    position, title[:27], duration_min, user_name
                ),
                reply_markup=close_markup(_),
            )
        else:
            if not forceplay:
                db[chat_id] = []
            await BAD.join_call(
                chat_id, original_chat_id, file_path, video=video, image=thumb
            )
            await put_queue(
                chat_id,
                original_chat_id,
                file_path,
                title,
                duration_min,
                user_name,
                "telegram",
                user_id,
                "video" if video else "audio",
                forceplay=forceplay,
            )
            button = stream_markup(_, "telegram", chat_id)
            run = await app.send_photo(
                original_chat_id,
                photo=thumb,
                caption=_["stream_1"].format(
                    title[:27],
                    "Telegram File",
                    duration_min,
                    user_name,
                ),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "stream"

    elif streamtype == "youtube":
        link = result.get("link")
        vidid = result.get("vidid")
        title = (result.get("title", "Unknown Title")).title()
        duration_min = result.get("duration_min", "Unknown")
        thumbnail = result.get("thumb", "https://te.legra.ph/file/6e5291ab3c5f5d5c04241.jpg")
        status = True if video else None

        try:
            file_path, direct = await Platform.youtube.download(
                vidid, mystic, videoid=True, video=status
            )
        except Exception:
            raise AssistantErr(_["play_16"])

        if await is_active_chat(chat_id):
            await put_queue(
                chat_id,
                original_chat_id,
                file_path if direct else f"vid_{vidid}",
                title,
                duration_min,
                user_name,
                vidid,
                user_id,
                "video" if video else "audio",
            )
            position = len(db.get(chat_id)) - 1
            qimg = await gen_qthumb(vidid)
            run = await app.send_photo(
                original_chat_id,
                photo=qimg,
                caption=_["queue_4"].format(
                    position, title[:27], duration_min, user_name
                ),
                reply_markup=close_markup(_),
            )
        else:
            if not forceplay:
                db[chat_id] = []
            await BAD.join_call(
                chat_id, original_chat_id, file_path, video=status, image=thumbnail
            )
            await put_queue(
                chat_id,
                original_chat_id,
                file_path if direct else f"vid_{vidid}",
                title,
                duration_min,
                user_name,
                vidid,
                user_id,
                "video" if video else "audio",
                forceplay=forceplay,
            )
            img = await gen_thumb(vidid)
            button = stream_markup(_, vidid, chat_id)
            run = await app.send_photo(
                original_chat_id,
                photo=img,
                caption=_["stream_1"].format(
                    title[:27],
                    f"https://t.me/{app.username}?start=info_{vidid}",
                    duration_min,
                    user_name,
                ),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "stream"

    elif streamtype == "live":
        link = result.get("link")
        vidid = result.get("vidid")
        title = (result.get("title", "Live Stream")).title()
        thumbnail = result.get("thumb", "https://te.legra.ph/file/6e5291ab3c5f5d5c04241.jpg")
        duration_min = "00:00"
        status = True if video else None

        if await is_active_chat(chat_id):
            await put_queue(
                chat_id,
                original_chat_id,
                link,
                title,
                duration_min,
                user_name,
                vidid,
                user_id,
                "video" if video else "audio",
            )
            position = len(db.get(chat_id)) - 1
            run = await app.send_photo(
                original_chat_id,
                photo=thumbnail,
                caption=_["queue_4"].format(
                    position, title[:27], duration_min, user_name
                ),
                reply_markup=close_markup(_),
            )
        else:
            if not forceplay:
                db[chat_id] = []
            await BAD.join_call(
                chat_id, original_chat_id, link, video=status, image=thumbnail
            )
            await put_queue(
                chat_id,
                original_chat_id,
                link,
                title,
                duration_min,
                user_name,
                vidid,
                user_id,
                "video" if video else "audio",
                forceplay=forceplay,
            )
            button = stream_markup(_, vidid, chat_id)
            run = await app.send_photo(
                original_chat_id,
                photo=thumbnail,
                caption=_["stream_1"].format(
                    title[:27],
                    link,
                    duration_min,
                    user_name,
                ),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "stream"