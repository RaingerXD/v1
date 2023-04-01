from pyrogram import Client, errors, filters
from pyrogram.types import ChatPermissions, Message
from bot.modules.sudo import DEVS, SUDO_USER, OWNER_ID
from bot.helper.PyroHelpers import get_ub_chats
from bot.modules.basic.profile import extract_user, extract_user_and_reason
from bot.modules.help import add_command_help

ok = []


@Client.on_message(filters.command("sudolist", ".") & filters.me)
async def gbanlist(client: Client, message: Message):
    users = (SUDO_USER)
    ex = await message.edit_text("`Processing...`")
    if not users:
        return await ex.edit("Belum ada Pengguna yang ditetapkan")
    gban_list = "**Admin:**\n"
    count = 0
    for i in users:
        count += 1
        gban_list += f"**{count} -** `{i}`\n"
    return await ex.edit(gban_list)


@Client.on_message(filters.command("addsudo", ".") & filters.user(OWNER_ID))
async def gmute_user(client: Client, message: Message):
    args = await extract_user(message)
    reply = message.reply_to_message
    ex = await message.reply_text("`Processing...`")
    if args:
        try:
            user = await client.get_users(args)
        except Exception:
            await ex.edit(f"`Harap tentukan pengguna yang valid!`")
            return
    elif reply:
        user_id = reply.from_user.id
        user = await client.get_users(user_id)
    else:
        await ex.edit(f"`Harap tentukan pengguna yang valid!`")
        return
    if user.id == client.me.id:
        return await ex.edit("**Okay Sure.. 🐽**")

    try:
        if user.id in SUDO_USER:
            return await ex.edit("`Pengguna sudah menjadi admin`")
        SUDO_USER.append(user.id)
        await ex.edit(f"[{user.first_name}](tg://user?id={user.id}) Added To Sudo Users!")
    
    except Exception as e:
        await ex.edit(f"**ERROR:** `{e}`")
        return


@Client.on_message(filters.command("rmsudo", ".") & filters.user(OWNER_ID))
async def gmute_user(client: Client, message: Message):
    args = await extract_user(message)
    reply = message.reply_to_message
    ex = await message.reply_text("`Processing...`")
    if args:
        try:
            user = await client.get_users(args)
        except Exception:
            await ex.edit(f"`Harap tentukan pengguna yang valid!`")
            return
    elif reply:
        user_id = reply.from_user.id
        user = await client.get_users(user_id)
    else:
        await ex.edit(f"`Harap tentukan pengguna yang valid!`")
        return
    if user.id == client.me.id:
        return await ex.edit("**Okay Sure.. 🐽**")

    try:
        if user.id not in SUDO_USER:
            return await ex.edit("`User is not a part of sudo`")
        SUDO_USER.remove(user.id)
        await ex.edit(f"[{user.first_name}](tg://user?id={user.id}) Removed To Sudo Users!")
    
    except Exception as e:
        await ex.edit(f"**ERROR:** `{e}`")
        return



add_command_help(
    "sudos",
    [
        [
            "addsudo <reply/username/userid>",
            "Add any user as Sudo (Use This At your own risk maybe sudo users can control ur account).",
        ],
        ["rmsudo <reply/username/userid>", "Remove Sudo access."],
        ["sudolist", "Displays the Sudo List."],
    ],
)
