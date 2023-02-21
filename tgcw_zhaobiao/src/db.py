# -*- coding: utf-8 -*-


__author__ = 'shaw'

# 导入:
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from setting import MYSQL_HOSTNAME, MYSQL_PORT, MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_SCHEMA

# 创建对象的基类
Base = declarative_base()

# 初始化数据库连接
engine = create_engine('mysql+mysqlconnector://%s:%s@%s:%s/%s' %
                       (MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_HOSTNAME, str(MYSQL_PORT), MYSQL_SCHEMA))
# 创建DBSession类型
DBSession = sessionmaker(bind=engine)
