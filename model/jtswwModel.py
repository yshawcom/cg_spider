# -*- coding: utf-8 -*-


"""
建投商务网
"""

__author__ = 'shaw'

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.dialects.mysql import MEDIUMTEXT

from db.mysqlDb import Base


class JtswwModel(Base):
    # 表名
    __tablename__ = 'jtsww'
    # 表主键
    id = Column(Integer(), primary_key=True, autoincrement=True)
    # 原id
    guid = Column(String())
    # 公告类型编码，biddingnotice/candidateanno/winnotice
    type_code = Column(String())
    # 公告类型，招标公告/中标候选人公示/中标结果公告
    type_name = Column(String())
    # 公告标题
    name = Column(String())
    # 发布时间
    time = Column(DateTime())
    # 项目类型编码
    project_type = Column(String())
    # 类型
    type = Column(String())
    # 项目编号
    bid_section_code = Column(String())
    # 文件获取时间
    doc_get_start_time = Column(DateTime())
    # 项目经理
    tender_agency_lxr = Column(String())
    # 招标机构名称
    tender_agency_name = Column(String())
    # 招标人
    tenderer_name = Column(String())
    # 公告内容
    notice_content = Column(MEDIUMTEXT())
    # 更新时间
    update_time = Column(DateTime())
