from collections import defaultdict

from flask_restplus import marshal
from sqlalchemy import func
from sqlalchemy.orm.attributes import set_committed_value

from .. import db
from ..model.organization import Organization, OrganizationDTO

_organization = OrganizationDTO.organization


def add_new_organization(data):
    organization = Organization.query.filter_by(fullname=data['fullname']).first()
    if not organization:
        max_idx, = db.session.query(func.max(Organization.idx)).first()
        if not max_idx:
            max_idx = 0

        new_organization = Organization(
            name=data['name'],
            fullname=data['fullname'],
            parent_id=data.get('parent_id', None),
            idx=max_idx + 1
        )
        save_changes(new_organization)
        response_object = {
            'status': 'success',
            'message': '用户组添加成功',
            'data':  marshal(new_organization, _organization)
        }
        print(response_object)
        return response_object, 200
    else:
        response_object = {
            'status': 'fail',
            'message': '用户组已经存在, 请使用其它名称'
        }
        return response_object, 409


def get_all_organization(page_no, page_size):
    rtn = Organization.query.filter(Organization.parent_id.is_(None))\
        .order_by(Organization.idx).paginate(page=page_no, per_page=page_size)
    return {
        'data': marshal(rtn.items, _organization),
        'pageNo': rtn.page,
        'pageSize': page_size,
        'totalPage': rtn.pages,
        'totalCount': rtn.total
    }


def get_children_by_id(organization_id):
    organizations = Organization.query.all()
    children = defaultdict(list)
    for organization in organizations:
        if organization.parent_id:
            children[organization.parent_id].append(organization)
    organization = Organization.query.get(organization_id)
    rtn = list()
    rtn.append(organization)
    rtn.extend(get_grandchildren(organization, children))
    return rtn


def get_grandchildren(organization, children):
    grandchildren = list()
    grandchildren.extend(children[organization.id])
    for child in grandchildren:
        grandchildren.extend(get_grandchildren(child, children))
    return grandchildren


def get_organization_by_id(organization_id):
    organization = Organization.query.filter_by(id=organization_id).first()
    rtn = {
        'data': marshal(organization, _organization),
        'status': 'success'
    }
    return rtn


def update_organization(data):
    organization = Organization.query.get(data['id'])
    organization.name = data['name']
    organization.fullname = data['fullname']
    organization.parent_id = data['parent_id']
    organization.idx = data['idx']
    db.session.commit()
    rtn = {
        'status': 'success',
        'message': '用户组更改成功',
        'data': marshal(organization, _organization)

    }
    return rtn


def delete_organization_by_id(organization_id):
    organization = Organization.query.get(organization_id)
    db.session.delete(organization)
    db.session.commit()
    rtn = {
        'status': 'success',
        'message': '删除成功'
    }
    return rtn, 201


def save_changes(data):
    db.session.add(data)
    db.session.commit()
