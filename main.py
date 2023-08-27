from pyrogram.handlers import MessageHandler

from config import CLIENT
from handlers.funnel import handler_middleware
from utils.utils import TASKS


def custom_exit():
    for tasks in TASKS.values():
        for task in tasks:
            task.cancel()


def main():
    CLIENT.add_handler(MessageHandler(handler_middleware))
    CLIENT.run()


if __name__ == '__main__':
    # asyncio.run(main())
    main()

