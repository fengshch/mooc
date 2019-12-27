import datetime
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token)
from flask_restplus import marshal
from .. import db
from ..model.user import User
from app.main.model.user import UserDto

_user = UserDto.user


def register_new_user(data):
    user = User.query.filter(User.email == data['email'] | User.username == data['username']).first()
    if not user:
        new_user = User(
            username=data['username'],
            password=data['password'],
            name=data['name'],
            email=data['email'],
            avatar=data['avatar'],
            organization_id=data['organization_id'] or None,
            registered_on=datetime.datetime.utcnow()
        )
        save_changes(new_user)
        response_object = {
            'access_token': create_access_token(identity=new_user.username),
            'token_type': "bearer",
            'refresh_token': create_refresh_token(identity=marshal(new_user.username)),
        }
        return response_object, 200
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409


def add_new_user(data):
    user = User.query.filter((User.email == data['email']) | (User.username == data['username'])).first()
    if not user:
        new_user = User(
            username=data['username'],
            password=data['password'],
            name=data['name'],
            email=data['email'],
            mobile_phone=data['mobile_phone'],
            avatar=data['avatar'],
            organization_id=data['organization_id'] or None,
            registered_on=datetime.datetime.utcnow(),
            roles=data['roles']
        )
        save_changes(new_user)
        response_object = {
            'status': 'success',
            'message': '用户添加成功',
            'data':  marshal(new_user, _user)
        }
        return response_object, 200
    else:
        response_object = {
            'status': 'fail',
            'message': '用户名或邮箱已经存在, 请使用其它名称邮箱'
        }
        return response_object, 409


def get_all_users():
    return User.query.all()


def list_users_by_organization_id(organization_id, page_no, page_size):
    rtn = User.query.filter_by(organization_id=organization_id) \
        .paginate(page=page_no, per_page=page_size)
    return {
        'data': marshal(rtn.items, _user),
        'pageNo': rtn.page,
        'pageSize': page_size,
        'totalPage': rtn.pages,
        'totalCount': rtn.total
    }


def get_user_by_username(username):
    return User.query.filter_by(username=username).first()


def list_users_by_course_id(course_id, page_no, page_size):
    result = User.query.join(User.courses).filter_by(id=course_id).paginate(page=page_no, per_page=page_size)
    return {
        'data': marshal(result.items, _user),
        'pageNo': result.page,
        'pageSize': page_size,
        'totalPage': result.pages,
        'totalCount': result.total
    }


def save_changes(data):
    db.session.add(data)
    db.session.commit()
