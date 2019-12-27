from flask_restplus import Namespace, fields

from .. import db


class Category(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    idx = db.Column(db.Integer, nullable=False)


class CategoryDTO:
    api = Namespace('category', description='Category related operations')
    category = api.model('category', {
        'id': fields.Integer(description='Category ID'),
        'name': fields.String(required=True, description='Category name'),
        'idx': fields.Integer(description='Category sorted index'),
    })
