import datetime
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token)
from flask_restplus import marshal

from .organization_service import get_children_by_id
from .. import db
from ..model.organization import Organization
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
            email=data.get('email') or None,
            mobile_phone=data.get('mobile_phone') or None,
            avatar=data.get('avatar') or None,
            organization_id=data['organization_id'] or None,
            registered_on=datetime.datetime.utcnow(),
            roles=data.get('roles') or ['users']

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
    if data.get('email'):
        user = User.query.filter((User.email == data.get('email')) | (User.username == data['username'])).first()
    else:
        user = User.query.filter(User.username == data['username']).first()
    if not user:
        new_user = User(
            username=data['username'],
            password=data.get('password') or '123456',
            name=data['name'],
            email=data.get('email') or None,
            mobile_phone=data.get('mobile_phone') or None,
            avatar=data.get('avatar') or None,
            organization_id=data['organization_id'] or None,
            registered_on=datetime.datetime.utcnow(),
            roles=data.get('roles') or ['users']
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


def list_users_by_organization_id(organization_id, page_no, page_size, show_grand):
    if int(organization_id) == 0:
        organization = Organization.query.filter_by(parent_id=None).first()
        organization_id = organization.id

    children = get_children_by_id(organization_id)
    children_ids = list(map(lambda child: child.id, children))
    if show_grand:
        rtn = User.query.filter(User.organization_id.in_(children_ids)).paginate(page=page_no, per_page=page_size)
    else:
        rtn = User.query.filter_by(organization_id=organization_id) \
            .paginate(page=page_no, per_page=page_size)
        print(rtn)
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


def update_user(data):
    user = User.query.get(data['id'])
    user.username = data['username'],
    user.name = data['name'],
    user.email = data.get('email') or None,
    user.mobile_phone = data.get('mobile_phone') or None,
    user.avatar = data.get('avatar') or None,
    user.organization_id = data['organization_id'] or None,
    user.registered_on = datetime.datetime.utcnow(),
    user.roles = data['roles']
    db.session.commit()
    rtn = {
        'status': 'success',
        'message': '更改成功',
        'data': marshal(user, _user)
    }
    return rtn, 201


def delete_user_by_id(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    rtn = {
        'status': 'success',
        'message': '删除用户成功'
    }
    return rtn


def get_user_by_id(user_id):
    user = User.query.get(user_id)
    rtn = {
        'status': 'success',
        'data':  marshal(user, _user)
    }
    return rtn, 200


def reset_password(user_id):
    user = User.query.get(user_id)
    user.password = '123456'
    db.session.commit()
    return {
        'status': 'success',
        'message': '密码重置成功'
    }


def update_password(user_id, password):
    user = User.query.get(user_id)
    user.password = password
    db.session.commit()
    return {
        'status': 'success',
        'message': '密码修改成功'
    }

def save_changes(data):
    db.session.add(data)
    db.session.commit()
