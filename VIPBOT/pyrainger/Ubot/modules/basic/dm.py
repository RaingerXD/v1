# if you can read this, this meant you use code from Ubot | Ram Project
# this code is from somewhere else
# please dont hestitate to steal it
# because Ubot and Ram doesn't care about credit
# at least we are know as well
# who Ubot and Ram is
#
#
# kopas repo dan hapus credit, ga akan jadikan lu seorang developer
# ©2023 Ubot | Ram Team

import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from Ubotlibs.Ubot import Ubot
from Ubot.modules.basic import add_command_help
from Ubotlibs.Ubot.database.accesdb import *
from Ubot import cmds

@Ubot("dm", cmds)
@check_access
async def dm(coli: Client, memek: Message):
    Ubot = await memek.reply_text("⚡ Proccessing.....")
    quantity = 1
    inp = memek.text.split(None, 2)[1]
    user = await coli.get_chat(inp)
    spam_text = ' '.join(memek.command[2:])
    quantity = int(quantity)

    if memek.reply_to_message:
        reply_to_id = memek.reply_to_message.message_id
        for _ in range(quantity):
            await Ubot.edit("Message Sended Successfully 😘")
            await coli.send_message(user.id, spam_text,
                                      reply_to_messsge_id=reply_to_id)
            await asyncio.sleep(0.15)
        return

    for _ in range(quantity):
        await coli.send_message(user.id, spam_text)
        await Ubot.edit("Message Sended Successfully 😘")
        await asyncio.sleep(0.15)


add_command_help(
    "dm",
    [
        [f"dm @username @username", "Untuk Mengirim Pesan Tanpa Harus Kedalam Roomchat.",],
    ],
)
