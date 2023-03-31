
from pyrogram import Client, enums, filters
from pyrogram.types import *
from Ubot import *
from Ubot.modules.basic import add_command_help
from Ubotlibs.Ubot.database import *
from Ubotlibs.Ubot.database.accesdb import *


from pyrogram.filters import chat
from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio
from typing import Dict, List, Union
from datetime import datetime, timedelta


collection = cli["pyRainger"]["tag_log"]


tagged_messages_filter = filters.group & filters.private & filters.mentioned & filters.incoming


async def anuan_log(user_id: int) -> bool:
    log = {"user_id": user_id}
    try:
        result = await collection.users.update_one(
            {'user_id': user_id},
            {'$set': {'tag_log': True}},
            upsert=True
        )
        if result.modified_count > 0 or result.upserted_id:
            await message.edit("**Tag alert Activated Successfully**")
            await log_tagged_messages()
            return True
    except:
        return False


async def gituan_log(user_id: int) -> bool:
    log = {"user_id": user_id}
    try:
        result = await collection.users.update_one(
            {'user_id': user_id},
            {'$set': {'tag_log': False}},
            upsert=True
        )
        if result.modified_count > 0 or result.upserted_id:
            await message.edit("**Tag alert Deactivated Successfully**")
            return False
    except:
        return False


async def log_tagged_messages():
    async for message in client.iter_messages(chat_id=CHAT_ID, filter=tagged_messages_filter):
        user_id = message.from_user.id
        tai = f"<b>📨 #TAGS #MESSAGE</b>\n<b> • : </b>{message.from_user.mention}"
        tai += f"\n<b> • Group : </b>{message.chat.title}"
        tai += f"\n<b> • 👀 </b><a href='{message.link}'>Lihat Pesan</a>"
        tai += f"\n<b> • Message : </b><code>{message.text}</code>"
        await asyncio.sleep(0.1)
        await client.send_message(
            BOTLOG_CHATID,
            tai,
            parse_mode="html",
            disable_web_page_preview=True,
        )


@Client.on_message(filters.command("log", cmds) & filters.me)
async def set_no_log_p_m_on(client: Client, message: Message):
    user_id = message.from_user.id
    await anuan_log(user_id)


@Client.on_message(filters.command("nolog", cmds) & filters.me)
async def set_no_log_p_m_off(client: Client, message: Message):
    user_id = message.from_user.id
    await gituan_log(user_id)

        
