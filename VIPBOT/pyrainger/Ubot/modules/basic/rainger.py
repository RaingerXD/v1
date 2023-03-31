# Credits Thx Tomi Setiawan

import time
from datetime import datetime
import asyncio
import os
from gc import get_objects
import dotenv
from dotenv import load_dotenv
from os import environ, execle, path
from itertools import count

from pyrogram import Client, enums, filters
from pyrogram.types import *
from Ubot import CMD_HELP, StartTime, app, ids
from Ubot import cmds
from Ubotlibs.Ubot.database.activedb import *
from Ubotlibs.Ubot.database.usersdb import *
from Ubotlibs.Ubot.database.accesdb import *
from pyrogram.raw.functions import Ping
from Ubot.modules.bot.inline import get_readable_time
from Ubotlibs.Ubot.database.accesdb import *
from Ubot.modules.bot.start import ADMINS
from Ubotlibs.Ubot import Ubot, Devs

OWNER_ID = 5615921474
SUDO_ID = [5615921474, 1620434318]

load_dotenv()

session_counter = count(1)


def support():
    buttons = [
        [
            InlineKeyboardButton(text="sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/raingersupport"),
            InlineKeyboardButton(text="ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/raingerproject"),
        ],
    ]
    return buttons
    
@Client.on_message(filters.command("login", cmds) & filters.user(ADMINS) & filters.me)
@check_access
async def create_env(client, message):
    try:
        session = message.text.split()[1]
    except IndexError:
        await message.reply_text("Format yang benar adalah: login <session>")
        return

    filename = ".env"
    if os.path.isfile(filename):
        with open(filename, "r") as file:
            contents = file.read()
            if session in contents:
                await message.reply_text(f"Session sudah tersimpan pada {filename}.")
                return
            else:
                session_index = next(session_counter)
                with open(filename, "a") as file:
                    file.write(f"\nSESSION{session_index}={session}")
                    load_dotenv()
                await message.reply_text(f"Session berhasil disimpan pada {filename} dengan Posisi SESSION{session_index}.")
    else:
        session_index = next(session_counter)
        with open(filename, "w") as file:
            file.write(f"SESSION{session_index}={session}")
            load_dotenv()
        await message.reply_text(f"Session berhasil disimpan pada {filename} dengan Posisi SESSION{session_index}.")

    
    
    

@Client.on_message(filters.command("acc", cmds) & filters.me)
@check_access
async def handle_grant_access(client: Client, message: Message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        text = message.text.split()
        if len(text) < 2:
            await message.edit("Maaf, format yang Anda berikan salah. Mohon balas ke pengguna atau berikan username/user ID.")
            return
        username = text[1]
        user = await client.get_users(username)
        if user is None:
            await message.edit(f"`Maaf, pengguna {username} tidak ditemukan`.")
            return
        user_id = user.id

    if message.from_user.id not in ADMINS:
        await message.edit("`Maaf, hanya admin yang dapat memberikan akses.`")
        return

    if await grant_access(user_id):
        await message.edit(f"`Akses diberikan kepada pengguna {user_id}.`")
    else:
        await message.edit(f"`Pengguna {user_id} sudah memiliki akses sebelumnya.`")


@Client.on_message(filters.command("noacc", cmds) & filters.me)
@check_access
async def handle_revoke_access(client: Client, message: Message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        text = message.text.split()
        if len(text) < 2:
            await message.edit("Maaf, format yang Anda berikan salah. Mohon balas ke pengguna atau berikan username/user ID.")
            return
        username = text[1]
        user = await client.get_users(username)
        if user is None:
            await message.edit(f"`Maaf, pengguna {username} tidak ditemukan.`")
            return
        user_id = user.id
    if message.from_user.id not in ADMINS:
        await message.edit("`Maaf, hanya admin yang dapat mencabut akses.`")
        return
    await delete_user_access(user_id)
    await message.edit(f"`Akses dicabut untuk pengguna {user_id}.`")