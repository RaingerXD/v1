from pyrogram import Client, filters
from Ubot import cmds
import os
import sys
from os import environ, execle, path, remove
from Ubot.modules.basic.help import add_command_help
from Ubotlibs import Ubot, DEVS, BOT_VER, ADMINS, BL_GCAST

add_command_help = add_command_help


BL_UBOT = [-1001755737234]

def restart():
    os.execvp(sys.executable, [sys.executable, "-m", "Ubot"])
