import heroku3
import time
import re
import asyncio
import math
import shutil
import sys
import dotenv
import datetime
import asyncio
import math
import os
import dotenv
import heroku3
import requests
import urllib3
from dotenv import load_dotenv
from os import environ, execle, path
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from bot import *
from itertools import count
from bot.modules.basic import *
from bot.modules.sudo import ADMINS, SUDO

from pyrogram import *
from platform import python_version as py
from pyrogram import __version__ as pyro
from pyrogram.types import * 
from io import BytesIO
#from ubotlibs.ubot.utils.misc import *
from bot.logging import LOGGER
from config import *

def restart():
    os.execvp(sys.executable, [sys.executable, "-m", "bot"])

HAPP = None

load_dotenv()

session_counter = count(1)

ANU = """
❏ **Users** Ke {}
├╼ **Nama**: {}
╰╼ **ID**: {}
"""

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


XCB = [
    "/",
    "@",
    ".",
    "com",
    ":",
    "git",
    "heroku",
    "push",
    str(HEROKU_API_KEY),
    "https",
    str(HEROKU_APP_NAME),
    "HEAD",
    "main",
]


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


@app.on_message(filters.command(["start"]) & filters.private)
async def start_(client: Client, message: Message):
    await message.reply_text(
        f"""<b>👋 Halo {message.from_user.first_name} \n
💭 Apa ada yang bisa saya bantu
💡 Jika ingin membuat bot Kamu bisa \nketik /deploy untuk membuat bot.\n Atau Hubungi Admin Untuk Meminta Akses.
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


@app.on_message(filters.command(["start"]))
async def start_(client: Client, message: Message):
    ADMIN1 = ADMIN1_ID[0]
    await message.reply_text(
        f"""<b>👋 Halo {message.from_user.first_name} \n
💭 Apa ada yang bisa saya bantu
💡 Jika ingin membuat bot premium . Kamu bisa hubungin admin dibawah ini membuat bot.</b>""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="👮‍♂ Admin 1", url=f"https://t.me/itachipremium"),
                ],
                  [
                     InlineKeyboardButton(text="Tutup", callback_data="cl_ad"),
                  ],
             ]
        ),
     disable_web_page_preview=True
    )
    
        
@app.on_message(filters.private & filters.command("restart") & ~filters.via_bot
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
        args = [sys.executable, "-m", "pyRainger"]
        execle(sys.executable, *args, environ)


@Client.on_message(filters.command("restart", "") & filters.me)
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
        args = [sys.executable, "-m", "pyRainger"]
        execle(sys.executable, *args, environ)
        
        
@Ubot("usage", "")
async def usage_dynos(client, message):
    if await is_heroku():
        if HEROKU_API_KEY == "" and HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>Menggunakan App Heroku!</b>\n\nMasukan/atur  `HEROKU_API_KEY` dan `HEROKU_APP_NAME` untuk bisa melakukan update!"
            )
        elif HEROKU_API_KEY == "" or HEROKU_APP_NAME == "":
            return await message.reply_text(
                "<b>Menggunakan App Heroku!</b>\n\n<b>pastikan</b> `HEROKU_API_KEY` **dan** `HEROKU_APP_NAME` <b>sudah di configurasi dengan benar!</b>"
            )
    else:
            return await message.reply_text("Hanya untuk Heroku Deployment")
    try:
        Heroku = heroku3.from_key(HEROKU_API_KEY)
        happ = Heroku.app(HEROKU_APP_NAME)
    except BaseException:
        return await message.reply_text(
            " Pastikan Heroku API Key, App name sudah benar"
        )
    dyno = await message.reply_text("Memeriksa penggunaan dyno...")
    account_id = Heroku.account().id
    useragent = (
        "Mozilla/5.0 (Linux; Android 10; SM-G975F) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/80.0.3987.149 Mobile Safari/537.36"
    )
    headers = {
        "User-Agent": useragent,
        "Authorization": f"Bearer {HEROKU_API_KEY}",
        "Accept": "application/vnd.heroku+json; version=3.account-quotas",
    }
    path = "/accounts/" + account_id + "/actions/get-quota"
    r = requests.get("https://api.heroku.com" + path, headers=headers)
    if r.status_code != 200:
        return await dyno.edit("Unable to fetch.")
    result = r.json()
    quota = result["account_quota"]
    quota_used = result["quota_used"]
    remaining_quota = quota - quota_used
    percentage = math.floor(remaining_quota / quota * 100)
    minutes_remaining = remaining_quota / 60
    hours = math.floor(minutes_remaining / 60)
    minutes = math.floor(minutes_remaining % 60)
    App = result["apps"]
    try:
        App[0]["quota_used"]
    except IndexError:
        AppQuotaUsed = 0
        AppPercentage = 0
    else:
        AppQuotaUsed = App[0]["quota_used"] / 60
        AppPercentage = math.floor(App[0]["quota_used"] * 100 / quota)
    AppHours = math.floor(AppQuotaUsed / 60)
    AppMinutes = math.floor(AppQuotaUsed % 60)
    await asyncio.sleep(1.5)
    text = f"""
**Penggunaan Dyno pyRainger**

 ❏ Dyno terpakai:
 ├ Terpakai: `{AppHours}`**h**  `{AppMinutes}`**m**  [`{AppPercentage}`**%**]
Dyno tersisa:
  ╰ Tersisa: `{hours}`**h**  `{minutes}`**m**  [`{percentage}`**%**]"""
    return await dyno.edit(text)
    
    
async def kok_bacotlog():
    botlog_chat_id = os.environ.get('BOTLOG_CHATID')
    if botlog_chat_id:
        return
   
    group_name = 'pyRainger Log'
    group_description = 'Log Group pyRainger'
    group = await bot1.create_supergroup(group_name, group_description)

    if await is_heroku():
        try:
            Heroku = heroku3.from_key(os.environ.get('HEROKU_API_KEY'))
            happ = Heroku.app(os.environ.get('HEROKU_APP_NAME'))
            happ.config()['BOTLOG_CHATID'] = str(group.id)
        except:
            pass
    else:
        with open('.env', 'a') as env_file:
            env_file.write(f'\nBOTLOG_CHATID={group.id}')

    message_text = 'Grouplog Berhasil Dibuat,\nMohon Masukkan Bot Anda Ke Group Ini, dan Aktifkan Mode Inline.\nRestarting...!'
    await bot1.send_message(group.id, message_text)
    restart()