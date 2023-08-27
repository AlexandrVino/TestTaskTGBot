import asyncio
import os
from pathlib import Path
from typing import Tuple

from dotenv import load_dotenv
from pyrogram import Client

from database.db.sql import create_pool

PROJECT_PATH = Path(__file__).parent.resolve()


def get_client(api_id, api_hash) -> Client:
    return Client('my_account', api_id, api_hash)


def load_env() -> Tuple[int | None, str | None, str | None]:
    dotenv_path = os.path.join('.env')

    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    return os.environ.get('API_ID'), os.environ.get('API_HASH'), os.environ.get('API_PHONE')


loop = asyncio.get_event_loop()

API_ID, API_HASH, API_PHONE = load_env()
CLIENT = get_client(API_ID, API_HASH)
DATABASE = loop.run_until_complete(create_pool(
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASS"),
    database=os.environ.get("DB_NAME"),
    host=os.environ.get("DB_HOST"),
    port=os.environ.get("DB_PORT")
))
