from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
lecturefeedbakevaluation = Table('lecturefeedbakevaluation', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user_id', String(length=100)),
    Column('lecture_id', Integer),
    Column('increased_knowledge', Integer),
    Column('well_organized', Integer),
    Column('logical', Integer),
    Column('use_of_slides', Integer),
    Column('use_of_time', Integer),
    Column('presenter_knowledgeable', Integer),
    Column('general_score', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['lecturefeedbakevaluation'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['lecturefeedbakevaluation'].drop()
