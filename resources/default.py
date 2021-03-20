from flask_restful import Resource
from flask_restful import Api, Resource, marshal_with, reqparse, fields, abort

from api.app import api
from api.app import db
from api.models import AudioBook, Song


audiobook_args = reqparse.RequestParser()
audiobook_args.add_argument(
    "title_of_audiobook", type=str, required=True, help="Title of audiobook is required")
audiobook_args.add_argument(
    "author_of_title", type=str, required=True, help="Author of title is required")
audiobook_args.add_argument(
    "narrator", type=str, required=True, help="Narrator is required")
audiobook_args.add_argument("duration", type=int, required=True,
                            help="Duration of audiobook is required in number")
audiobook_args.add_argument("uploaded_time")

audiobook_update_args = reqparse.RequestParser()
audiobook_update_args.add_argument("title_of_audiobook", type=str)
audiobook_update_args.add_argument("author_of_title", type=str)
audiobook_update_args.add_argument("narrator", type=str)
audiobook_update_args.add_argument("duration", type=int)

resource_audiobook_fields = {
    "id": fields.Integer,
    "title_of_audiobook": fields.String,
    "author_of_title": fields.String,
    "narrator": fields.String,
    "duration": fields.Integer,
    "uploaded_time": fields.String,
}


song_args = reqparse.RequestParser()
song_args.add_argument("name_of_song", type=str,
                       required=True, help="Name of song is required")
song_args.add_argument("duration", type=int, required=True,
                       help="Duration of song is required in number")
song_args.add_argument("uploaded_time")

song_update_args = reqparse.RequestParser()
song_update_args.add_argument("name_of_song", type=str)
song_update_args.add_argument("duration", type=int)


resource_song_fields = {
    "id": fields.Integer,
    "name_of_song": fields.String,
    "duration": fields.Integer,
    "uploaded_time": fields.String,
}


class AudioBookR(Resource):
    @marshal_with(resource_audiobook_fields)
    def get(self, audio_id=None):
        if audio_id is None:
            audiobook = AudioBook.query.all()
            return audiobook, 200
        else:
            audiobook = AudioBook.query.filter_by(id=audio_id).first_or_404(
                description="Audiobook with that id not found")
            return audiobook, 200

    @marshal_with(resource_audiobook_fields)
    def post(self, audio_id):
        args = audiobook_args.parse_args()
        result = AudioBook.query.filter_by(id=audio_id).first()
        if result:
            abort(409, message="Post with that video id already exist!")
        elif args['duration'] < 1:
            abort(400, message="Duration can't be negative")
        else:
            new_audiobook = AudioBook(
                title_of_audiobook=args['title_of_audiobook'], author_of_title=args['author_of_title'], narrator=args['narrator'], duration=args['duration'], uploaded_time=args['uploaded_time'])
            db.session.add(new_audiobook)
            db.session.commit()
            return new_audiobook, 201

    @marshal_with(resource_audiobook_fields)
    def patch(self, audio_id):
        args = audiobook_update_args.parse_args()
        audio = AudioBook.query.filter_by(id=audio_id).first()
        if not audio:
            abort(404, message="Audiobook with that id not found")
        else:
            if args['title_of_audiobook'] != None:
                audio.title_of_audiobook = args['title_of_audiobook']
            if args['author_of_title'] != None:
                audio.author_of_title = args['author_of_title']
            if args['narrator'] != None:
                audio.narrator = args['narrator']
            if args['duration'] != None:
                if args['duration'] < 1:
                    abort(400, message="Duration can't be negative")
                else:
                    audio.duration = args['duration']
            db.session.commit()
            return audio, 200

    @marshal_with(resource_audiobook_fields)
    def delete(self, audio_id):
        audio = AudioBook.query.filter_by(id=audio_id).first()
        if audio:
            db.session.delete(audio)
            db.session.commit()
            return audio, 200
        else:
            abort(404, message="Audiobook with that id doesn't exist!")


class SongR(Resource):
    @marshal_with(resource_song_fields)
    def get(self, song_id=None):
        if song_id is None:
            songs = Song.query.all()
            return songs, 200
        else:
            song = Song.query.filter_by(id=song_id).first_or_404(
                description="Song with that id not found")
            return song, 200

    @marshal_with(resource_song_fields)
    def post(self, song_id):
        args = song_args.parse_args()
        song = Song.query.filter_by(id=song_id).first()
        if song:
            abort(409, message="Song with that id already exist!")
        elif args['duration'] < 1:
            abort(400, message="Duration can't be negative")
        else:
            new_song = Song(
                name_of_song=args['name_of_song'], duration=args['duration'], uploaded_time=args['uploaded_time'])
            db.session.add(new_song)
            db.session.commit()
            return new_song, 201

    @marshal_with(resource_song_fields)
    def patch(self, song_id):
        args = song_update_args.parse_args()
        song = Song.query.filter_by(id=song_id).first()
        if not song:
            abort(404, message="Song with that id not found")
        else:
            if args['name_of_song'] != None:
                song.name_of_song = args['name_of_song']
            if args['duration'] != None:
                if args['duration'] < 1:
                    abort(400, message="Duration can't be negative")
                else:
                    song.duration = args['duration']
            db.session.commit()
            return song, 200

    @marshal_with(resource_song_fields)
    def delete(self, song_id):
        song = Song.query.filter_by(id=song_id).first()
        if song:
            db.session.delete(song)
            db.session.commit()
            return song, 200
        else:
            abort(404, message="Song with that id doesn't exist!")


api.add_resource(AudioBookR, "/audiobook", endpoint="audiobooks")
api.add_resource(AudioBookR, "/audiobook/<int:audio_id>",
                 endpoint="audiobook")
api.add_resource(SongR, '/song', endpoint="songs")
api.add_resource(SongR, '/song/<int:song_id>', endpoint="song")
