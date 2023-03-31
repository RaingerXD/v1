import asyncio
from threading import Event

from pyrogram import Client, enums, filters
from pyrogram.types import Message
from Ubotlibs.Ubot.helper.basic import edit_or_reply
from Ubotlibs.Ubot.utils.misc import extract_args
from Ubotlibs.Ubot import Ubot
from Ubotlibs import BL_GCAST
from config import BOTLOG_CHATID
from Ubot import cmds
from Ubotlibs.Ubot.database.accesdb import *

from Ubot.modules.basic.help import add_command_help
SPAM_COUNT = [0]
commands = ["spam", "statspam", "slowspam", "restspam"]

def increment_spam_count():
    SPAM_COUNT[0] += 1
    return spam_allowed()


def spam_allowed():
    return SPAM_COUNT[0] < 1000


@Ubot("dspam", cmds)
@check_access
async def delayspam(client: Client, message: Message):
    #if message.chat.id in BL_GCAST:
    #    return await edit_or_reply(
    #        message, "**Gabisa Digunain Disini Tod!!**"
    #    )
    delayspam = await extract_args(message)
    arr = delayspam.split()
    if len(arr) < 3 or not arr[0].isdigit() or not arr[1].isdigit():
        await message.edit("`Something seems missing / wrong.`")
        return
    delay = int(arr[0])
    count = int(arr[1])
    spam_message = delayspam.replace(arr[0], "", 1)
    spam_message = spam_message.replace(arr[1], "", 1).strip()
    await message.delete()

    if not spam_allowed():
        return

    delaySpamEvent = Event()
    for i in range(0, count):
        if i != 0:
            delaySpamEvent.wait(delay)
        await client.send_message(message.chat.id, spam_message)
        limit = increment_spam_count()
        if not limit:
            break

    await client.send_message(
        BOTLOG_CHATID, "**#DELAYSPAM**\nDelaySpam was executed successfully"
    )


@Ubot(commands, cmds)
@check_access
async def sspam(client: Client, message: Message):
    amount = int(message.command[1])
    text = " ".join(message.command[2:])

    cooldown = {"spam": 0, "statspam": 2.0, "slowspam": 2.5, "restspam": 1}

    await message.delete()

    for msg in range(amount):
        if message.reply_to_message:
            sent = await message.reply_to_message.reply(text)
        else:
            sent = await client.send_message(message.chat.id, text)

        if message.command[0] == "statspam":
            await asyncio.sleep(0.1)
            await sent.delete()

        await asyncio.sleep(cooldown[message.command[0]])


@Ubot("sspam", cmds)
@check_access
async def spam_stick(client: Client, message: Message):
    if not message.reply_to_message:
        await edit_or_reply(
            message, "**Reply to a sticker with amount you want to spam**"
        )
        return
    if not message.reply_to_message.sticker:
        await edit_or_reply(
            message, "**Reply to a sticker with amount you want to spam**"
        )
        return
    else:
        i = 0
        times = message.command[1]
        if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            for i in range(int(times)):
                sticker = message.reply_to_message.sticker.file_id
                await client.send_sticker(
                    message.chat.id,
                    sticker,
                )
                await asyncio.sleep(0.10)

        if message.chat.type == enums.ChatType.PRIVATE:
            for i in range(int(times)):
                sticker = message.reply_to_message.sticker.file_id
                await client.send_sticker(message.chat.id, sticker)
                await asyncio.sleep(0.10)

add_command_help(
    "spam",
    [
        [f"dspam [jumlah] [waktu delay] [kata kata]","delay spam.",],
        [f"dspam [jumlah] [waktu delay] [kata kata]","delay spam.",],
        [f"sspam [balas ke stiker] [jumlah spam]","spam stiker.",],
    ],
)

commands = ["spam", "statspam", "slowspam", "restspam"]