from flask_restplus import Api
from flask import Blueprint
from .main import jwt, db

from .main.controller.user_controller import api as user_api
from .main.controller.auth_controller import api as auth_api
from .main.controller.category_controller import api as category_api
from .main.controller.course_controller import api as course_api
from .main.controller.chapter_controller import api as chapter_api
from .main.controller.video_controller import api as video_api
from .main.controller.organization_controller import api as organization_api
from .main.controller.learning_controller import api as learning_api
from .main.controller.upload_controller import api as upload_api
from .main.model.user import User

from .main.service.blacklist_service import (
    is_token_revoked, add_token_to_database, get_user_tokens,
    revoke_token, unrevoke_token, prune_database
)

from .main.service.user_service import get_user_by_username

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='FLASK RESTPLUS API BOILER-PlATE WITH JWT',
          version='1.0',
          description='a boilerplate for flask restplus web servbice'
          )

api.add_namespace(user_api, path='/api/users')
api.add_namespace(auth_api, path='/api/auth')
api.add_namespace(category_api, path='/api/categories')
api.add_namespace(course_api, path='/api/courses')
api.add_namespace(chapter_api, path='/api/chapters')
api.add_namespace(video_api, path='/api/videos')
api.add_namespace(organization_api, path='/api/organizations')
api.add_namespace(learning_api, path='/api/learning')
api.add_namespace(upload_api, path='/api/upload')


@jwt.user_claims_loader
def add_claims_to_access_token(user_identity):
    roles = get_user_by_username(user_identity).roles
    return {'roles': roles}


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decoded_token):
    return is_token_revoked(decoded_token)


@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    user = get_user_by_username(identity)
    return user



