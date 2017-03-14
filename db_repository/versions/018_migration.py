from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
lecture = Table('lecture', post_meta,
    Column('subject', String(length=20), primary_key=True, nullable=False),
    Column('week_number', Integer),
    Column('day_number', Integer, primary_key=True, nullable=False),
    Column('start_time', String(length=5), primary_key=True, nullable=False),
    Column('end_time', String(length=5)),
    Column('room_name', String(length=5), primary_key=True, nullable=False),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['lecture'].columns['week_number'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['lecture'].columns['week_number'].drop()
