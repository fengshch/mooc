from flask import request
from flask_restplus import Resource, marshal
from flask_jwt_extended import jwt_required, get_jwt_claims, current_user
from webargs import fields
from webargs.flaskparser import use_args

from app.main.model.user import UserDto
from ..service.user_service import add_new_user, get_all_users, get_user_by_username, list_users_by_organization_id, \
    list_users_by_course_id

api = UserDto.api
_user = UserDto.user


@api.route('/')
class UserList(Resource):
    @api.doc('list_of_registered_users')
    @jwt_required
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        """List all registered users"""
        return get_all_users()

    @api.expect(_user, validate=True)
    @api.response(201, 'User successfully created')
    @api.doc('create a new user')
    def post(self):
        """Creates a new user """
        print(request.json)
        data = request.json
        return add_new_user(data=data)

    @api.route('/organization/<organization_id>')
    @api.param('organization_id', 'The organization identifier')
    class ListUsersByOrganizationId(Resource):
        @api.doc('list_of_users_by_organization_id')
        @use_args({'page_no': fields.Integer(required=False), 'page_size': fields.Integer(required=False)})
        def get(self, args, organization_id):
            """List all categories"""
            page_no = args.get('page_no')
            page_size = args.get('page_size')
            return list_users_by_organization_id(organization_id, page_no, page_size)

    @api.route('/course/<course_id>')
    @api.param('course_id', 'The course identifier')
    class ListUsersByCourseId(Resource):
        @api.doc('list_of_users_by_use_id')
        @use_args({'page_no': fields.Integer(required=False), 'page_size': fields.Integer(required=False)})
        def get(self, args, course_id):
            """List all categories"""
            page_no = args.get('page_no')
            page_size = args.get('page_size')
            return list_users_by_course_id(course_id, page_no, page_size)

        def put(self):
            pass

    @api.route('/<username>')
    @api.param('username', 'The User identifier')
    @api.response(404, 'User not found.')
    class User(Resource):
        @api.doc('get a user')
        @api.marshal_list_with(_user)
        def get(self, username):
            """get a user given its identifier"""
            user = get_user_by_username(username)
            if not user:
                api.abort(404)
            else:
                return user


@api.route('/info')
class UserInfo(Resource):
    """
    User info Resource
    """
    @api.doc('user info')
    @jwt_required
    # @api.marshal_with(_user)
    def get(self):
        print(request.json)
        print(get_jwt_claims()['roles'])
        rtn = {
            'status': 'success',
            'data':  marshal(current_user, _user)
        }
        print(rtn)
        return rtn, 200
