
import os
import shutil

from pyrogram import Client, filters
from pyrogram.enums import MessageMediaType
from pyrogram.types import Message
from py_extract import Video_tools
from Ubot import cmds
from Ubotlibs.Ubot.database.accesdb import *
from Ubot.modules.basic import add_command_help

# Help
mod_name = os.path.basename(__file__)[:-3]


@Client.on_message(
    filters.command("audio", cmds) & filters.me
)
@check_access
async def extract_all_aud(client: Client, message: Message):
    replied_msg = message.reply_to_message
    geez = await message.reply("`Downloading Video . . .`")
    ext_out_path = os.getcwd() + "/" + "Ubot/py_extract/audios"
    if not replied_msg:
        await geez.edit("**Mohon Balas Ke Video**")
        return
    if not replied_msg.video:
        await geez.edit("**Mohon Balas Ke Video**")
        return
    if os.path.exists(ext_out_path):
        await geez.edit("Processing.....")
        return
    replied_video = replied_msg.video
    try:
        await geez.edit("`Downloading...`")
        ext_video = await client.download_media(message=replied_video)
        await geez.edit("`Extracting Audio(s)...`")
        exted_aud = Video_tools.extract_all_audio(input_file=ext_video, output_path=ext_out_path)
        await geez.edit("`Uploading...`")
        for nexa_aud in exted_aud:
            await message.reply_audio(audio=nexa_aud, caption=f"`Extracted by` {(await client.get_me()).mention}")
        await geez.edit("`Extracting Finished!`")
        shutil.rmtree(ext_out_path)
    except Exception as e:
        await geez.edit(f"**Error:** `{e}`")
        
add_command_help(
    "convert",
    [
        [f"audio <reply to file>", "Convert video to audio"],
    ],
)
