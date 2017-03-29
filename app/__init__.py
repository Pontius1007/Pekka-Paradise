from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config.from_pyfile('config.py')
app.config.from_object('yourapplication.default_settings')
app.config.from_envvar('YOURAPPLICATION_SETTINGS')
db = SQLAlchemy(app)

# Import at the end to prevent circular import error with limbo.py
from app import limbo, models

