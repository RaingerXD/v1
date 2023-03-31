import importlib
import time
from datetime import datetime
import asyncio
from asyncio import get_event_loop_policy
from pyrogram import idle
from uvloop import install
from Ubotlibs import *
from Ubot import BOTLOG_CHATID, aiosession, bots, app, ids, LOOP
from platform import python_version as py
from Ubot.logging import LOGGER
from pyrogram import __version__ as pyro
from Ubot.modules import ALL_MODULES
from Ubotlibs import *
from Ubotlibs.Ubot.database.activedb import *
from Ubotlibs.Ubot.database.usersdb import *
from config import SUPPORT, CHANNEL
from Ubotlibs import ADMIN1_ID, ADMINS, BOT_VER
from Ubot import CMD_HNDLR
import os
from dotenv import load_dotenv


MSG_BOT = """
╼┅━━━━━━━━━━╍━━━━━━━━━━┅╾
• **pyRainger**
• **Phython**: `{}`
• **Pyrogram**: `{}`
• **Users**: `{}`
╼┅━━━━━━━━━━╍━━━━━━━━━━┅╾
"""

MSG_ON = """
**pyRainger Actived ✅**
╼┅━━━━━━━━━━╍━━━━━━━━━━┅╾
• **Versi** : `{}`
• **Phython** : `{}`
• **Pyrogram** : `{}`
• **Masa Aktif** : `{}`
• **Akan Berakhir**: `{}`
**Ketik** `{}ping` **untuk Mengecheck Bot**
╼┅━━━━━━━━━━╍━━━━━━━━━━┅╾
"""

MSG = """
**Users**: `{}`
**ID**: `{}`
"""


async def main():
    load_dotenv()
    await app.start()
    LOGGER("Ubot").info("Memulai pyRainger..")
    LOGGER("Ubot").info("Proses..")
    for all_module in ALL_MODULES:
        importlib.import_module("Ubot.modules" + all_module)
    for bot in bots:
        try:
            await bot.start()
            ex = await bot.get_me()
            await join(bot)
            LOGGER("Ubot").info("⚡⚡⚡")
            LOGGER("√").info(f"Started as {ex.first_name} | {ex.id} ")
            await add_user(ex.id)
            user_active_time = await get_active_time(ex.id)
            active_time_str = str(user_active_time.days) + " Hari " + str(user_active_time.seconds // 3600) + " Jam"
            expired_date = await get_expired_date(ex.id)
            remaining_days = (expired_date - datetime.now()).days
            msg = f"{ex.first_name} ({ex.id}) - Masa Aktif: {active_time_str}"
            ids.append(ex.id)
            await bot.send_message(BOTLOG_CHATID, MSG_ON.format(BOT_VER, pyro, py(), active_time_str, remaining_days, CMD_HNDLR))
            user = len( await get_active_users())
        except Exception as e:
            LOGGER("X").info(f"{e}")
            if "TELEGRAM" in str(e):
                for i in range(1, 201):
                    if os.getenv(f"SESSION{i}") == str(e):
                        os.environ.pop(f"SESSION{i}")
                        LOGGER("Ubot").info(f"Removed SESSION{i} from .env file due to error.")
                        await app.send_message(SUPPORT, f"Removed SESSION{i} from .env file due to error.")
                        break
    await idle()
    for ex_id in ids:
        await remove_user(ex_id)


              
if __name__ == "__main__":
   install()
   LOOP.run_until_complete(main())
   LOGGER("Info").info("⚡Start pyRainger⚡")