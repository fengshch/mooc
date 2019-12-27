from flask_restplus import Namespace, fields


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'username': fields.String(required=False, description='The username'),
        'email': fields.String(required=False, description='The email'),
        'password': fields.String(required=True, description='the user password'),
    })
