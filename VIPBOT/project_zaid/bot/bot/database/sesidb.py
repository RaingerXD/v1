import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from bot.database import cli

collection = cli["session_string"]
load_dotenv()


session_strings = []
for i in range(1, 32):
    session_var_name = f"SESSION{i}"
    session_string = os.getenv(session_var_name)
    if session_string:
        session_strings.append(session_string)


for session_string in session_strings:
    existing_session = collection.find_one({"session_string": session_string})
    if existing_session:
        print(f"Session '{session_string}' already exists")
    else:
        session_data = {"session_string": session_string}
        collection.insert_one(session_data)
        print(f"Session '{session_string}' saved successfully")
