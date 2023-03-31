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
import os
from asyncio import sleep
import os
from Ubotlibs.Ubot import Ubot
from Ubotlibs.Ubot.utils.misc import *
from Ubotlibs.Ubot.helper.PyroHelpers import ReplyCheck
from pyrogram import Client, filters
from pyrogram.types import Message

from Ubot import SUDO_USER

from Ubot.modules.basic import add_command_help
from Ubotlibs.Ubot.database.accesdb import *
from Ubot import cmds

flood = {}
profile_photo = "cache/pfp.jpg"



@Ubot("unblock", cmds)
@check_access
async def unblock_user_func(client: Client, message: Message):
    user_id = await extract_user(message)
    tex = await message.reply_text("`Processing . . .`")
    if not user_id:
        return await message.edit(
            "Berikan username atau reply pesan untuk membuka blokir."
        )
    if user_id == client.me.id:
        return await tex.edit("Ok done ✅.")
    await client.unblock_user(user_id)
    umention = (await client.get_users(user_id)).mention
    await message.edit(f"**Berhasil membuka blokir** {umention}")


@Ubot("block", cmds)
@check_access
async def block_user_func(client: Client, message: Message):
    user_id = await extract_user(message)
    tex = await message.reply_text("`Processing . . .`")
    if not user_id:
        return await tex.edit_text(
            "Berikan username untuk di blok."
        )
    if user_id == client.me.id:
        return await tex.edit_text("ok ✅.")
    await client.block_user(user_id)
    umention = (await client.get_users(user_id)).mention
    await tex.edit_text(f"**Berhasil mem-blokir** {umention}")


@Ubot("setname", cmds)
@check_access
async def setname(client: Client, message: Message):
    tex = await message.reply_text("`Processing . . .`")
    if len(message.command) == 1:
        return await tex.edit(
            "Berikan text untuk diatur sebagai nama anda."
        )
    elif len(message.command) > 1:
        name = message.text.split(None, 1)[1]
        try:
            await client.update_profile(first_name=name)
            await tex.edit(f"**Berhasil mengganti nama menjadi** `{name}`")
        except Exception as e:
            await tex.edit(f"**ERROR:** `{e}`")
    else:
        return await tex.edit(
            "Berikan text untuk diatur sebagai nama anda."
        )


@Ubot("setbio", cmds)
@check_access
async def set_bio(client: Client, message: Message):
    tex = await message.edit_text("`Processing . . .`")
    if len(message.command) == 1:
        return await tex.edit("Berikan text untuk diatur sebagai bio.")
    elif len(message.command) > 1:
        bio = message.text.split(None, 1)[1]
        try:
            await client.update_profile(bio=bio)
            await tex.edit(f"**Berhasil mengganti bio menjadi** `{bio}`")
        except Exception as e:
            await tex.edit(f"**ERROR:** `{e}`")
    else:
        return await tex.edit("Berikan text untuk diatur sebagai bio.")


@Ubot("setpp", cmds)
@check_access
async def set_pfp(client: Client, message: Message):
    replied = message.reply_to_message
    if (
        replied
        and replied.media
        and (
            replied.photo
            or (replied.document and "image" in replied.document.mime_type)
        )
    ):
        await client.download_media(message=replied, file_name=profile_photo)
        await client.set_profile_photo(profile_photo)
        if os.path.exists(profile_photo):
            os.remove(profile_photo)
        await message.reply_text("**Foto profil berhasil di ganti.**")
    else:
        await message.reply_text(
            "Balas ke gamabr/foto untuk atur sebagai foto profil"
        )
        await sleep(3)
        await message.delete()


@Ubot("setppv", cmds)
@check_access
async def view_pfp(client: Client, message: Message):
    user_id = await extract_user(message)
    if user_id:
        user = await client.get_users(user_id)
    else:
        user = await client.get_me()
    if not user.photo:
        await message.reply_text("Foto profil tidak ditemukan!")
        return
    await client.download_media(user.photo.big_file_id, file_name=profile_photo)
    await client.send_photo(
        message.chat.id, profile_photo, reply_to_message_id=ReplyCheck(message)
    )
    await message.delete()
    if os.path.exists(profile_photo):
        os.remove(profile_photo)


add_command_help(
    "profile",
    [
        [f"block", "Blokir pengguna"],
        [f"unblock", "membuka blokir"],
        [f"setname", "mengatur nama anda."],
        [f"setbio", "mengatur bio anda."],
        [f"setpp", "balas ke gambar untuk atur sebagai foto profil."],
        [f"setppv", "balas ke video untuk atur sebagai foto profil."],
    ],
)
