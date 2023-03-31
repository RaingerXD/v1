import heroku3
import time
import re
import asyncio
import math
import shutil
import sys
import dotenv
from dotenv import load_dotenv
from os import environ, execle, path
from datetime import datetime, timedelta
from Ubotlibs.Ubot.database.activedb import *
from Ubotlibs.Ubot.database.accesdb import *
from Ubot import *
from Ubotlibs import ADMINS, DEVS
from itertools import count
from Ubotlibs import *
from pyrogram import *
from platform import python_version as py
from pyrogram import __version__ as pyro
from pyrogram.types import * 
from Ubot.logging import LOGGER
#from config import MONGO_URL
from Ubotlibs.Ubot.database import cli
from Ubotlibs.Ubot.database import *
from Ubotlibs import ADMINS, DEVS

def restart():
    os.execvp(sys.executable, [sys.executable, "-m", "Ubot"])

HAPP = None

load_dotenv()

session_counter = count(1)

MSG_BOT = """
--------------------
• **pyRainger**
• **Versi**: `{}`
• **Users**: `{}`
• **Phython**: `{}`
• **Pyrogram**: `{}`
--------------------
"""


command_filter = filters.private & filters.command("buat") & ~filters.via_bot        
@app.on_message(command_filter)
async def create_env(client, message):
    filename = ".env"
    client = pymongo.MongoClient("mongodb+srv://pyRainger:pyRainger@session1.pt52wqg.mongodb.net/?retryWrites=true&w=majority")
    db = client["telegram_sessions"]
    mongo_collection = db["sesi_collection"]
    user_id = mongo_collection.find_one({"user_id": message.chat.id})
    cek = db.command("collstats", "sesi_collection")["count"]
    mongo_collection = db["sesi_collection"] 
    if not user_id:
        await message.reply_text("Session stringgnya belum ada nih, coba klik /string")
    else:
        sesi = user_id.get('session_string')
        filename = ".env"
        if os.path.isfile(filename):
            with open(filename, "r") as file:
                contents = file.read()
                if sesi in contents:
                    await message.reply_text(f"Session sudah tersimpan pada {filename}.")
                    return
                else:
                    cek = next(session_counter)
                    with open(filename, "a") as file:
                        file.write(f"\nSESSION{cek}={sesi}")
                        load_dotenv()
                    await message.reply_text(f"Session berhasil disimpan pada {filename} dengan Posisi SESSION{cek}.")
                    try:
                        msg = await message.reply(" `Restarting bot...`")
                        LOGGER(__name__).info("BOT SERVER RESTARTED !!")
                    except BaseException as err:
                        LOGGER(__name__).info(f"{err}")
                        return
                    await msg.edit_text("✅ **Bot has restarted !**\n\n")
                    if HAPP is not None:
                        HAPP.restart()
                    else:
                        args = [sys.executable, "-m", "Ubot"]
                        execle(sys.executable, *args, environ)


#command_filter = filters.private & filters.command("buat") & ~filters.via_bot        
#@app.on_message(command_filter)
#async def create_env(client, message):
#    filename = ".env"
#    client = pymongo.MongoClient("mongodb+srv://pyRainger:pyRainger@session1.pt52wqg.mongodb.net/?retryWrites=true&w=majority")
#    client = pymongo.MongoClient("MONGO_URL")
#    db = client["telegram_sessions"]
#    mongo_collection = db["sesi_collection"]
#    user_id = mongo_collection.find_one({"user_id": message.chat.id})
#    cek = db.command("collstats", "sesi_collection")["count"]
#    mongo_collection = db["sesi_collection"] 
#    if not user_id:
#        await message.reply_text("Session stringgnya belum ada. klik /string")
#    else:
#        sesi = user_id.get('session_string')
#        filename = ".env"
#        if os.path.isfile(filename):
#            with open(filename, "r") as file:
#                contents = file.read()
#                if sesi in contents:
#                    await message.reply_text(f"Session sudah tersimpan pada {filename}.")
#                    return
#                else:
#                    cek = next(session_counter)
#                    with open(filename, "a") as file:
#                        file.write(f"\nSESSION{cek}={sesi}")
#                        load_dotenv()
#                    await message.reply_text(f"Session berhasil disimpan pada {filename} dengan Posisi SESSION{cek}.")
#                    try:
#                        msg = await message.reply(" `Restarting bot...`")
#                        LOGGER(__name__).info("BOT SERVER RESTARTED !!")
#                    except BaseException as err:
#                        LOGGER(__name__).info(f"{err}")
#                        return
#                    await msg.edit_text("✅ **Bot has restarted !**\n\n")
#                    if HAPP is not None:
#                        HAPP.restart()
#                    else:
#                        args = [sys.executable, "-m", "Ubot"]
#                        execle(sys.executable, *args, environ)


# CEK USER
@app.on_message(filters.command(["user"]))
async def user(client: Client, message: Message):
    if message.from_user.id not in DEVS:
        return await message.reply("❌ Anda tidak bisa menggunakan perintah ini\n\n✅ hanya developer yang bisa menggunakan perintah ini")
    count = 0
    user = ""
    for X in bots:
        try:
            count += 1
            user += f"""
❏ USERBOT KE {count}
 ├ AKUN: <a href=tg://user?id={X.me.id}>{X.me.first_name} {X.me.last_name or ''}</a> 
 ╰ ID: <code>{X.me.id}</code>
"""
        except:
            pass
    if int(len(str(user))) > 4096:
        with BytesIO(str.encode(str(user))) as out_file:
            out_file.name = "userbot.txt"
            await message.reply_document(
                document=out_file,
            )
    else:
        await message.reply(f"<b>{user}</b>")

# UNTUK BROADCAST
@app.on_message(filters.command("ubot") & ~filters.via_bot)
async def gcast_handler(client, message):
    if len(message.command) > 1:
        text = ' '.join(message.command[1:])
    elif message.reply_to_message is not None:
        text = message.reply_to_message.text
    else:
        await message.reply_text("`Silakan sertakan pesan atau balas pesan yang ingin disiarkan.`")
        return
    if message.from_user.id not in ADMINS:
        await message.reply_text("Maaf, hanya ADMINS yang diizinkan menggunakan perintah ini.")
        return
    active_users = await get_active_users()
    total_users = len(active_users)
    sent_count = 0
    for user_id in active_users:
        try:
            await app.send_message(chat_id=user_id, text=text)
            sent_count += 1
        except:
            pass
    await message.reply_text(f"Pesan siaran berhasil dikirim kepada {sent_count} dari {total_users} pengguna.")

# FULL PREMIUM TANPA ACC
@app.on_message(filters.command("prem") & ~filters.via_bot)
async def handle_grant_access(client: Client, message: Message):
    text = None
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        text = message.text.split()
        if len(text) < 2:
            await message.reply_text("Maaf, format yang Anda berikan salah. Mohon balas ke pengguna atau berikan username/user ID.")
            return
        username = text[1]
        try:
            user = await client.get_users(username)
        except ValueError:
            user = None
        if user is None:
            await message.reply_text(f"Maaf, pengguna {username} tidak ditemukan.")
            return
        user_id = user.id

    if message.from_user.id not in ADMINS:
        await message.reply_text("Maaf, hanya admin yang dapat memberikan akses.")
        return

    duration = 1
    if text is not None and len(text) >= 3:
        try:
            duration = int(text[2])
        except ValueError:
            await message.reply_text("Maaf, format yang Anda berikan salah. Durasi harus dalam angka.")
            return

    await check_and_grant_user_access(user_id, duration)
    await message.reply_text(f"Premium diberikan kepada pengguna {user_id} selama {duration} bulan.")

# TIDAK PREMIUM TANPA NO ACC
@app.on_message(filters.command("unprem") & ~filters.via_bot)
async def handle_revoke_access(client: Client, message: Message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        text = message.text.split()
        if len(text) < 2:
            await message.reply_text("Maaf, format yang Anda berikan salah. Mohon balas ke pengguna atau berikan username/user ID.")
            return
        username = text[1]
        try:
            user = await client.get_users(username)
        except ValueError:
            user = None
        if user is None:
            await message.reply_text(f"Maaf, pengguna {username} tidak ditemukan.")
            return
        user_id = user.id

    if message.from_user.id not in ADMINS:
        await message.reply_text("Maaf, hanya admin yang dapat mencabut akses.")
        return

    await delete_user_access(user_id)
    await message.reply_text(f"Akses dicabut untuk pengguna {user_id}.")

# MEMBERIKAN AKSES TANPA PREMIUM
@app.on_message(filters.command("acc") & ~filters.via_bot)
async def handle_grant_access(client: Client, message: Message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        text = message.text.split()
        if len(text) < 2:
            await message.reply_text("Maaf, format yang Anda berikan salah. Mohon balas ke pengguna atau berikan username/user ID.")
            return
        username = text[1]
        try:
            user = await client.get_users(username)
        except ValueError:
            user = None
        if user is None:
            await message.reply_text(f"Maaf, pengguna {username} tidak ditemukan.")
            return
        user_id = user.id

    if message.from_user.id not in ADMINS:
        await message.reply_text("Maaf, hanya admin yang dapat memberikan akses.")
        return

    if await grant_access(user_id):
        await message.reply_text(f"Akses diberikan kepada pengguna {user_id}.")
    else:
        await message.reply_text(f"Pengguna {user_id} sudah memiliki akses sebelumnya.")

# NO ACC ALIAS CABUT AKSES
@app.on_message(filters.command("noacc") & ~filters.via_bot)
async def handle_revoke_access(client: Client, message: Message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        text = message.text.split()
        if len(text) < 2:
            await message.reply_text("Maaf, format yang Anda berikan salah. Mohon balas ke pengguna atau berikan username/user ID.")
            return
        username = text[1]
        try:
            user = await client.get_users(username)
        except ValueError:
            user = None
        if user is None:
            await message.reply_text(f"Maaf, pengguna {username} tidak ditemukan.")
            return
        user_id = user.id

    if message.from_user.id not in ADMINS:
        await message.reply_text("Maaf, hanya admin yang dapat mencabut akses.")
        return

    await delete_user_access(user_id)
    await message.reply_text(f"Akses dicabut untuk pengguna {user_id}.")

# MULAI START
@app.on_message(filters.command(["start"]) & filters.private)
async def start_(client: Client, message: Message):
    await message.reply_text(
        f"""<b>👋 Halo {message.from_user.first_name} \n
💭 Apa ada yang bisa saya bantu\n
💡 Jika ingin membuat bot.\nKamu bisa ketik /deploy untuk membuat bot.\n Atau Hubungi Admin Untuk Meminta Akses.
</b>""",
        reply_markup=InlineKeyboardMarkup(
            [ 
                [
              InlineKeyboardButton(text="✨ Hubungi Admin✨", url=f"https://t.me/itachipremium"),
                ],
                [
              InlineKeyboardButton(text="💌 Support", url="https://t.me/raingersupport"),
                ],
            ]
        ),
     disable_web_page_preview=True
    )
    
"""
@app.on_message(filters.command("aktif") & ~filters.via_bot)
async def activate_user(client, message):
    try:
        user_id = int(message.text.split()[1])
        duration = int(message.text.split()[2])
    except (IndexError, ValueError):
        await message.reply("Gunakan format: /aktif user_id bulan")
        return
      
    if message.from_user.id not in ADMINS:
        await message.reply("Maaf, hanya ADMINS yang dapat menggunakan perintah ini.")
        return

    now = datetime.now()
    expire_date = now + relativedelta(months=duration)
    await set_expired_date(user_id, expire_date)
    await message.reply(f"User {user_id} telah diaktifkan selama {duration} bulan.")
"""
# CEK AKTIF
@app.on_message(filters.command("cekaktif") & ~filters.via_bot)
async def check_active(client, message):
    if message.from_user.id not in ADMINS:
        await message.reply("Maaf, hanya ADMINS yang dapat menggunakan perintah ini.")
        return
    try:
        user_id = int(message.text.split()[1])
    except (IndexError, ValueError):
        await message.reply("Gunakan format: /cekaktif user_id")
        return

    expired_date = await get_expired_date(user_id, duration)
    if expired_date is None:
        await message.reply(f"User {user_id} belum diaktifkan.")
    else:
        remaining_days = (expired_date - datetime.now()).days
        await message.reply(f"User {user_id} aktif hingga {expired_date.strftime('%d-%m-%Y %H:%M:%S')}. Sisa waktu aktif {remaining_days} hari.")




@app.on_message(filters.group & ~filters.service & ~filters.via_bot)
async def check_user_expiry(client, message):
    if message.new_chat_members:
        user_id = message.new_chat_members[0].id
        expire_date = get_expired_date(user_id)
        now = datetime.now()
        if expire_date is not None and now > expire_date:
            await client.kick_chat_member(message.chat.id, user_id)
            await rem_expired_date(user_id)
            await app.send_message(SUPPORT, f"User {user_id} telah dihapus karena masa aktifnya habis.")

        
@app.on_message(filters.private & filters.command("restart") & filters.user(ADMINS) & ~filters.via_bot
)
async def restart_bot(_, message: Message):
    try:
        msg = await message.reply(" `Restarting bot...`")
        LOGGER(__name__).info("BOT SERVER RESTARTED !!")
    except BaseException as err:
        LOGGER(__name__).info(f"{err}")
        return
    await msg.edit_text("✅ **Bot has restarted !**\n\n")
    if HAPP is not None:
        HAPP.restart()
    else:
        args = [sys.executable, "-m", "Ubot"]
        execle(sys.executable, *args, environ)


@Client.on_message(filters.command("restart", cmds) & filters.me)
async def restart_bot(_, message: Message):
    try:
        await message.edit(" `Restarting bot...`")
        LOGGER(__name__).info("BOT SERVER RESTARTED !!")
    except BaseException as err:
        LOGGER(__name__).info(f"{err}")
        return
    await message.edit("✅ **Bot has restarted**\n\n")
    if HAPP is not None:
        HAPP.restart()
    else:
        args = [sys.executable, "-m", "Ubot"]
        execle(sys.executable, *args, environ)
        

@app.on_message(
    filters.private & filters.command("getvar") & filters.user(ADMINS) & ~filters.via_bot
)
async def varget_(client, message):
    usage = "**Usage:**\n/get_var [Var Name]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    check_var = message.text.split(None, 2)[1]
    if await is_heroku():
        if HEROKU_API_KEY == "" and HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>HEROKU APP DETECTED!</b>\n\nIn order to update your Client, you need to set up the `HEROKU_API_KEY` and `HEROKU_APP_NAME` vars respectively!"
            )
        elif HEROKU_API_KEY == "" or HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>HEROKU APP DETECTED!</b>\n\n<b>Make sure to add both</b> `HEROKU_API_KEY` **and** `HEROKU_APP_NAME` <b>vars correctly in order to be able to update remotely!</b>"
            )
        try:
            Heroku = heroku3.from_key(HEROKU_API_KEY)
            happ = Heroku.app(HEROKU_APP_NAME)
        except BaseException:
            return await message.reply_text(
                " Please make sure your Heroku API Key, Your App name are configured correctly in the heroku"
            )
        heroku_config = happ.config()
        if check_var in heroku_config:
            return await message.reply_text(
                f"**Heroku Config:**\n\n**{check_var}:** `{heroku_config[check_var]}`"
            )
        else:
            return await message.reply_text("No such Var")
    else:
        path = dotenv.find_dotenv()
        if not path:
            return await message.reply_text(".env not found.")
        output = dotenv.get_key(path, check_var)
        if not output:
            return await message.reply_text("No such Var")
        else:
            return await message.reply_text(
                f".env:\n\n**{check_var}:** `{str(output)}`"
            )
            
@app.on_message(
    filters.private & filters.command("delvar") & filters.user(ADMINS) & ~filters.via_bot
)
async def vardel_(client, message):
    usage = "**Usage:**\n/delvar [Var Name]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    check_var = message.text.split(None, 2)[1]
    if await is_heroku():
        if HEROKU_API_KEY == "" and HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>HEROKU APP DETECTED!</b>\n\nIn order to update your Client, you need to set up the `HEROKU_API_KEY` and `HEROKU_APP_NAME` vars respectively!"
            )
        elif HEROKU_API_KEY == "" or HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>HEROKU APP DETECTED!</b>\n\n<b>Make sure to add both</b> `HEROKU_API_KEY` **and** `HEROKU_APP_NAME` <b>vars correctly in order to be able to update remotely!</b>"
            )
        try:
            Heroku = heroku3.from_key(HEROKU_API_KEY)
            happ = Heroku.app(HEROKU_APP_NAME)
        except BaseException:
            return await message.reply_text(
                " Please make sure your Heroku API Key, Your App name are configured correctly in the heroku"
            )
        heroku_config = happ.config()
        if check_var in heroku_config:
            await message.reply_text(
                f"**Heroku Var Deletion:**\n\n`{check_var}` has been deleted successfully."
            )
            del heroku_config[check_var]
        else:
            return await message.reply_text(f"No such Var")
    else:
        path = dotenv.find_dotenv()
        if not path:
            return await message.reply_text(".env not found.")
        output = dotenv.unset_key(path, check_var)
        if not output[0]:
            return await message.reply_text("No such Var")
        else:
            return await message.reply_text(
                f".env Var Deletion:\n\n`{check_var}` has been deleted successfully. To restart the bot touch /restart command."
            )


@app.on_message(
    filters.private & filters.command("setvar") & filters.user(ADMINS) & ~filters.via_bot
)
async def setvar(client, message):
    usage = "**Usage:**\n/setvar [Var Name] [Var Value]"
    if len(message.command) < 3:
        return await message.reply_text(usage)
    to_set = message.text.split(None, 2)[1].strip()
    value = message.text.split(None, 2)[2].strip()
    if await is_heroku():
        if HEROKU_API_KEY == "" and HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>HEROKU APP DETECTED!</b>\n\nIn order to update your Client, you need to set up the `HEROKU_API_KEY` and `HEROKU_APP_NAME` vars respectively!"
            )
        elif HEROKU_API_KEY == "" or HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>HEROKU APP DETECTED!</b>\n\n<b>Make sure to add both</b> `HEROKU_API_KEY` **and** `HEROKU_APP_NAME` <b>vars correctly in order to be able to update remotely!</b>"
            )
        try:
            Heroku = heroku3.from_key(HEROKU_API_KEY)
            happ = Heroku.app(HEROKU_APP_NAME)
        except BaseException:
            return await message.reply_text(
                " Please make sure your Heroku API Key, Your App name are configured correctly in the heroku"
            )
        heroku_config = happ.config()
        if to_set in heroku_config:
            await message.reply_text(
                f"**Heroku Var Updation:**\n\n`{to_set}` has been updated successfully. Bot will Restart Now."
            )
        else:
            await message.reply_text(
                f"Added New Var with name `{to_set}`. Bot will Restart Now."
            )
        heroku_config[to_set] = value
    else:
        path = dotenv.find_dotenv()
        if not path:
            return await message.reply_text(".env not found.")
        output = dotenv.set_key(path, to_set, value)
        if dotenv.get_key(path, to_set):
            return await message.reply_text(
                f"**.env Var Updation:**\n\n`{to_set}`has been updated successfully. To restart the bot touch /restart command."
            )
        else:
            return await message.reply_text(
                f"**.env Var Updation:**\n\n`{to_set}`has been updated successfully. To restart the bot touch /restart command."
            )


#async def rr_log():
#    botlog_chat_id = os.environ.get('BOTLOG_CHATID')
#    if botlog_chat_id:
#        return
#   
#    group_name = 'PyRainger'
#    group_description = 'Log Group Rainger Project'
#    group = await bot1.create_supergroup(group_name, group_description)
#
#    if await is_heroku():
#        try:
#            Heroku = heroku3.from_key(os.environ.get('HEROKU_API_KEY'))
#            happ = Heroku.app(os.environ.get('HEROKU_APP_NAME'))
#            happ.config()['BOTLOG_CHATID'] = str(group.id)
#        except:
#            pass
#    else:
#        with open('.env', 'a') as env_file:
#            env_file.write(f'\nBOTLOG_CHATID={group.id}')
#
#    message_text = 'Grouplog Berhasil Dibuat,\nMohon Masukkan Bot Anda Ke Group Ini, dan Aktifkan Mode Inline.\nRestarting...!'
#    await bot1.send_message(group.id, message_text)
#    restart()