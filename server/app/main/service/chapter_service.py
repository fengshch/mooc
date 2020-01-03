from flask_restplus import marshal
from sqlalchemy import func

from .. import db
from ..model.chapter import Chapter, ChapterDTO
from ..model.learning import Learning

_chapter = ChapterDTO.chapter


def add_new_chapter(data):
    max_idx, = db.session.query(func.max(Chapter.idx)).first()
    print(data)
    if not max_idx:
        max_idx = 0

    new_chapter = Chapter(
        title=data['title'],
        course_id=data['course_id'],
        idx=max_idx + 1
    )
    save_changes(new_chapter)
    response_object = {
        'status': 'success',
        'message': '课程章节添加成功',
        'data':  marshal(new_chapter, _chapter)
    }
    print(response_object)
    return response_object, 200


def get_chapters_by_course_id(course_id, page_no, page_size):
    rtn = Chapter.query.filter_by(course_id=course_id)\
        .order_by(Chapter.idx).paginate(page=page_no, per_page=page_size)
    print(rtn.items)
    return {
        'data': marshal(rtn.items, _chapter),
        'pageNo': rtn.page,
        'pageSize': page_size,
        'totalPage': rtn.pages,
        'totalCount': rtn.total
    }


def get_chapters_by_learning_id(learning_id):
    chapters = db.session.query(Chapter)\
        .filter(Learning.course_id == Chapter.course_id, Learning.id == learning_id).all()
    return {
        'data': marshal(chapters, _chapter)
    }


def get_chapter_id(chapter_id):
    chapter = Chapter.query.get(chapter_id)
    rtn = {
        'status': 'success',
        'data': marshal(chapter, _chapter)
    }

    return rtn


def update_chapter(data):
    chapter = Chapter.query.get(data['id'])
    chapter.title = data['title']
    chapter.idx = data['idx']
    db.session.commit()
    rtn = {
        'status': 'success',
        'message': '更改成功',
        'data': marshal(chapter, _chapter)
    }
    return rtn, 201


def delete_chapter_by_id(chapter_id):
    chapter = Chapter.query.get(chapter_id)
    db.session.delete(chapter)
    db.session.commit()
    rtn = {
        'status': 'success',
        'message': '删除成功'
    }
    return rtn, 201


def save_changes(data):
    db.session.add(data)
    db.session.commit()
