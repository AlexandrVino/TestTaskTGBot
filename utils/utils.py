import asyncio
from datetime import datetime, timedelta
from typing import Dict, List

from loguru import logger

TASKS: Dict = {}
TEXTS = {
    0.02: "Test",
    10: "Добрый день!",
    90: "Подготовила для вас материал",
    120: "Скоро вернусь с новым материалом!"
}


def write_csv(data: List[Dict]):
    headers = list(data[0].keys())

    with open('static/users_today.csv', 'w') as file:
        file.write(';'.join(map(str, headers)) + '\n')
        for row in data:
            file.write(';'.join(map(str, row.values())) + '\n')


async def create_update_task(client, mess, timer=[10, 90, 120]):
    user_id = mess.from_user.id
    if TASKS.get(user_id) is None:
        TASKS[user_id] = {}

    if TASKS.get(user_id):
        for time, task in TASKS[user_id].items():
            task.cancel()
        TASKS[user_id] = {}

    for time in timer:
        TASKS[user_id][time] = asyncio.create_task(notify_task(client, time, mess))
    for task in TASKS[user_id].values():
        await task


async def notify_task(client, time_to_sleep, mess):
    await asyncio.sleep(time_to_sleep * 60)

    dtime = datetime.now()
    messages = [
        message.text
        async for message in client.get_chat_history(mess.chat.id)
        if message.date + timedelta(hours=2) >= dtime
    ]
    if time_to_sleep == 120 and any(txt.lower() == "хорошего дня" for txt in messages):
        return

    logger.info(
        f"Message Send\n"
        f"Time {dtime}\n"
        f"Data Type: text (notify after {time_to_sleep} minutes)"
    )
    await mess.reply(TEXTS[time_to_sleep])
