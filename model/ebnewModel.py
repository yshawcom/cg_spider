# -*- coding: utf-8 -*-


"""
必联网
"""

__author__ = 'shaw'

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.dialects.mysql import MEDIUMTEXT

from db.mysqlDb import Base


class EbnewModel(Base):
    # 表名
    __tablename__ = 'ebnew'
    # 表主键
    id = Column(Integer(), primary_key=True, autoincrement=True)
    # 原id
    ori_id = Column(Integer())
    # 公告标题
    details_title = Column(String())
    # 发布时间
    release_time = Column(DateTime())
    # 项目编号
    bidcode = Column(String())
    # 公告类型
    announcement_type = Column(String())
    # 招标方式
    tender_method = Column(String())
    # 截止时间
    deadline = Column(DateTime())
    # 招标机构
    orgname = Column(String())
    # 招标地区
    tender_area = Column(String())
    # 招标产品
    tender_products = Column(String())
    # 所属行业
    industry = Column(String())
    # 主体内容
    details_content = Column(MEDIUMTEXT())
    # 更新时间
    update_time = Column(DateTime())
