from flask_restplus import Namespace, fields
from sqlalchemy.orm import backref

from .. import db


class Organization(db.Model):
    """ User Model for storing Organization related details """
    __tablename__ = "organization"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=False)
    fullname = db.Column(db.String(100), nullable=False, unique=True)
    idx = db.Column(db.Integer, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=True)
    # children: db.relationship('Organization', remote_side=[id], backref='parent', uselist=True)
    children = db.relationship("Organization",
                               backref=backref("parent", remote_side=[id])
                               )


class OrganizationDTO:
    api = Namespace('organization', description='Organization related operations')
    organization = api.model('organization', {
        'id': fields.Integer(description='Organization ID'),
        'name': fields.String(required=True, description='Organization name'),
        'fullname': fields.String(required=True, description='Organization full name'),
        'idx': fields.Integer(description='Organization sorted index'),
        'parent_id': fields.Integer(description='Parent Id')
    })
    organization['children'] = fields.List(fields.Nested(api.models['organization']), description='children')
