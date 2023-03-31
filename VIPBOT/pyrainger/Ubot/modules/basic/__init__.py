from pyrogram import Client, filters
from Ubot import cmds
from Ubot.modules.basic.help import add_command_help
from Ubotlibs import BL_GCAST, DEVS, BOT_VER

#BL_GCAST = [-100]
#BL_GEEZ = [1245451624]
#DEVS = [5615921474]

add_command_help = add_command_help

#BOT_VER = "7.2.0"

def Ubot(command: str, prefixes: cmds):
    def wrapper(func):
        @Client.on_message(filters.command(command, prefixes) & filters.me)
        async def wrapped_func(client, message):
            await func(client, message)

        return wrapped_func

    return wrapper

def Devs(command: str):
    def wrapper(func):
        @Client.on_message(filters.command(command, ".") & filters.user(DEVS))
        def wrapped_func(client, message):
            return func(client, message)

        return wrapped_func

    return wrapper


def restart():
    os.execvp(sys.executable, [sys.executable, "-m", "Ubot"])