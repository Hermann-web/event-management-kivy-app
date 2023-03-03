from sqlalchemy import Table, Column, String, MetaData, Boolean
from sqlalchemy import create_engine

engine = create_engine('sqlite:///tasks.db', echo=True)
meta = MetaData()
tasks = Table(
    'tasks', meta,
    Column('task', String, primary_key=True),
    Column('is_done', Boolean, default=False),
)
meta.create_all(engine)
