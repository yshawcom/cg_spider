# -*- coding: utf-8 -*-


__author__ = 'shaw'

# 日志格式化
LOG_FORMATTER = '%(asctime)s %(levelname)-5s %(name)s %(filename)-21s:%(lineno)-3d %(message)s'

# 请求重试次数
REQUEST_RETRY_TIME = 1
# 请求重试间隔(s)
REQUEST_RETRY_INTERVAL = 1
# 请求超时(s)
REQUEST_TIMEOUT = 7

# 是否需要IP代理
NEED_PROXY = True
# 代理IP池url
PROXY_POOL_URL = 'http://127.0.0.1:5010/get/'

# 每次执行爬取过去几天的数据
INTERVAL_DAYS = 2

# 最大线程数
MAX_THREAD = 32

# MySQL数据库连接
MYSQL_HOSTNAME = 'localhost'
MYSQL_PORT = 3306
MYSQL_USERNAME = 'root'
MYSQL_PASSWORD = '123456'
MYSQL_SCHEMA = 'cg_spider'

# 日志级别
LOG_LEVEL = 'DEBUG'
# 日志文件保留数量
LOG_BACKUP_COUNT = 30

# 定时任务
# 天工e招（天工开物电子招投标交易平台）
TGCW_ZHAOBIAO_XMGG_CRON = '5 0 * * *'  # 招标公告
TGCW_ZHAOBIAO_BIDZBGS_CRON = '10 0 * * *'  # 中标候选人公示
TGCW_ZHAOBIAO_BIDZBGG_CRON = '15 0 * * *'  # 中标结果公告
# 必联网
EBNEW_CRON = '20 0 * * *'  # 招标项目
