from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
lecturefeedbakevaluation = Table('lecturefeedbakevaluation', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('user_id', VARCHAR(length=100)),
    Column('lecture_id', INTEGER),
    Column('increased_knowledge', INTEGER),
    Column('well_organized', INTEGER),
    Column('logical', INTEGER),
    Column('use_of_slides', INTEGER),
    Column('use_of_time', INTEGER),
    Column('presenter_knowledgeable', INTEGER),
    Column('general_score', INTEGER),
)

lecturefeedbackevaluation = Table('lecturefeedbackevaluation', post_meta,
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
    pre_meta.tables['lecturefeedbakevaluation'].drop()
    post_meta.tables['lecturefeedbackevaluation'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['lecturefeedbakevaluation'].create()
    post_meta.tables['lecturefeedbackevaluation'].drop()
