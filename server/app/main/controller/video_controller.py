from flask import request
from flask_jwt_extended import jwt_required
from flask_restplus import Resource
from webargs import fields
from webargs.flaskparser import use_args
# from ..util import manager_required

from ..model.video import VideoDTO
from ..service.video_service import add_new_video, get_video_by_id, get_videos_by_chapter_id, update_video, \
    delete_video_by_id

api = VideoDTO.api
_video = VideoDTO.video


@api.route('/')
class VideoList(Resource):
    @api.expect(_video, validate=True)
    @api.response(201, 'Video successfully created')
    @api.doc('create a new video')
    # @manager_required
    @jwt_required
    def post(self):
        """Creates a new video """
        data = request.json
        return add_new_video(data=data)

    @api.expect(_video, validate=True)
    @api.response(201, 'Video successfully updated')
    @api.doc('updates a new video')
    # @manager_required
    @jwt_required
    def put(self):
        """Updates a new video """
        data = request.json
        return update_video(data=data)

    @api.route('/<id>')
    @api.param('id', 'The Video identity')
    @api.response(404, 'Video not found.')
    class Video(Resource):
        @api.doc('get a video')
        def get(self, id):
            """get a video given its identifier"""
            return get_video_by_id(id)

        @api.doc('delete a video')
        @jwt_required
        def delete(self, id):
            """get a video given its identifier"""
            return delete_video_by_id(id)

    @api.route('/chapter/<chapter_id>')
    @api.param('chapter_id', 'The Chapter identity')
    class ListVideosByChapterID(Resource):
        @api.doc('list_of_videos_by_chapter_id')
        @use_args({'page_no': fields.Integer(required=False), 'page_size': fields.Integer(required=False)})
        def get(self, args, chapter_id):
            """List videos with chapter ID"""
            page_no = args.get('page_no')
            page_size = args.get('page_size')
            return get_videos_by_chapter_id(chapter_id, page_no, page_size)
