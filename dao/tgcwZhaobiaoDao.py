# -*- coding: utf-8 -*-


"""
天工e招（天工开物电子招投标交易平台）
"""

__author__ = 'shaw'

from db.mysqlDb import DBSession
from model.tgcwZhaobiaoModel import TgcwZhaobiaoModel


def find_top_by_ori_id_and_type_code(ori_id, type_code):
    """
    根据公告原id和公告类型查询
    :param ori_id:
    :param type_code:
    :return:
    """

    session = DBSession()
    # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
    notice = session.query(TgcwZhaobiaoModel) \
        .filter(TgcwZhaobiaoModel.ori_id == ori_id) \
        .filter(TgcwZhaobiaoModel.type_code == type_code) \
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
