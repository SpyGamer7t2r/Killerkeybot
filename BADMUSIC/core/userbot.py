# Copyright (C) 2024 by Badhacker98@Github, < https://github.com/Badhacker98 >
# Owner: https://t.me/

from typing import Callable, Optional

import pyrogram
from pyrogram import Client, filters, handlers

import config
from ..logging import LOGGER

assistants = []
assistantids = []
clients = []


class Userbot:
    def __init__(self):
        self.one = self.create_client("BADString1", config.STRING1, "BADMUSIC.plugins.user")
        self.two = self.create_client("BADString2", config.STRING2)
        self.three = self.create_client("BADString3", config.STRING3)
        self.four = self.create_client("BADString4", config.STRING4)
        self.five = self.create_client("BADString5", config.STRING5)

    def create_client(self, name, session, plugin_root=None):
        if not session:
            return None
        return Client(
            name=name,
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=session,
            no_updates=False,
            plugins=dict(root=plugin_root) if plugin_root else None,
        )

    async def start(self):
        LOGGER(__name__).info("Starting Assistant Clients...")

        for idx, client in enumerate(
            [self.one, self.two, self.three, self.four, self.five], start=1
        ):
            if not client:
                continue

            try:
                await client.start()

                # Try joining required chats
                for chat in [
                    "PBX_CHAT",
                    "HEROKUBIN_01",
                    "ll_BAD_MUNDA_WORLD_ll",
                    "ll_BAD_ABOUT_ll",
                ]:
                    try:
                        await client.join_chat(chat)
                    except Exception:
                        pass  # Ignore join errors

                assistants.append(idx)
                clients.append(client)

                try:
                    await client.send_message(config.LOG_GROUP_ID, f"💫 Assistant {idx} Started ❤️")
                except Exception as e:
                    LOGGER(__name__).warning(
                        f"Assistant {idx} failed to access the log group: {e}"
                    )

                user = await client.get_me()
                client.username = user.username
                client.id = user.id
                client.mention = user.mention
                client.name = f"{user.first_name} {user.last_name or ''}".strip()

                assistantids.append(user.id)
                LOGGER(__name__).info(f"Assistant {idx} Started as {client.name}")

            except Exception as e:
                LOGGER(__name__).error(f"Failed to start Assistant {idx}: {e}")


def on_cmd(filters: Optional[pyrogram.filters.Filter] = None, group: int = 0) -> Callable:
    def decorator(func: Callable) -> Callable:
        for client in clients:
            try:
                client.add_handler(handlers.MessageHandler(func, filters), group)
            except Exception as e:
                LOGGER(__name__).warning(f"Error binding handler: {e}")
        return func
    return decorator