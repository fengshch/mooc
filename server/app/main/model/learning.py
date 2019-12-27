from flask_restplus import Namespace, fields

from app import db

# course_user = db.Table('course_user',
#                        db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
#                        db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
#                        )


class Learning(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "learning"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    idx = db.Column(db.Integer, nullable=False, autoincrement=True)


class LearningDTO:
    api = Namespace('chapter', description='Chapter related operations')
    learning = api.model('learning', {
        'id': fields.Integer(description='Chapter ID'),
        'user_id': fields.Integer(Require=True, description="Learning\'s user id"),
        'course_id': fields.Integer(Require=True, description="Learning\'s user id"),
        'idx': fields.Integer(description='Chapter sorted index')
    })
