# -*- coding: utf-8 -*-


__author__ = 'shaw'

BASE_URL = 'http://zhaobiao.tgcw.net.cn'

# 列表页URL
LIST_URL = BASE_URL + '/cms/channel/xmgg/index.htm?pageNo='

# 请求重试次数
REQUEST_RETRY_TIME = 3
# 请求重试间隔
REQUEST_RETRY_INTERVAL = 3
# 请求超时（s）
REQUEST_TIMEOUT = 10

# 是否需要IP代理
NEED_PROXY = True
# 代理IP池url
PROXY_POOL_URL = 'http://127.0.0.1:5010/get/'

# 每次执行爬取过去几天的数据
INTERVAL_DAYS = 20

# MySQL数据库连接
MYSQL_HOSTNAME = 'localhost'
MYSQL_PORT = 3306
MYSQL_USERNAME = 'root'
MYSQL_PASSWORD = '123456'
MYSQL_SCHEMA = 'cg_spider'

# 日志级别
LOG_LEVEL = 'DEBUG'
# 日志文件保留数量
LOG_BACKUP_COUNT = 3
