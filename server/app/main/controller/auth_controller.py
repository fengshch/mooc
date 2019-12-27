from flask import request
from flask_restplus import Resource
from flask_jwt_extended import jwt_required

from ..service.auth_service import Auth
from app.main.model.auth import AuthDto
from app.main.model.user import UserDto

api = AuthDto.api
user_auth = AuthDto.user_auth


@api.route('/login')
class UserLogin(Resource):
    """
        User Login Resource
    """
    @api.doc('user login')
    @api.expect(user_auth, validate=True)
    def post(self):
        # get the post data
        post_data = request.json
        return Auth.login_user(data=post_data)


_user = UserDto.user


@api.route('/logout')
class LogoutAPI(Resource):
    """
    Logout Resource
    """
    @api.doc('logout a user')
    @jwt_required
    def delete(self):
        return Auth.logout_user()
