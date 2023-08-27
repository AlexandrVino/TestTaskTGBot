import asyncio
from dataclasses import dataclass

from asyncpgsa import PG
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from database.db.schema import users_table


# class, which will keep data for connection with your database
@dataclass
class DBData:
    user: str
    password: str
    database: str
    host: str
    port: int

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def insert_command(**kwargs):
        query = insert(users_table).values(**kwargs).on_conflict_do_update(
            index_elements=['user_id'], set_={users_table.c.last_time_message: kwargs['last_time_message']}
        )
        query.parameters = []
        return query

    @staticmethod
    def get_user_by_id_command(**kwargs):
        query = select(users_table).where(
            users_table.c.user_id == kwargs['user_id']
        )
        query.parameters = []
        return query

    @staticmethod
    def users_today(**kwargs):
        query = select(users_table).where(
            users_table.c.registration_date == kwargs['registration_date']
        )
        query.parameters = []
        return query


# class, which will interact with your database
class DBSession:
    def __init__(self, **kwargs):
        self.db_data = DBData(**kwargs)
        self.pg = PG()

    async def start(self):
        await self.pg.init(**self.db_data.__dict__)

    async def add_user(self, **kwargs) -> None:
        await self.pg.execute(DBData.insert_command(**kwargs))

    async def get_users_today(self, **kwargs) -> None:
        return await self.pg.fetch(DBData.users_today(**kwargs))

    async def get_user(self, user_id: int):
        return await self.pg.fetchrow(DBData.get_user_by_id_command(user_id=user_id))

    async def get_user_or_create(self, **kwargs):
        user = await self.get_user(kwargs['user_id'])
        if user is None:
            await self.add_user(**kwargs)
            user = await self.get_user(kwargs['user_id'])
        return user


async def create_pool(**kwargs) -> DBSession:
    """
    :param kwargs: data for connect to database
    :returns None:
    function, which will return DBSession
    """

    db = DBSession(**kwargs)
    await db.start()
    await asyncio.sleep(3)
    return db
