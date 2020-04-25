from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import Column, Integer, String

database_filename = 'database.db'
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = 'postgresql://alexservie@localhost:5432/football-pool'

db = SQLAlchemy()


def setup_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


def create_all():
    db.create_all()


class User(db.Model):
    id = Column(Integer(), primary_key=True)
