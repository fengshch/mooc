from flask_restplus import Namespace, fields

from .. import db


class Course(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "course"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(500), nullable=False)
    intro = db.Column(db.Text)
    content = db.Column(db.Text)
    cover = db.Column(db.String(500))
    category_id = db.Column(db.Integer, nullable=False)
    published = db.Column(db.Boolean, nullable=False, default=False)
    idx = db.Column(db.Integer, nullable=False, autoincrement=True)
    # users = db.relationship('User', secondary=course_user, lazy='dynamic',
    users = db.relationship('User', secondary='learning', lazy='dynamic',
                            backref=db.backref('courses_backref', lazy=True)
                            )


class CourseDTO:
    api = Namespace('course', description='Course related operations')
    course = api.model('course', {
        'id': fields.Integer(description='Course ID'),
        'title': fields.String(required=True, description='Course title'),
        'intro': fields.String(description='Course introduction'),
        'content': fields.String(description='Course content'),
        'cover': fields.String(description='Course cover image url'),
        'category_id': fields.Integer(required=True, description='Course\'s category id'),
        'category_name': fields.String(rquired=False, description='Course\'s category name'),
        'published': fields.Boolean(required=True, description='Course is published or not'),
        'idx': fields.Integer(description='Category sorted index')
    })


