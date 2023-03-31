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
from pyrogram import Client
from pyrogram.enums import MessagesFilter
from pyrogram.types import Message
from Ubotlibs.Ubot import Ubot
from Ubotlibs.Ubot.helper.basic import edit_or_reply
from Ubot.modules.basic import add_command_help
from Ubot import cmds
from Ubotlibs.Ubot.database.accesdb import *

@Ubot("toanime", cmds)
@check_access
async def convert_image(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.edit("**Mohon Balas Pesan Ini Ke Media**")
    if message.reply_to_message:
        await message.edit("`Processing ...`")
    reply_message = message.reply_to_message
    photo = reply_message.photo.file_id
    bot = "qq_neural_anime_bot"
    xxx = await client.send_photo(bot, photo=photo)
    await asyncio.sleep(20)
    await message.delete()
    async for result in client.search_messages(bot, filter=MessagesFilter.PHOTO, limit=1):
        if result.photo:
            await client.send_photo(message.chat.id, result.photo.file_id, caption=f"**Powered by {client.me.mention}**")
            await result.delete()
            await xxx.delete()
