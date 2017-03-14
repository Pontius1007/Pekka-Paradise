from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
lecturefeed = Table('lecturefeed', pre_meta,
    Column('user_id', TEXT, nullable=False),
    Column('feedback', TEXT, nullable=False),
    Column('subject', TEXT, nullable=False),
)

lecturefeedback = Table('lecturefeedback', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_id', String(length=100)),
    Column('feedback', Integer),
    Column('subject', String(length=20)),
    Column('lecture_id', String(length=100)),
)

lecture = Table('lecture', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('subject', String(length=20)),
    Column('year', Integer),
    Column('week_number', Integer),
    Column('day_number', Integer),
    Column('start_time', String(length=5)),
    Column('end_time', String(length=5)),
    Column('room_name', String(length=5)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['lecturefeed'].drop()
    post_meta.tables['lecturefeedback'].create()
    post_meta.tables['lecture'].columns['id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['lecturefeed'].create()
    post_meta.tables['lecturefeedback'].drop()
    post_meta.tables['lecture'].columns['id'].drop()
