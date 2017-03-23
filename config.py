import os
basedir = os.path.abspath(os.path.dirname(__file__))



# SET DATABASE_URL="LINK-URL" to set it in VENV
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True
