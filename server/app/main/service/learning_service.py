from flask_restplus import marshal
from sqlalchemy import func
from .. import db
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


def get_learning_by_id(learning_id):
    return Learning.query.get(learning_id)


def save_changes(data):
    db.session.add(data)
    db.session.commit()
