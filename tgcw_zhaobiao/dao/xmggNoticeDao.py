# -*- coding: utf-8 -*-


__author__ = 'shaw'

from db.mysqlDb import DBSession
from model.xmggNotice import XmggNotice


def find_top_by_ori_id(ori_id):
    """
    根据公告原id查询
    :param ori_id:
    :return:
    """

    session = DBSession()
    # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
    notice = session.query(XmggNotice) \
        .filter(XmggNotice.ori_id == ori_id) \
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
