from flask import request
from flask_jwt_extended import jwt_required
from flask_restplus import Resource
from webargs import fields
from webargs.flaskparser import use_args

from ..model.learning import LearningDTO
from ..service.learning_service import add_new_learning, list_learning_by_organization_id, get_learning_by_id, \
    delete_learning_by_id, add_learning_by_course_id, add_learning_by_user_id, \
    list_learning_by_course_id_and_organization_id, delete_learning_by_course_id, get_learning_by_user_id_and_course_id, \
    list_learning_by_user_id

api = LearningDTO.api
_learning = LearningDTO.learning


@api.route('/')
class LearningList(Resource):
    @api.doc('list of learning')
    @use_args({'page_no': fields.Integer(required=False), 'page_size': fields.Integer(required=False)})
    def get(self, args):
        pass

    @api.expect(_learning, validate=True)
    @api.response(201, 'Category successfully created')
    # @api.doc('create a new category')
    # @manager_required
    @jwt_required
    def post(self):
        """Creates a new user """
        data = request.json
        return add_new_learning(data=data)

    @api.route('/organization/<organization_id>')
    @api.param('organization_id', 'The organization identifier')
    class ListLearningByOrganizationId(Resource):
        @api.doc('List learning by organization id')
        @use_args({'page_no': fields.Integer(required=False),
                   'page_size': fields.Integer(required=False),
                   'show_grand': fields.Boolean(required=True)
                   })
        def get(self, args, organization_id):
            """List all categories"""
            page_no = args.get('page_no')
            page_size = args.get('page_size')
            show_grand = args.get('show_grand')
            return list_learning_by_organization_id(organization_id, page_no, page_size, show_grand)

    @api.route('/<id>')
    @api.param('id', 'The Learning identifier')
    @api.response(404, 'Learning not found.')
    class User(Resource):
        @api.doc('get a learning')
        def get(self, id):
            """get a user given its identifier"""
            learning = get_learning_by_id(id)
            if not learning:
                api.abort(404)
            else:
                return learning

        @api.doc('delete a learning')
        def delete(self, id):
            """delete a learning given its identifier"""
            return delete_learning_by_id(id)

    @api.route('/course/<course_id>')
    @api.param('course_id', 'The course identifier')
    class LearningListByCourseId(Resource):
        @api.doc('list of learning by course id')
        @jwt_required
        @use_args({
            'organization_id': fields.Integer(required=True),
            'show_grand': fields.Boolean(required=True)})
        def get(self, args, course_id):
            print(course_id)
            """List learning by course id"""
            organization_id = args.get('organization_id')
            show_grand = args.get('show_grand')
            return list_learning_by_course_id_and_organization_id(course_id, organization_id, show_grand)

        @api.response(201, 'add learning successfully')
        @api.doc('bulk learning by course id')
        def post(self, course_id):
            """add learning """
            data = request.json
            return add_learning_by_course_id(course_id, data)

        @api.response(201, 'Learning successfully deleted')
        @api.doc('bulk learning by course id')
        def delete(self, course_id):
            """delete learning by course id """
            data = request.json
            return delete_learning_by_course_id(course_id, data)


@api.route('/user/<user_id>/course/<course_id>')
@api.param('user_id', 'The user identifier')
@api.param('course_id', 'The course identifier')
class LearningByUserIdAndCourse(Resource):
    @api.doc('get learning by user id and course id')
    @jwt_required
    def get(self, user_id, course_id):
        """List learning by course id"""
        return get_learning_by_user_id_and_course_id(user_id, course_id)

    @api.response(201, 'Learning successfully created')
    @api.doc('bulk learning by user id')
    def post(self, user_id, course_id):
        """Creates new learning With user id and course id"""
        return add_learning_by_user_id(user_id, course_id)


@api.route('/user/<user_id>')
@api.param('user_id', 'The user identifier')
class LearningListByUserId(Resource):
    @api.doc('list of learning by user id')
    @jwt_required
    @use_args({
        'page_no': fields.Integer(required=True),
        'page_size': fields.Integer(required=True)})
    def get(self, args, user_id):
        """List learning by course id"""
        page_no = args.get('page_no')
        page_size = args.get('page_size')
        return list_learning_by_user_id(user_id, page_no, page_size)
