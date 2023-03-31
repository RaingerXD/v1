import time
import os
import time
from datetime import datetime
from dotenv import load_dotenv
from config import TIME_LIMIT, TIME_SLEEP, SUPPORT
from Ubot import app


def delete_expired_env_files():
    current_time = time.time()
    for i in range(1, 200):
        env_file = f".env{i}"
        if os.path.isfile(env_file):
            load_dotenv(env_file)
            session_string = os.getenv("SESSION{i}")
            creation_time = os.path.getctime(env_file)
            time_diff = current_time - creation_time
            if time_diff > TIME_LIMIT and session_string is not None:
                os.remove(env_file)
                app.send_message(SUPPORT, f"File {env_file} telah dihapus")

                

with app:
    delete_expired_env_files()
    load_dotenv()
    while True:
        time.sleep(TIME_SLEEP)
        delete_expired_env_files()
