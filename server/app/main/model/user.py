from flask_restplus import Namespace, fields

from .. import db, bcrypt


class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(100))
    name = db.Column(db.String(100), nullable=False)
    mobile_phone = db.Column(db.String(11), unique=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    avatar = db.Column(db.String(255))
    organization_id = db.Column(db.Integer, nullable=True)
    registered_on = db.Column(db.DateTime, nullable=False)
    last_login_ip = db.Column(db.String(15))
    last_login_time = db.Column(db.DateTime)
    roles = db.Column(db.ARRAY(db.String(50)))
    courses = db.relationship('Course', secondary='learning', lazy='dynamic',
                              backref=db.backref("users_backref", lazy=True)
                              )

    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'id': fields.Integer(description='User ID'),
        'username': fields.String(required=True, description='user username'),
        'email': fields.String(required=True, description='user email address'),
        'password': fields.String(required=True, description='user password'),
        'name': fields.String(required=True, description='user name'),
        'mobile_phone': fields.String(description='User mobile phone'),
        'avatar': fields.String(descript='User avatar'),
        'organization_id': fields.Integer(description="Organization Id"),
        'registered_on': fields.DateTime(description='User registered time'),
        'last_login_ip': fields.String(description='User last login ip address'),
        'last_login_time': fields.DateTime(description='User last login time'),
        'roles': fields.List(fields.String)
    })
