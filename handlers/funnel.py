import asyncio
from datetime import datetime

from pyrogram import Client
from pyrogram.types.messages_and_media.message import Message

from config import DATABASE
from utils.utils import create_update_task, write_csv
from loguru import logger


async def handler_middleware(client: Client, mess: Message):
    dtime = datetime.now()
    user = mess.from_user
    if user is None:
        return

    user_kwargs = {
        'user_id': str(user.id), 'first_name': str(user.first_name),
        'last_name': str(user.last_name), 'username': str(user.username),
        'registration_date': dtime.date(), 'last_time_message': dtime,
    }

    await DATABASE.add_user(**user_kwargs)
    if mess.photo is not None:
        logger.info(
            f"Message Send\n"
            f"Time {dtime}\n"
            f"Data Type: jpg(image)"
        )
        await mess.reply_photo("static/cat.jpg")
    else:
        await asyncio.create_task(create_update_task(client, mess))

    if mess.text is not None and mess.text.startswith('/'):
        await command_middleware(client, mess)
    else:
        pass


async def command_middleware(client: Client, mess: Message):
    if mess.text == '/users_today':
        await users_today_handler(client, mess)


async def users_today_handler(client: Client, mess: Message):
    if mess.from_user.is_self:
        write_csv(await DATABASE.get_users_today(registration_date=datetime.now().date()))
        await client.send_document(document="static/users_today.csv", chat_id=mess.chat.id)
