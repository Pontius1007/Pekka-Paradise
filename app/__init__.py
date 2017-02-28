from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import limbo