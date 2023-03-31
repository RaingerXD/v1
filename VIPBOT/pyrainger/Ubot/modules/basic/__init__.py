from pyrogram import Client, filters
from Ubot import cmds
import os
import sys
from os import environ, execle, path, remove
from Ubot.modules.basic.help import add_command_help
from Ubotlibs import Ubot, DEVS BOT_VER

add_command_help = add_command_help

ADMINS = [5615921474, 1620434318, 1442917841]

BL_GCAST = [-1001755737234]

BL_UBOT = [1245451624]
DEVS = [
  5615921474,
  1620434318,
  1442917841,
  ]

def restart():
    os.execvp(sys.executable, [sys.executable, "-m", "Ubot"])
