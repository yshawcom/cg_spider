# -*- coding: utf-8 -*-


"""
MySQL数据库连接
"""

__author__ = 'shaw'

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from handler.configHandler import ConfigHandler

conf = ConfigHandler()

# 创建对象的基类
Base = declarative_base()

# 初始化数据库连接
engine = create_engine('mysql+mysqlconnector://%s:%s@%s:%s/%s' %
                       (conf.mysql_username,
                        conf.mysql_password,
                        conf.mysql_hostname,
                        conf.mysql_port,
                        conf.mysql_schema))

# 创建DBSession类型
DBSession = sessionmaker(bind=engine)
