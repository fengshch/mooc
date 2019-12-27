from flask_restplus import marshal
from sqlalchemy import func
from .. import db
from ..model.video import Video, VideoDTO

_video = VideoDTO.video


def add_new_video(data):
    max_idx, = db.session.query(func.max(Video.idx)).first()
    if not max_idx:
        max_idx = 0

    new_video = Video(
        title=data['title'],
        chapter_id=data['chapter_id'],
        thumbnail=data['thumbnail'],
        url=data['url'],
        idx=max_idx + 1
    )
    save_changes(new_video)
    rtn_video = marshal(new_video, _video)
    response_object = {
        'status': 'success',
        'message': '视频添加成功',
        'data': rtn_video
    }
    return response_object, 200


def get_videos_by_chapter_id(chapter_id, page_no, page_size):
    rtn = db.session.query(Video)\
        .filter_by(chapter_id=chapter_id)\
        .order_by(Video.idx).paginate(page=page_no, per_page=page_size)
    videos = rtn.items
    return {
        'data': marshal(videos, _video),
        'pageNo': rtn.page,
        'pageSize': page_size,
        'totalPage': rtn.pages,
        'totalCount': rtn.total
    }


def get_video_by_id(video_id):
    video = Video.query.get(video_id)
    rtn = {
        'status': 'success',
        'data': marshal(video, _video)
    }
    return rtn, 200


def update_video(data):
    video = Video.query.get(data['id'])
    video.title = data['title']
    video.thumbnail = data['thumbnail']
    video.url = data['url']
    video.idx = data['idx']
    db.session.commit()
    rtn = {
        'status': 'success',
        'message': '更改成功',
        'data': marshal(video, _video)
    }
    return rtn, 201


def delete_video_by_id(video_id):
    video = Video.query.get(video_id)
    db.session.delete(video)
    db.session.commit()
    rtn = {
        'status': 'success',
        'message': '删除成功'
    }
    return rtn, 201


def save_changes(data):
    db.session.add(data)
    db.session.commit()
