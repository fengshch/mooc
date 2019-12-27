from flask_restplus import marshal
from sqlalchemy import func

from .. import db
from ..model.catetgory import Category, CategoryDTO

_category = CategoryDTO.category


def add_new_category(data):
    category = Category.query.filter_by(name=data['name']).first()
    if not category:
        max_idx, = db.session.query(func.max(Category.idx)).first()
        if not max_idx:
            max_idx = 0

        new_category = Category(
            name=data['name'],
            idx=max_idx + 1
        )
        save_changes(new_category)
        response_object = {
            'status': 'success',
            'message': '课程类别添加成功',
            'data':  marshal(new_category, _category)
        }
        return response_object, 200
    else:
        response_object = {
            'status': 'fail',
            'message': '课程类别已经存在, 请使用其它名称'
        }
        return response_object, 409


def get_all_categories(page_no, page_size):
    rtn = Category.query.order_by(Category.idx).paginate(page=page_no, per_page=page_size)
    return {
        'data': marshal(rtn.items, _category),
        'pageNo': rtn.page,
        'pageSize': rtn.per_page,
        'totalPage': rtn.pages,
        'totalCount': rtn.total
    }


def get_category_by_id(category_id):
    category = Category.query.get(category_id)
    rtn = {
        'status': 'success',
        'data': marshal(category, _category)
    }
    return rtn, 200


def update_category(data):
    category = Category.query.get(data['id'])
    category.name = data['name']
    category.idx = data['idx']
    db.session.commit()
    rtn = {
        'status': 'success',
        'message': '更改成功',
        'data': marshal(category, _category)
    }
    return rtn, 201


def delete_category_by_id(category_id):
    category = Category.query.get(category_id)
    db.session.delete(category)
    db.session.commit()
    rtn = {
        'status': 'success',
        'message': '删除成功'
    }
    return rtn, 201


def save_changes(data):
    db.session.add(data)
    db.session.commit()
