from flask_restplus import Namespace, fields

from .. import db


class Video(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "video"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(500), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    thumbnail = db.Column(db.String(500))
    url = db.Column(db.String(500))
    idx = db.Column(db.Integer, nullable=False, autoincrement=True)


class VideoDTO:
    api = Namespace('video', description='Video related operations')
    video = api.model('video', {
        'id': fields.Integer(description='Video ID'),
        'title': fields.String(required=True, description='Video title'),
        'chapter_id': fields.Integer(required=True, description='Video\'s chapter id'),
        'thumbnail': fields.String(description='Video cover image url'),
        'url': fields.String(description='Video url'),
        'idx': fields.Integer(description='Video sorted index')
    })
