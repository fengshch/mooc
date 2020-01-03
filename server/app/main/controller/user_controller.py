from flask import request
from flask_restplus import Resource, marshal
from flask_jwt_extended import jwt_required, get_jwt_claims, current_user
from webargs import fields
from webargs.flaskparser import use_args

from app.main.model.user import UserDto
from ..service.user_service import add_new_user, get_all_users, get_user_by_username, list_users_by_organization_id, \
    list_users_by_course_id, update_user, delete_user_by_id, get_user_by_id, reset_password, update_password

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
    def post(self):
        """Creates a new user """
        data = request.json
        return add_new_user(data=data)

    # @api.expect(_user, validate=True)
    @api.response(201, 'User successfully updated')
    @api.doc('update a user')
    def put(self):
        """Creates a new user """
        data = request.json
        return update_user(data=data)

    @api.route('/organization/<organization_id>')
    @api.param('organization_id', 'The organization identifier')
    class ListUsersByOrganizationId(Resource):
        @api.doc('list_of_users_by_organization_id')
        @use_args({'page_no': fields.Integer(required=False),
                   'page_size': fields.Integer(required=False),
                   'show_grand': fields.Boolean(required=True)})
        def get(self, args, organization_id):
            """List all categories"""
            page_no = args.get('page_no')
            page_size = args.get('page_size')
            show_grand = args.get('show_grand')
            return list_users_by_organization_id(organization_id, page_no, page_size, show_grand)

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

    @api.route('/<id>')
    @api.param('id', 'The User identifier')
    @api.response(404, 'User not found.')
    class User(Resource):
        @api.doc('get a user')
        def get(self, id):
            """get a user given its identifier"""
            user = get_user_by_id(id)
            if not user:
                api.abort(404)
            else:
                return user

        @api.doc('delete a user')
        def delete(self, id):
            """delete a user given its identifier"""
            return delete_user_by_id(id)


@api.route('/info')
class UserInfo(Resource):
    """
    User info Resource
    """

    @api.doc('user info')
    @jwt_required
    # @api.marshal_with(_user)
    def get(self):
        rtn = {
            'status': 'success',
            'data': marshal(current_user, _user)
        }
        return rtn, 200


@api.route('/reset_password')
class ResetPassword(Resource):
    """
    Reset Password
    """

    @api.doc('reset password')
    @jwt_required
    def put(self):
        data = request.json
        user_id = data.get('user_id')
        return reset_password(user_id)


@api.route('/update_password')
class UpdatePassword(Resource):
    """
    Update Password
    """

    @api.doc('update password')
    @jwt_required
    def put(self):
        data = request.json
        user_id = data.get('user_id')
        password = data.get('password')
        return update_password(user_id, password)
