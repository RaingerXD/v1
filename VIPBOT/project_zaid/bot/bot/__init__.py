from pyrogram import Client
# extra
#from config import API_ID, API_HASH, SUDO_USERS, OWNER_ID, BOT_TOKEN, STRING_SESSION1, STRING_SESSION2, STRING_SESSION3, STRING_SESSION4, STRING_SESSION5, STRING_SESSION6, STRING_SESSION7, STRING_SESSION8, STRING_SESSION9, STRING_SESSION10
from datetime import datetime
import time
from aiohttp import ClientSession
# dari bot string
import logging
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler
from bot.get_config import get_config
# dari bot string
load_dotenv("config.env")

StartTime = time.time()
START_TIME = datetime.now()
CMD_HELP = {}
SUDO_USER = SUDO_USERS
clients = []
ids = []

# extra
cmds = ["!", "?", "*", "-", "^", "."]
CMD_HELP = {}
clients = []
ids = []

SUDOERS = filters.user()
SUDO_USER = SUDOERS

# extra
if LOG_GROUP:
   LOG_GROUP = LOG_GROUP
else:
   LOG_GROUP = "me"

"""
app = Client(
    name="bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="bot/modules/bot"),
    in_memory=True,
)
"""

####### terusan dari bot string
API_HASH = get_config("API_HASH", should_prompt=True)
###
APP_ID = get_config("APP_ID", should_prompt=True)
# get a token from @BotFather
BOT_TOKEN = get_config("BOT_TOKEN", should_prompt=True)
####
BOT_WORKERS = int(get_config("TG_BOT_WORKERS", "4"))
#
COMMM_AND_PRE_FIX = get_config("COMMM_AND_PRE_FIX", "/")
# start command
START_COMMAND = get_config("START_COMMAND", "start")
# path to store LOG files
LOG_FILE_ZZGEVC = get_config("LOG_FILE_ZZGEVC", "rainger.log")


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_ZZGEVC,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    """ get a Logger object """
    return logging.getLogger(name)


# a dictionary to store the currently running processes
AKTIFPERINTAH = {}
# /start message when other users start your bot
START_OTHER_USERS_TEXT = get_config(
    "START_OTHER_USERS_TEXT",
    (
        """
        Selamat Datang Di Rainger Session
        """
    )
)
INPUT_PHONE_NUMBER = get_config("INPUT_PHONE_NUMBER", (
    "Masukkan Nomor Akun Telegram"
))
RECVD_PHONE_NUMBER_DBP = get_config("RECVD_PHONE_NUMBER_DBP", (
    "Mencoba mengirim otp, silahkan cek otp"
))
ALREADY_REGISTERED_PHONE = get_config("ALREADY_REGISTERED_PHONE", (
    "Periksa Pesan Masuk"
))
CONFIRM_SENT_VIA = get_config("CONFIRM_SENT_VIA", (
    "kode otp dikirim dari {}"
))
RECVD_PHONE_CODE = get_config("RECVD_PHONE_CODE", (
    "Mencoba mengirim otp, silahkan cek otp"
))
NOT_REGISTERED_PHONE = get_config("NOT_REGISTERED_PHONE", (
    "Nomor terverifikasi belum terdaftar tele gan"
))
PHONE_CODE_IN_VALID_ERR_TEXT = get_config(
    "Kode otp salah su. ketik atau tekan ini /start"
)
TFA_CODE_IN_VALID_ERR_TEXT = get_config(
    "Kode verif salah su. ketik atau tekan ini /start"
)
ACC_PROK_WITH_TFA = get_config("ACC_PROK_WITH_TFA", (
    "Diverif 2 langkah nih, paste dibawah cuy"
))
SESSION_GENERATED_USING = get_config("SESSION_GENERATED_USING", (
    "Terima kasih telah menggunakan bot ini ..."
))


if STRING_SESSION1:
   print("Client1: Found.. Starting..📳")
   client1 = Client(name="one", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION1, plugins=dict(root="bot/modules"))
   clients.append(client1)

if STRING_SESSION2:
   print("Client2: Found.. Starting.. 📳")
   client2 = Client(name="two", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION2, plugins=dict(root="bot/modules"))
   clients.append(client2)

if STRING_SESSION3:
   print("Client3: Found.. Starting.. 📳")
   client3 = Client(name="three", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION3, plugins=dict(root="bot/modules"))
   clients.append(client3)

if STRING_SESSION4:
   print("Client4: Found.. Starting.. 📳")
   client4 = Client(name="four", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION4, plugins=dict(root="bot/modules"))
   clients.append(client4)

if STRING_SESSION5:
   print("Client5: Found.. Starting.. 📳")
   client5 = Client(name="five", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION5, plugins=dict(root="bot/modules"))
   clients.append(client5)

if STRING_SESSION6:
   print("Client6: Found.. Starting.. 📳")
   client6 = Client(name="six", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION6, plugins=dict(root="bot/modules"))
   clients.append(client6)

if STRING_SESSION7:
   print("Client7: Found.. Starting.. 📳")
   client7 = Client(name="seven", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION7, plugins=dict(root="bot/modules"))
   clients.append(client7)

if STRING_SESSION8:
   print("Client8: Found.. Starting.. 📳")
   client8 = Client(name="eight", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION8, plugins=dict(root="bot/modules"))
   clients.append(client8)

if STRING_SESSION9:
   print("Client9: Found.. Starting.. 📳")
   client9 = Client(name="nine", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION9, plugins=dict(root="bot/modules"))
   clients.append(client9)

if STRING_SESSION10:
   print("Client10: Found.. Starting.. 📳")
   client10 = Client(name="ten", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION10, plugins=dict(root="bot/modules")) 
   clients.append(client10)
