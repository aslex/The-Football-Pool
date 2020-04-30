from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import Column, Integer, String, ForeignKey
import json
from sqlalchemy.orm import relationship

database_filename = 'database.db'
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = 'postgresql://alexservie@localhost:5432/football-pool'

db = SQLAlchemy()


def setup_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


def drop_and_create_all():
    db.drop_all()
    db.create_all()


class User(db.Model):
    __tablename__='users'
    id = Column(Integer, primary_key=True)
    nickname = Column(String, unique=True)

    picks = relationship('Pick', backref='user')

    def __repr__(self):
        return f'<User  id={id} nickname={nickname} >'

class Pick(db.Model):
    __tablename__='picks'
    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('games.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    selection = Column(String)

    def __repr__(self):
        return f'<Pick  id={id} game_id={game_id} user_id={user_id} selection={selection} >'



class Week(db.Model):
    __tablename__ = 'weeks'
    id = Column(Integer, primary_key=True)
    season = Column(Integer)

    games = relationship('Game', backref='week')

    def __repr__(self):
        return f'<Week:  id={id} games={games} season={season} >'

class Game(db.Model):
    __tablename__ = 'games'
    id=Column(Integer, primary_key=True)
    home_team = Column(String, nullable=False)
    away_team = Column(String, nullable=False)
    week_id = Column(Integer, ForeignKey('weeks.id'))

    picks = relationship('Pick', backref='game')

    def __repr__(self):
        return f'<Game:  id: {id} home_team: {home_team}, away_team:{away_team} >'



