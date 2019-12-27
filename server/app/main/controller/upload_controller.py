import os
import pathlib
import uuid
import subprocess

from flask import request
from flask_restplus import Resource, Namespace
from werkzeug.utils import secure_filename

from app.main import app

api = Namespace('upload', description='Upload file')

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4'}
IMG_EXTENSIONS = {'png', 'jpg', 'jpeg'}
VIDEO_EXTENSIONS = {'mp4', 'mov', 'wmv', 'flv', 'mkv', 'ogg', 'webm'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.')[1].lower() in ALLOWED_EXTENSIONS


def allowed_img(filename):
    return '.' in filename and \
           filename.rsplit('.')[1].lower() in IMG_EXTENSIONS


def allowed_video(filename):
    return '.' in filename and \
           filename.rsplit('.')[1].lower() in VIDEO_EXTENSIONS


@api.route('/')
class Upload(Resource):
    @api.route('/course_cover')
    class UploadCourseCover(Resource):
        @api.doc('up load file')
        def post(self):
            if 'course_cover' not in request.files:
                return {
                           'message': 'No file part in the request'
                       }, 400
            file = request.files['course_cover']
            if file.filename == '':
                return {
                           'message': ' No file selected for uploading'
                       }, 400
            if file and allowed_img(file.filename):
                filename = secure_filename(file.filename)
                extension = filename.rsplit('.')[1].lower()
                uid = str(uuid.uuid4())
                new_filename = uid + '.' + extension
                pathlib.Path(app.config['UPLOAD_FOLDER'] + '/images/course_cover').mkdir(exist_ok=True)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'] + '/images/course_cover', new_filename))
                return {
                           'file': {
                               'uid': uid,
                               'name': new_filename,
                               'status': 'done',
                               'response': '{"status": "success"}',
                               'linkProps': '{"download": "image"}',
                               'url': '/images/course_cover/' + new_filename
                           },
                           'message': '文件上传成功'
                       }, 201

    @api.route('/ckfinder')
    class UploadCourseCover(Resource):
        @api.doc('up load file')
        def post(self):
            print(request.files)
            if 'upload' not in request.files:
                return {
                           'message': 'No file part in the request'
                       }, 400
            file = request.files['upload']
            if file.filename == '':
                return {
                           'message': ' No file selected for uploading'
                       }, 400
            if file and allowed_img(file.filename):
                filename = secure_filename(file.filename)
                # file.seek(0, os.SEEK_END)
                # size = file.tell() / 1024 / 1024
                extension = filename.rsplit('.')[1].lower()
                # extension = os.path.split(filename)[1]
                uid = str(uuid.uuid4())
                new_filename = uid + '.' + extension
                pathlib.Path(app.config['UPLOAD_FOLDER'] + '/images/ckfinder').mkdir(exist_ok=True)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'] + '/images/ckfinder', new_filename))
                return {
                           'uploaded': True,
                           "error": {
                               "message": "no error"
                           },
                           'url': '/images/ckfinder/' + new_filename
                       }, 201

    @api.route('/video')
    class UploadCourseCover(Resource):
        @api.doc('up load file')
        def post(self):
            print(request.files)
            if 'video' not in request.files:
                return {
                       'message': 'No file part in the request'
                   }, 400
            file = request.files['video']
            if file.filename == '':
                return {
                       'message': ' No file selected for uploading'
                   }, 400
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                extension = filename.rsplit('.')[1].lower()
                # extension = os.path.split(filename)[1]
                save_filename = str(uuid.uuid4())
                video_file = os.path.join(app.config['UPLOAD_FOLDER'] + '/videos', save_filename + '.' + extension)
                thumbnail_file = os.path.join(app.config['UPLOAD_FOLDER'] + '/images/thumbnails', save_filename + '.png')
                file.save(video_file)
                size = os.stat(video_file).st_size
                print(thumbnail_file)
                subprocess.call(['ffmpeg', '-i', video_file, '-ss', '00:01:03.000', '-vframes', '1', thumbnail_file])

                return {
                       'data': {
                           'filename': save_filename + '.' + extension,
                           'size': size,
                           'url': '/videos/' + save_filename + '.' + extension,
                           'thumbnail': '/images/thumbnails/' + save_filename + '.png'
                       },
                       'message': '文件上传成功'
                   }, 201
        # parse = reqparse.RequestParser()
        # parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        # args = parse.parse_args()
        # new_file = args['file']
        # new_file.save(uuid.uuid4() + extension)
