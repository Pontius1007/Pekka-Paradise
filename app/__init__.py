from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.config.from_pyfile('config')
db = SQLAlchemy(app)

# Import at the end to prevent circular import error with limbo.py
from app import limbo, models

