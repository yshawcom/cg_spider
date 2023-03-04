# -*- coding: utf-8 -*-


"""
建投商务网
"""

__author__ = 'shaw'

from db.mysqlDb import DBSession
from model.jtswwModel import JtswwModel


def find_top_by_guid_and_type_code(guid, type_code):
    """
    根据公告原id和公告类型查询
    """

    session = DBSession()
    # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
    notice = session.query(JtswwModel) \
        .filter(JtswwModel.guid == guid) \
        .filter(JtswwModel.type_code == type_code) \
        .one_or_none()
    session.close()
    return notice


def save(notice):
    """
    保存
    :param notice:
    :return:
    """
    session = DBSession()
    session.add(notice)
    session.commit()
    session.close()
    return notice
