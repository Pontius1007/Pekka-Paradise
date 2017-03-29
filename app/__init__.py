from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
SQLALCHEMY_DATABASE_URI = "postgres://zmfgqtegrrvgfl:4654c37a586e8e982c610e93aa2453618a4970715eef4c10686da44572d3d39" \
                          "c@ec2-184-72-216-69.compute-1.amazonaws.com:5432/d8avccro5jjpbi"
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

# Import at the end to prevent circular import error with limbo.py
from app import limbo, models

