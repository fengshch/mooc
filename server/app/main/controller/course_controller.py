from flask import request
from flask_jwt_extended import jwt_required
from flask_restplus import Resource
from webargs import fields
from webargs.flaskparser import use_args
# from ..util import manager_required

from ..model.course import CourseDTO
from ..service.course_service import add_new_course, get_all_courses, get_course_by_id, list_courses_by_user_id, \
    list_courses_by_category_id, update_course, delete_course_by_id, update_published

api = CourseDTO.api
_course = CourseDTO.course


@api.route('/')
class CoursesList(Resource):
    @api.doc('list_of_courses')
    @use_args({'page_no': fields.Integer(required=True), 'page_size': fields.Integer(required=True)})
    def get(self, args):
        """List all courses"""
        page_no = args['page_no']
        page_size = args['page_size']
        return get_all_courses(page_no, page_size)

    @api.expect(_course, validate=True)
    @api.response(201, 'Course successfully created')
    # @api.doc('create a new category')
    # @manager_required
    @jwt_required
    def post(self):
        """Creates a new user """
        data = request.json
        return add_new_course(data=data)

    @api.expect(_course, validate=True)
    @api.response(201, 'Update successfully created')
    # @api.doc('create a new category')
    # @manager_required
    @jwt_required
    def put(self):
        """Creates a new user """
        data = request.json
        return update_course(data=data)

    @api.route('/<id>')
    @api.param('id', 'The Course identity')
    @api.response(404, 'Course not found.')
    class Course(Resource):
        @api.doc('get a category')
        def get(self, id):
            """get a user given its identifier"""
            return get_course_by_id(id)

        @api.doc('delete a course')
        def delete(self, id):
            """delete a course given its identifier"""
            return delete_course_by_id(id)

    @api.route('/user/<user_id>')
    @api.param('user_id', 'The user identifier')
    class ListCoursesByUserId(Resource):
        @api.doc('List courses by user id')
        @use_args({'page_no': fields.Integer(required=False), 'page_size': fields.Integer(required=False)})
        def get(self, args, user_id):
            """List all categories"""
            page_no = args.get('page_no')
            page_size = args.get('page_size')
            return list_courses_by_user_id(user_id, page_no, page_size)

    @api.route('/category/<category_id>')
    @api.param('category_id', 'The category identifier')
    class ListCoursesByCategoryId(Resource):
        @api.doc('List courses by category id')
        @use_args({'page_no': fields.Integer(required=False), 'page_size': fields.Integer(required=False)})
        def get(self, args, category_id):
            """List all categories"""
            page_no = args.get('page_no')
            page_size = args.get('page_size')
            return list_courses_by_category_id(category_id, page_no, page_size)

    @api.route('/publish')
    class UpdateCoursePublished(Resource):
        @api.doc('Update course published')
        def put(self):
            data = request.json
            course_id = data.get('course_id')
            published = data.get('published')
            return update_published(course_id, published)
