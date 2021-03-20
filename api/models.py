import datetime

from .app import db


# Defining the AudioBook Model
class AudioBook(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    title_of_audiobook = db.Column(db.String(100), nullable=False)
    author_of_title = db.Column(db.String(100), nullable=False)
    narrator = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    uploaded_time = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __init__(self, title_of_audiobook, author_of_title, narrator, duration, uploaded_time):
        self.title_of_audiobook = title_of_audiobook
        self.author_of_title = author_of_title
        self.narrator = narrator
        self.duration = duration
        self.uploaded_time = uploaded_time


# Defining the Song Model
class Song(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    name_of_song = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    uploaded_time = db.Column(
        db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    def __init__(self, name_of_song, duration, uploaded_time):
        self.name_of_song = name_of_song
        self.duration = duration
        self.uploaded_time = uploaded_time
