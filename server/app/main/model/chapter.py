from flask_restplus import Namespace, fields

from .video import VideoDTO
from .. import db
_video = VideoDTO.video


class Chapter(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "chapter"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(500), nullable=False)
    course_id = db.Column(db.Integer, nullable=False)
    idx = db.Column(db.Integer, nullable=False)
    videos = db.relationship('Video', backref='chapter', lazy=True)


class ChapterDTO:
    api = Namespace('chapter', description='Chapter related operations')
    chapter = api.model('chapter', {
        'id': fields.Integer(description='Chapter ID'),
        'title': fields.String(require=True, description='Chapter  title'),
        'course_id': fields.Integer(require=True, description="Video\'s course id"),
        'idx': fields.Integer(description='Chapter sorted index'),
        'videos': fields.List(fields.Nested(_video), description='videos')
    })
