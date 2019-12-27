from flask import request
from flask_jwt_extended import jwt_required
from flask_restplus import Resource
from webargs import fields
from webargs.flaskparser import use_args
# from ..util import manager_required

from ..model.learning import LearningDTO
from ..service.learning_service import add_new_learning

api = LearningDTO.api
_learning = LearningDTO.learning


@api.route('/')
class LearningList(Resource):
    @api.doc('list_of_learning')
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
        pass
        return add_new_learning(data=data)

    # @api.route('/<id>')
    # @api.param('id', 'The Category identity')
    # @api.response(404, 'Category not found.')
    # class Category(Resource):
    #     @api.doc('get a category')
    #     @api.marshal_list_with(_category)
    #     def get(self, id):
    #         """get a user given its identifier"""
    #         category = get_category_by_id(id)
    #         if not category:
    #             api.abort(404)
    #         else:
    #             return category

