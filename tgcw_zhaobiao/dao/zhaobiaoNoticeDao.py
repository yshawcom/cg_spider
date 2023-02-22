# -*- coding: utf-8 -*-


__author__ = 'shaw'

from db.mysqlDb import DBSession
from model.zhaobiaoNotice import ZhaobiaoNotice


def find_top_by_ori_id_and_type_code(ori_id, type_code):
    """
    根据公告原id和公告类型查询
    :param ori_id:
    :param type_code:
    :return:
    """

    session = DBSession()
    # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
    notice = session.query(ZhaobiaoNotice) \
        .filter(ZhaobiaoNotice.ori_id == ori_id) \
        .filter(ZhaobiaoNotice.type_code == type_code) \
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
