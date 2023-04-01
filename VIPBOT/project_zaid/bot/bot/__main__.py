import asyncio
import importlib
from pyrogram import Client, idle
from bot.helper import join
from bot.modules import ALL_MODULES
from bot import clients, app, ids
from bot.bot import Bot
#extra
from dotenv import load_dotenv

async def start_bot():
    await app.start()
    print("LOG: Founded Bot token Booting..")
    for all_module in ALL_MODULES:
        importlib.import_module("bot.modules" + all_module)
        print(f"Sukses import {all_module} 💥")
    for cli in clients:
        try:
            await cli.start()
            ex = await cli.get_me()
            await join(cli)
            print(f"Start {ex.first_name} 🔥")
            ids.append(ex.id)
        except Exception as e:
            print(f"{e}")
    await idle()

loop = asyncio.get_event_loop()
loop.run_until_complete(start_bot())
