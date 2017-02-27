import os
basedir = os.path.abspath(os.path.dirname(__file__))


DEBUG = os.environ.get('DEBUG', 0)
SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True
