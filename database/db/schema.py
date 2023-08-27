
from sqlalchemy import (Column, DateTime, Date, MetaData, String, Table)

convention = {
    'all_column_names': lambda constraint, table: '_'.join([
        column.name for column in constraint.columns.values()
    ]),
    'ix': 'ix__%(table_name)s__%(all_column_names)s',  # Именование индексов
    'uq': 'uq__%(table_name)s__%(all_column_names)s',  # Именование уникальных индексов
    'ck': 'ck__%(table_name)s__%(constraint_name)s',  # Именование CHECK-constraint-ов
    'fk': 'fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s',  # Именование внешних ключей
    'pk': 'pk__%(table_name)s'  # Именование первичных ключей
}
metadata = MetaData(naming_convention=convention)


users_table = Table(
    'users_table',
    metadata,
    Column('user_id', String, primary_key=True),
    Column('first_name', String, nullable=False),
    Column('last_name', String, nullable=False),
    Column('username', String, nullable=False),
    Column('registration_date', Date, nullable=True),
    Column('last_time_message', DateTime, nullable=True)
)
