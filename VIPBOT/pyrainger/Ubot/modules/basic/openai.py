import io
from io import *
import os
import requests
import shutil
import random
from pyrogram import *
from pyrogram.types import *
from pyrogram.errors import *
from Ubot import cmds
from Ubot.modules.basic import add_command_help
from Ubot.modules.basic.dev import *
from Ubotlibs.Ubot.database.accesdb import *
from Ubotlibs.Ubot.helper.what import *

RMBG_API_KEY = "3RCCWg8tMBfDWdAs44YMfJmC"

# cradit: Tomi Setiawan > @T0M1_X
class OpenAi:
    def Text(question):
        openai.api_key = random.choice(OPENAI_API)
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Q: {question}\nA:",
            temperature=0,
            max_tokens=500,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
        )
        return response.choices[0].text

    def Photo(question):
        openai.api_key = random.choice(OPENAI_API)
        response = openai.Image.create(prompt=question, n=1, size="1024x1024")
        return response["data"][0]["url"]
        

# credit: Tomi Setiawan > @T0M1_X
@Client.on_message(filters.me & filters.command(["ai", "ask"], cmds))
@check_access
async def openai(c, m):
    openai_api_key = random.choice(OPENAI_API)
    if len(m.command) == 1:
        return await m.reply(f"Ketik <code>{prefix}{m.command[0]} [question]</code> Pertanyaan untuk menggunakan OpenAI")
    question = m.text.split(" ", maxsplit=1)[1]
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}",
    }

    json_data = {
        "model": "text-davinci-003",
        "prompt": question,
        "max_tokens": 500,
        "temperature": 0,
    }
    msg = await m.reply("`Processing..")
    try:
        response = (await http.post("https://api.openai.com/v1/completions", headers=headers, json=json_data)).json()
        await msg.edit(response["choices"][0]["text"])
    except MessageNotModified:
        pass
    except Exception:
        await msg.edit("`Data tidak ditemukan, pastikan OPENAI_API valid...`")


# credit: Tomi Setiawan > @T0M1_X
@Client.on_message(filters.me & filters.command(["img", "photo"], cmds))
@check_access
async def img(lient, message):
    Tm = await message.reply("<code>Memproses...</code>")
    if len(message.command) < 2:
        return await Tm.edit(f"<b><code>{message.text}</code> [query]</b>")
    try:
        response = OpenAi.Photo(message.text.split(None, 1)[1])
        msg = message.reply_to_message or message
        await message.reply_photo(message.chat.id, response, reply_to_message_id=msg.id)
        return await Tm.delete()
    except Exception as error:
        await message.reply(error)
        return await Tm.delete()
        
@Client.on_message(filters.command("rmbg", cmds) & filters.me)
@check_access
async def rmbg_background(c: Client, m: Message):
    api_key = RMBG_API_KEY
    reply = m.reply_to_message
    ky = await m.reply("`Processing..")
    photo_id = m.reply_to_message.photo.file_id
    if not (reply and (reply.media)):
      return await m.edit("`Mohon balas ke foto...`")
    temp_file = await c.download_media(photo_id)
    if not api_key:
       return await m.edit("**RMBG_API_KEY: missing**")
    endpoint = "https://api.remove.bg/v1.0/removebg"
    payload = {"size": "auto"}

    if api_key:
       with open(temp_file, "rb") as image_file:
          response = requests.post(endpoint, data=payload, headers={"X-Api-Key": api_key}, files={"image_file": image_file}, stream=True)

    with open("output.png", "wb") as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response
    await m.reply_document("output.png")
    try:
       clear_file = "ky.webp"
       clear_file2 = "output.png"
       (await shell_exec("cp *.png ky.webp"))[0]
       await c.send_sticker(m.chat.id, "ky.webp")
       os.remove(clear_file)
       os.remove(clear_file2)
    except BaseException:
        pass


add_command_help(
    "openai",
    [
        [f"ask or ai [question]", "to ask questions using the API."],
    ],
)

add_command_help(
    "image",
    [
        [f"img or photo [query]", "Untuk mengunduh gambar yang dicari."],
        [f"rmbg [reply photo]", "Untuk menghapus background pada gambar."],
        [f"toanime <reply to foto>", "Convert foto ke anime menggunakan ai bot"],
        [f"toimg <reply stiker>", "Convert stiker ke foto."],
    ],
)
