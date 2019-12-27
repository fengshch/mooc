from flask import request
from flask_jwt_extended import jwt_required
from flask_restplus import Resource
from webargs import fields
from webargs.flaskparser import use_args
# from ..util import manager_required

from ..model.chapter import Chapter, ChapterDTO
from ..service.chapter_service import add_new_chapter, get_chapters_by_course_id, get_chapter_id, update_chapter, \
    delete_chapter_by_id

api = ChapterDTO.api
_chapter = ChapterDTO.chapter


@api.route('/')
class ChapterList(Resource):
    @api.expect(_chapter, validate=True)
    @api.response(201, 'Chapter successfully created')
    # @api.doc('create a new category')
    # @manager_required
    @jwt_required
    def post(self):
        """Creates a new user """
        data = request.json
        return add_new_chapter(data=data)

    @api.expect(_chapter, validate=True)
    @api.response(201, 'Update successfully created')
    # @api.doc('create a new category')
    # @manager_required
    @jwt_required
    def put(self):
        """Creates a new user """
        data = request.json
        return update_chapter(data=data)

    @api.route('/<id>')
    @api.param('id', 'The Chapter identity')
    @api.response(404, 'Chapter not found.')
    class Chapter(Resource):
        @api.doc('get a category')
        def get(self, id):
            """get a user given its identifier"""
            return get_chapter_id(id)

        @api.doc('delete a chapter')
        def delete(self, id):
            """delete a course given its identifier"""
            return delete_chapter_by_id(id)

    @api.route('/course/<course_id>')
    @api.param('course_id', 'The Course identity')
    class ListChapterByCourseID(Resource):
        @api.doc('list_of_chapters_by_course_id')
        @use_args({'page_no': fields.Integer(required=False), 'page_size': fields.Integer(required=False)})
        def get(self, args, course_id):
            """List all categories"""
            page_no = args.get('page_no')
            page_size = args.get('page_size')
            return get_chapters_by_course_id(course_id, page_no, page_size)