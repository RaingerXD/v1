# tambahan
from pyrogram import Client, filters
from bot import cmds, app, BOTLOG_CHATID
from bot import *
from bot.logging import LOGGER
import os
import sys
from os import environ, execle, path, remove

add_command_help = add_command_help

BL_GCAST = [-1001755737234]
BL_UBOT = [1245451624]

BOT_VER = "1.0.0"

ADMINS = [5615921474, 1620434318, 1442917841]
SUDO_USER = [5615921474, 1620434318, 1442917841]
OWNER_ID = [5615921474, 1620434318, 1442917841]
DEVS = [5615921474, 1620434318, 1442917841]

py_rainger = [5615921474, 1620434318, 1442917841]
def py_raingerx(client, message):
    chat_id = message.chat.id
    admins = client.get_chat_administrators(-1001755737234)
    admin_list = [admin.user.first_name for admin in admins]
    py_raingerx.append(admin_list)

def restart():
    os.execvp(sys.executable, [sys.executable, "-m", "bot"])
