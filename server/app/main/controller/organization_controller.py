from flask import request
from flask_jwt_extended import jwt_required
from flask_restplus import Resource
from webargs import fields
from webargs.flaskparser import use_args

from ..model.organization import OrganizationDTO
from ..service.organization_service \
    import add_new_organization, get_all_organization, get_organization_by_id, update_organization, \
    delete_organization_by_id

api = OrganizationDTO.api
_organization = OrganizationDTO.organization


@api.route('/')
class OrganizationList(Resource):
    @api.doc('list_of_organization')
    @use_args({'page_no': fields.Integer(required=False), 'page_size': fields.Integer(required=False)})
    def get(self, args):
        """List all categories"""
        page_no = args.get('page_no')
        page_size = args.get('page_size')
        return get_all_organization(page_no, page_size)

    @api.expect(_organization, validate=True)
    @api.response(201, 'Category successfully created')
    # @api.doc('create a new category')
    # @manager_required
    @jwt_required
    def post(self):
        """Creates a new user """
        data = request.json
        return add_new_organization(data=data)

    @api.expect(_organization, validate=True)
    @api.response(201, 'Category successfully updated')
    # @api.doc('create a new category')
    # @manager_required
    @jwt_required
    def put(self):
        """update organization"""
        data = request.json
        return update_organization(data=data)

    @api.route('/<id>')
    @api.param('id', 'The Organization identity')
    @api.response(404, 'Organization not found.')
    class Organization(Resource):
        @api.doc('get a category')
        # @api.marshal_list_with(_organization)
        def get(self, id):
            """get a user given its identifier"""

            # _organization['children'] = fields.List(r_fields.Nested(OrganizationDTO.organization),
            # description='children')
            return get_organization_by_id(id)

        @api.doc('delete a organization')
        def delete(self, id):
            """delete organization by id"""
            return delete_organization_by_id(id)

