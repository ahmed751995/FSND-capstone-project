import os
from flask import abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, create_engine, DateTime, ForeignKey
from flask_migrate import Migrate

# database_name = "castingAgency"
database_path = os.environ['DATABASE_URL']    # "postgres:///"+database_name

db = SQLAlchemy()


'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # migrate = Migrate(app, db)


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Base(db.Model):
    __abstract__ = True
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    

class Actor(Base):
    __tablename__ = 'Actor'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    gender = Column(String)
    shows = db.relationship(
        'Show',
        backref='actors',
        cascade="all, delete",
        lazy=True)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

   
    def formate(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }


class Movie(Base):
    __tablename__ = 'Movie'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    release_date = Column(DateTime)
    shows = db.relationship(
        'Show',
        backref='movies',
        cascade="all, delete",
        lazy=True)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def formate(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }


class Show(Base):
    __tablename__ = 'Show'
    id = Column(Integer, primary_key=True)
    actor_id = Column(Integer, ForeignKey('Actor.id'), nullable=False)
    movie_id = Column(Integer, ForeignKey('Movie.id'), nullable=False)

    def __init__(self, actor_id, movie_id):
        self.actor_id = actor_id
        self.movie_id = movie_id

    def formate(self):
        return {
            'id': self.id,
            'actor_id': self.actor_id,
            'movie_id': self.movie_id
        }
