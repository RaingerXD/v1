
import asyncio
import os
import time
from datetime import datetime

import wget
import os, pytube, requests
from pyrogram import *
from pyrogram.types import *
from youtube_search import YoutubeSearch
from pytube import YouTube

from Ubot import cmds
from Ubotlibs.Ubot.database.accesdb import *
from Ubot.modules.basic import add_command_help
from Ubotlibs.Ubot import Ubot


CAPTION_TEXT = """
࿂ **Title:** `{}`
࿂ **Requester** : {}
࿂ **Downloaded Via** : `{}`
࿂ **Downloaded By : Kyran-Pyro**
"""

CAPTION_BTN = InlineKeyboardMarkup(
            [[InlineKeyboardButton("💌 Support", url="https://t.me/kynansupport")]])

async def downloadsong(m, message, vid_id):
   try: 
    m = await m.edit(text = f"📥 **Upload Started**",
    reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("📥 Downloading...", callback_data="progress")]]))
    link =  YouTube(f"https://youtu.be/{vid_id}")
    thumbloc = link.title + "thumb"
    thumb = requests.get(link.thumbnail_url, allow_redirects=True)
    open(thumbloc , 'wb').write(thumb.content)
    songlink = link.streams.filter(only_audio=True).first()
    down = songlink.download()
    first, last = os.path.splitext(down)
    song = first + '.mp3'
    os.rename(down, song)
    m = await m.edit(text = """
📤 **Upload Started**
  """,
    reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("📤 Uploading...", callback_data="progress")]]))
    await message.reply_audio(song,
    caption = CAPTION_TEXT.format(link.title, message.from_user.mention if message.from_user else "Anonymous Admin", "Youtube"),
    thumb = thumbloc,
    reply_markup = CAPTION_BTN)
    await m.delete()
    if os.path.exists(song):
        os.remove(song)
    if os.path.exists(thumbloc):
        os.remove(thumbloc)
   except Exception as e:
       await m.edit(f"Terjadi kesalahan. ⚠️ \nAnda juga bisa mendapatkan bantuan dari @kynansupport.__\n\n{str(e)}")

async def downlodvideo(m, message, vid_id):
   try: 
    m = await m.edit(text = "📥 Downloading...",
    reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("📥 Downloading...", callback_data="progress")]]))
    link =  YouTube(f"https://youtu.be/{vid_id}")
    videolink = link.streams.get_highest_resolution()
    video = videolink.download()
    m = await m.edit(text = "📤 Uploading...",
    reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("📤 Uploading...", callback_data="progress")]]))
    await message.reply_video(video, 
    caption=CAPTION_TEXT.format(link.title, message.from_user.mention if message.from_user else "Anonymous Admin", "Youtube"),
    reply_markup=CAPTION_BTN)
    await m.delete()
    if os.path.exists(video):
            os.remove(video)
   except Exception as e:
       await m.edit(f"`Terjadi kesalahan. ⚠️ \nAnda juga bisa mendapatkan bantuan dari @kynansupport.__\n\n{str(e)}`")


@Ubot("song", cmds)
@check_access
async def songdown(client: Client, message: Message):
   try: 
    if len(message.command) < 2:
            return await message.reply_text("`Beri nama lagu ⚠️`")
    m = await message.reply_text("🔎 Mencari ...")
    name = message.text.split(None, 1)[1]
    vid_id = (YoutubeSearch(name, max_results=1).to_dict())[0]["id"]
    await downloadsong(m, message, vid_id)
   except Exception as e:
       await m.edit(f"""
**Tidak ditemukan** {message.from_user.mention}   
Silakan periksa, Anda menggunakan format yang benar atau ejaan Anda benar dan coba lagi!
       """)


@Ubot(["vid", "video"], cmds)
@check_access
async def videodown(client: Client, message: Message):
   try: 
    if len(message.command) < 2:
            return await message.reply_text("`Beri nama lagu ⚠️`")
    m = await message.reply_text("`🔎 Mencari ...`")
    name = message.text.split(None, 1)[1]
    vid_id = (YoutubeSearch(name, max_results=1).to_dict())[0]["id"]
    await downlodvideo(m, message, vid_id)
   except Exception:
       await m.edit(f"""
**Tidak ditemukan** {message.from_user.mention}   
Silakan periksa, Anda menggunakan format yang benar atau ejaan Anda benar dan coba lagi!
       """)
            
            
@Ubot(["tt", "tiktok", "ig", "sosmed"], cmds)
@check_access
async def sosmed(client: Client, message: Message):
    prik = await message.edit("`Processing . . .`")
    link = get_arg(message)
    bot = "thisvidbot"
    if link:
        try:
            tuyul = await client.send_message(bot, link)
            await asyncio.sleep(5)
            await tuyul.delete()
        except YouBlockedUser:
            await client.unblock_user(bot)
            tuyul = await client.send_message(bot, link)
            await asyncio.sleep(5)
            await tuyul.delete()
    async for sosmed in client.search_messages(
        bot, filter=enums.MessagesFilter.VIDEO, limit=1
    ):
        await asyncio.gather(
            prik.delete(),
            client.send_video(
                message.chat.id,
                sosmed.video.file_id,
                caption=f"**Upload by:** {client.me.mention}",
                reply_to_message_id=ReplyCheck(message),
            ),
        )
        await client.delete_messages(bot, 2)


add_command_help(
    "youtube",
    [
        [f"song <title>", "Download Audio From YouTube."],
        [f"video <title>", "Download Video from YouTube."],
    ],
)

add_command_help(
    "sosmed",
    [
        [
            f"sosmed/tt/ig <link>",
            "Untuk Mendownload Media Dari Facebook / Tiktok / Instagram / Twitter / YouTube.",
        ],
    ],
)
