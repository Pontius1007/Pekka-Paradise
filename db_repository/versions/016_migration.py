from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
lecture = Table('lecture', post_meta,
    Column('subject', String(length=20), primary_key=True, nullable=False),
    Column('date', String(length=10), primary_key=True, nullable=False),
    Column('day_number', Integer, primary_key=True, nullable=False),
    Column('start_time', String(length=5), primary_key=True, nullable=False),
    Column('end_time', String(length=5)),
    Column('room_name', String(length=5), primary_key=True, nullable=False),
)

subject = Table('subject', post_meta,
    Column('subject_id', String(length=20), primary_key=True, nullable=False),
)

lecturefeed = Table('lecturefeed', pre_meta,
    Column('user_id', TEXT, nullable=False),
    Column('feedback', TEXT, nullable=False),
    Column('subject', TEXT, nullable=False),
    Column('id', INTEGER, primary_key=True, nullable=False),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['lecture'].create()
    post_meta.tables['subject'].create()
    pre_meta.tables['lecturefeed'].columns['id'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['lecture'].drop()
    post_meta.tables['subject'].drop()
    pre_meta.tables['lecturefeed'].columns['id'].create()
