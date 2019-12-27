from flask import request
from flask_jwt_extended import jwt_required
from flask_restplus import Resource
from webargs import fields
from webargs.flaskparser import use_args
# from ..util import manager_required

from ..model.catetgory import CategoryDTO
from ..service.category_service import add_new_category, get_all_categories, get_category_by_id, update_category, \
    delete_category_by_id

api = CategoryDTO.api
_category = CategoryDTO.category


@api.route('/')
class CategoryList(Resource):
    @api.doc('list_of_categories')
    @use_args({'page_no': fields.Integer(required=False), 'page_size': fields.Integer(required=False)})
    def get(self, args):
        """List all categories"""
        page_no = args.get('page_no')
        page_size = args.get('page_size')
        return get_all_categories(page_no, page_size)

    @api.expect(_category, validate=True)
    @api.response(201, 'Category successfully created')
    # @api.doc('create a new category')
    # @manager_required
    @jwt_required
    def post(self):
        """Creates a new user """
        data = request.json
        return add_new_category(data=data)

    @api.expect(_category, validate=True)
    @api.response(201, 'Category successfully created')
    # @api.doc('create a new category')
    # @manager_required
    @jwt_required
    def put(self):
        """Creates a new user """
        data = request.json
        return update_category(data=data)

    @api.route('/<id>')
    @api.param('id', 'The Category identity')
    @api.response(404, 'Category not found.')
    class AddCategory(Resource):
        @api.doc('get a category')
        def get(self, id):
            """get a user given its identifier"""
            return get_category_by_id(id)

        @api.doc('delete a category')
        def delete(self, id):
            """get a user given its identifier"""
            return delete_category_by_id(id)

