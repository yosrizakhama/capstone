import os
from sqlalchemy.sql.expression import func
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from flask_cors import CORS
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column as c
from flask_migrate import Migrate

database_path = os.environ['DATABASE_PATH']   # --for local server
# database_path = os.environ['DATABASE_URL']
db = SQLAlchemy()
migrate = Migrate()
Base = declarative_base()
app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = database_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.app = app
db.init_app(app)
migrate.init_app(app, db)
db.create_all()

# table for many to many relation between actor and movie
ActorMovie = db.Table('actormovie',
                      c('actor_id', db.Integer,
                        db.ForeignKey('actor.id', primary_key=True)),
                      c('movie_id', db.Integer,
                        db.ForeignKey('movie.id', primary_key=True)))


class Actor(db.Model):
    __tablename__ = 'actor'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    name = db.Column(db.String(120))
    age = db.Column(db.Integer())
    genre = db.Column(db.String(1))

    def __init__(self, name, age, genre):
        self.name = name
        self.age = age
        self.genre = genre

    def __repr__(self):
        s = str(self.age)+"\n-genre: "+self.genre
        ch = str(self.id)+"\n-name: "+self.name+"\n-age: " + s
        return "Todo : \n-ID: " + ch

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        try:
            actor_movie = ActorMovie.delete().where(actor_id == self.id)
            db.engine.execute(actor_movie)
        except Exception:
            print("not OK")
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    title = db.Column(db.String(120))
    date = db.Column(db.DateTime())
    actors = db.relationship('Actor', secondary=ActorMovie,
                             backref=backref('movies', lazy=True))

    def __init__(self, title, date):
        self.title = title
        self.date = date

    def __repr__(self):
        return "Todo : \n-ID: "+str(self.id)+"\n-title: "+self.title

    def insert(self):
        try:
            max = db.session.query(func.max(Movie.id)).scalar()+1
        except Exception:
            max = 1
        self.id = max
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        try:
            actor_movie = ActorMovie.delete().where(movie_id == self.id)
            db.engine.execute(actor_movie)
        except Exception:
            print("not OK")
        db.session.delete(self)
        db.session.commit()
