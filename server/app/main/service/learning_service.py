from flask_restplus import marshal
from sqlalchemy import func

from .organization_service import get_children_by_id
from .. import db
from ..model.organization import Organization
from ..model.user import User
from ..model.catetgory import Category
from ..model.course import Course
from ..model.learning import Learning, LearningDTO

_learning = LearningDTO.learning


def add_new_learning(data):
    max_idx, = db.session.query(func.max(Learning.idx)).first()
    if not max_idx:
        max_idx = 0

    new_learning = Learning(
        user_id=data['user_id'],
        course_id=data['course_id'],
        idx=max_idx + 1
    )
    save_changes(new_learning)
    rtn_learning = marshal(new_learning, _learning)
    response_object = {
        'status': 'success',
        'message': '视频添加成功',
        'data': rtn_learning
    }
    return response_object, 200


def add_learning_by_course_id(course_id, userIds):
    max_idx, = db.session.query(func.max(Learning.idx)).first()
    if not max_idx:
        max_idx = 0
    learnings = []
    for user_id in userIds:
        new_learning = Learning(
            user_id=user_id,
            course_id=course_id,
            idx=++max_idx
        )
        learnings.append(new_learning)
    db.session.bulk_save_objects(learnings)
    db.session.commit()
    return dict(status='success', message='添加选课成功')


def delete_learning_by_course_id(course_id, userIds):
    learnings = db.session.query(Learning).filter(Learning.course_id == course_id, Learning.user_id.in_(userIds)).all()
    for i in range(len(learnings)):
        db.session.delete(learnings[i])

    db.session.commit()
    return {
        'status': 'success',
        'message': '删除选课成功'
    }


def add_learning_by_user_id(user_id, course_id):
    max_idx, = db.session.query(func.max(Learning.idx)).first()
    if not max_idx:
        max_idx = 0
    new_learning = Learning(
        user_id=user_id,
        course_id=course_id,
        idx=++max_idx
    )
    save_changes(new_learning)
    return {
        'status': 'success',
        'data': marshal(new_learning, _learning),
        'message': '选课成功'
    }


def get_learning_by_user_id_and_course_id(user_id, course_id):
    learning = db.session.query(Learning)\
        .filter(Learning.user_id == user_id, Learning.course_id == course_id).first()
    if learning:
        rtn = {
            'status': 'success',
            'data': marshal(learning, _learning)
        }
    else:
        rtn = {
            'status': 'failure',
            'data': None
        }
    return rtn, 201


def delete_learning_by_id(learning_id):
    learning = Learning.query.get(learning_id)
    db.session.delete(learning)
    db.session.commit()
    rtn = {
        'status': 'success',
        'message': '删除选课成功'
    }
    return rtn, 201


def get_learning_by_id(learning_id):
    return Learning.query.get(learning_id)


def list_learning_by_course_id_and_organization_id(course_id, organization_id, show_grand):
    if int(organization_id) == 0:
        organization = Organization.query.filter_by(parent_id=None).first()
        organization_id = organization.id
    children = get_children_by_id(organization_id)
    children_ids = list(map(lambda child: child.id, children))
    if show_grand:
        rtn = db.session.query(Learning,
                               User.name.label('user_name'),
                               Course.title.label('course_title'),
                               Category.name.label('category_name')) \
            .join(User, User.id == Learning.user_id) \
            .join(Course, Course.id == Learning.course_id) \
            .join(Category, Category.id == Course.category_id) \
            .filter(User.organization_id.in_(children_ids), Learning.course_id == course_id).all()
    else:
        rtn = db.session.query(Learning,
                               User.name.label('user_name'),
                               Course.title.label('course_title'),
                               Category.name.label('category_name')) \
            .join(User, User.id == Learning.user_id) \
            .join(Course, Course.id == Learning.course_id) \
            .join(Category, Category.id == Course.category_id) \
            .filter(User.organization_id == organization_id, Learning.course_id == course_id).all()
    if len(rtn) == 0:
        return {
            'data': []
        }
    learnings, user_names, course_titles, category_names = zip(*rtn)
    print(learnings, user_names)
    length = len(learnings)
    for i in range(length):
        learnings[i].user_name = user_names[i]
        learnings[i].course_title = course_titles[i]
        learnings[i].category_name = category_names[i]
    data = marshal(learnings, _learning)
    print(data)
    return {
        'data': data
    }


def list_learning_by_organization_id(organization_id, page_no, page_size, show_grand):
    if int(organization_id) == 0:
        organization = Organization.query.filter_by(parent_id=None).first()
        organization_id = organization.id
    children = get_children_by_id(organization_id)
    children_ids = list(map(lambda child: child.id, children))
    if show_grand:
        rtn = db.session.query(Learning,
                               User.name.label('user_name'),
                               Course.title.label('course_title'),
                               Category.name.label('category_name')) \
            .join(User, User.id == Learning.user_id) \
            .join(Course, Course.id == Learning.course_id) \
            .join(Category, Category.id == Course.category_id) \
            .filter(User.organization_id.in_(children_ids)) \
            .paginate(page=page_no, per_page=page_size)
    else:
        rtn = db.session.query(Learning,
                               User.name.label('user_name'),
                               Course.title.label('course_title'),
                               Category.name.label('category_name')) \
            .join(User, User.id == Learning.user_id) \
            .join(Course, Course.id == Learning.course_id) \
            .join(Category, Category.id == Course.category_id) \
            .filter(User.organization_id == organization_id) \
            .paginate(page=page_no, per_page=page_size)
    if len(rtn.items) == 0:
        return {
            'data': [],
            'pageNo': 0,
            'pageSize': 0,
            'totalPage': 0,
            'totalCount': 0
        }
    learnings, user_names, course_titles, category_names = zip(*rtn.items)
    length = len(learnings)
    for i in range(length):
        learnings[i].user_name = user_names[i]
        learnings[i].course_title = course_titles[i]
        learnings[i].category_name = category_names[i]
    data = marshal(learnings, _learning)
    return {
        'data': data,
        'pageNo': rtn.page,
        'pageSize': rtn.per_page,
        'totalPage': rtn.pages,
        'totalCount': rtn.total
    }


def list_learning_by_user_id(user_id, page_no, page_size):
    rtn = db.session.query(Learning,
                               Course.title.label('course_title'),
                               Category.name.label('category_name')) \
            .join(Course, Course.id == Learning.course_id) \
            .join(Category, Category.id == Course.category_id) \
            .filter(Learning.user_id == user_id) \
            .paginate(page=page_no, per_page=page_size)
    if len(rtn.items) == 0:
        return {
            'data': [],
            'pageNo': 0,
            'pageSize': 0,
            'totalPage': 0,
            'totalCount': 0
        }
    learnings, course_titles, category_names = zip(*rtn.items)
    length = len(learnings)
    for i in range(length):
        learnings[i].course_title = course_titles[i]
        learnings[i].category_name = category_names[i]
    data = marshal(learnings, _learning)
    return {
        'data': data,
        'pageNo': rtn.page,
        'pageSize': rtn.per_page,
        'totalPage': rtn.pages,
        'totalCount': rtn.total
    }


def save_changes(data):
    db.session.add(data)
    db.session.commit()
