from .blacklist_service import add_token_to_database, revoke_token

from app.main.model.user import User
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    current_user,
    get_raw_jwt)

from app.main.model.user import UserDto
_user = UserDto.user


class Auth:

    @staticmethod
    def login_user(data):
        try:
            username = data.get('username', None)
            email = data.get('email', None)

            if username:
                user = User.query\
                    .filter(User.username == username).first()
            else:
                user = User.query \
                    .filter(User.email == email).first()
            if user and user.check_password(data.get('password')):
                # revoke_token(user.username)
                # access_token = create_access_token(identity=marshal(user, _user))
                # refresh_token = create_refresh_token(identity=marshal(user, _user))
                access_token = create_access_token(identity=user.username)
                refresh_token = create_refresh_token(identity=user.username)

                add_token_to_database(access_token)
                add_token_to_database(refresh_token)
                response_object = {
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }
                return response_object, 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'username or password does not match.'
                }
                return response_object, 401
        except Exception as e:
            print(e)
            response_object = {
                'status': 'fail',
                'message': 'Try again'
            }
            return response_object, 500

    @staticmethod
    def logout_user():
        user_identity = get_raw_jwt()['identity']
        revoke_token(user_identity=user_identity)
        ret = {
            "status": "success",
            "message": 'Successfully logged out'
        }
        return ret, 200

    @staticmethod
    def get_logged_in_user():
        ret = {
            "status": "success",
            "data": current_user
        }
        return ret, 200
