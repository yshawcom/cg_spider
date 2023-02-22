# -*- coding: utf-8 -*-


"""
招标公告
"""

__author__ = 'shaw'

from sqlalchemy import Column, String, Integer, DateTime, Text

from db.mysqlDb import Base


class XmggNotice(Base):
    # 表名
    __tablename__ = 'tgcw_zhaobiao_xmgg'

    # 表主键
    id = Column(Integer(), primary_key=True, autoincrement=True)

    # 原id
    ori_id = Column(Integer())

    # 公告标题
    notice_title = Column(String())

    # 发布时间
    publish_time = Column(DateTime())

    # 公告内容
    notice_content = Column(Text())

    # 更新时间
    update_time = Column(DateTime())
