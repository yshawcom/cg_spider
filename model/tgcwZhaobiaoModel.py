# -*- coding: utf-8 -*-


"""
天工e招（天工开物电子招投标交易平台）
"""

__author__ = 'shaw'

from sqlalchemy import Column, String, Integer, DateTime, Text

from db.mysqlDb import Base


class TgcwZhaobiaoModel(Base):
    # 表名
    __tablename__ = 'tgcw_zhaobiao'
    # 表主键
    id = Column(Integer(), primary_key=True, autoincrement=True)
    # 原id
    ori_id = Column(Integer())
    # 公告类型编码，xmgg/bidzbgs/bidzbgg
    type_code = Column(String())
    # 公告类型，招标公告/中标候选人公示/中标结果公告
    type_name = Column(String())
    # 公告标题
    notice_title = Column(String())
    # 发布时间
    publish_time = Column(DateTime())
    # 公告内容
    notice_content = Column(Text())
    # 更新时间
    update_time = Column(DateTime())
