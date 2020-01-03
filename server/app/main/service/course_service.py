from flask_restplus import marshal
from sqlalchemy import func
from .. import db
from ..model.catetgory import Category
from ..model.course import Course, CourseDTO
from ..model.learning import Learning

_course = CourseDTO.course


def add_new_course(data):
    max_idx, = db.session.query(func.max(Course.idx)).first()
    if not max_idx:
        max_idx = 0

    new_course = Course(
        title=data['title'],
        intro=data['intro'],
        content=data['content'],
        cover=data['cover'],
        category_id=data['category_id'],
        published=data['published'],
        idx=max_idx + 1
    )
    save_changes(new_course)
    category_name, = db.session.query(Category.name) \
        .filter(Category.id == new_course.category_id)\
        .first()
    rtn_course = marshal(new_course, _course)
    rtn_course['category_name'] = category_name
    response_object = {
        'status': 'success',
        'message': '课程添加成功',
        'data': rtn_course
    }
    return response_object, 200


def get_all_courses(page_no, page_size):
    rtn = db.session.query(Course, Category.name.label('category_name'))\
        .join(Category, Course.category_id == Category.id)\
        .order_by(Course.idx).paginate(page=page_no, per_page=page_size)
    courses, category_names = zip(*rtn.items)
    length = len(courses)
    for i in range(length):
        courses[i].category_name = category_names[i]
    data = marshal(courses, _course)
    return {
        'data': data,
        'pageNo': rtn.page,
        'pageSize': page_size,
        'totalPage': rtn.pages,
        'totalCount': rtn.total
    }


def get_course_by_id(course_id):
    course = Course.query.get(course_id)
    rtn = {
        'status': 'success',
        'data': marshal(course, _course)
    }
    return rtn, 200


def list_courses_by_user_id(user_id, page_no, page_size):
    # result = Course.query.join(Course.users).filter_by(id=user_id).paginate(page=page_no, per_page=page_size)
    result = Course.query.join(Learning).filter_by(user_id=user_id).paginate(page=page_no, per_page=page_size)
    return {
        'data': marshal(result.items, _course),
        'pageNo': result.page,
        'pageSize': page_size,
        'totalPage': result.pages,
        'totalCount': result.total
    }


def list_courses_by_category_id(category_id, page_no, page_size):
    # result = Course.query.join(Course.users).filter_by(id=user_id).paginate(page=page_no, per_page=page_size)
    result = Course.query.filter_by(category_id=category_id).paginate(page=page_no, per_page=page_size)
    return {
        'data': marshal(result.items, _course),
        'pageNo': result.page,
        'pageSize': page_size,
        'totalPage': result.pages,
        'totalCount': result.total
    }


def update_course(data):
    course = Course.query.get(data['id'])
    course.title = data['title']
    course.intro = data['intro']
    course.content = data['content']
    course.cover = data['cover']
    course.category_id = data['category_id']
    course.published = data['published']
    course.idx = data['idx']
    db.session.commit()
    rtn = {
        'status': 'success',
        'message': '更改成功',
        'data': marshal(course, _course)
    }
    return rtn, 201


def delete_course_by_id(course_id):
    course = Course.query.get(course_id)
    db.session.delete(course)
    db.session.commit()
    rtn = {
        'status': 'success',
        'message': '删除成功'
    }
    return rtn


def update_published(course_id, published):
    course = Course.query.get(course_id)
    course.published = published
    db.session.commit()
    if course.published:
        message = '课程发布成功'
    else:
        message = '课程取消发布成功'
    rtn = {
        'status': 'success',
        'message': message,
        'data': course.published
    }
    return rtn


def save_changes(data):
    db.session.add(data)
    db.session.commit()
