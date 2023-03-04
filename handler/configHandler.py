# -*- coding: utf-8 -*-


__author__ = 'shaw'

import logging
import os

import setting
from util.commonUtil import with_metaclass
from util.lazyProperty import LazyProperty
from util.singleton import Singleton


logging_level_dict = {'CRITICAL': logging.FATAL,
                      'FATAL': logging.FATAL,
                      'ERROR': logging.ERROR,
                      'WARNING': logging.WARN,
                      'WARN': logging.WARN,
                      'INFO': logging.INFO,
                      'DEBUG': logging.DEBUG,
                      'NOTSET': logging.NOTSET}


class ConfigHandler(with_metaclass(Singleton)):

    def __init__(self):
        pass


    @LazyProperty
    def request_retry_time(self):
        """
        请求重试次数
        """
        return int(os.environ.get('REQUEST_RETRY_TIME', setting.REQUEST_RETRY_TIME))


    @LazyProperty
    def request_retry_interval(self):
        """
        请求重试间隔(s)
        """
        return int(os.environ.get('REQUEST_RETRY_INTERVAL', setting.REQUEST_RETRY_INTERVAL))


    @LazyProperty
    def request_timeout(self):
        """
        请求超时(s)
        """
        return int(os.environ.get('REQUEST_TIMEOUT', setting.REQUEST_TIMEOUT))


    @LazyProperty
    def need_proxy(self):
        """
        是否需要IP代理
        """
        need_proxy = os.environ.get('NEED_PROXY', setting.NEED_PROXY)
        if need_proxy is True or need_proxy == 'True':
            need_proxy_bool = True
        elif need_proxy is False or need_proxy == 'False':
            need_proxy_bool = False
        else:
            raise ValueError('NEED_PROXY 配置错误')
        return need_proxy_bool


    @LazyProperty
    def proxy_pool_url(self):
        """
        代理IP池url
        """
        return os.environ.get('PROXY_POOL_URL', setting.PROXY_POOL_URL)


    @LazyProperty
    def interval_days(self):
        """
        每次执行爬取过去几天的数据
        """
        return int(os.environ.get('INTERVAL_DAYS', setting.INTERVAL_DAYS))


    @LazyProperty
    def max_thread(self):
        """
        最大线程数
        """
        return int(os.environ.get('MAX_THREAD', setting.MAX_THREAD))


    @LazyProperty
    def mysql_hostname(self):
        """
        MySQL数据库连接hostname
        """
        return os.environ.get('MYSQL_HOSTNAME', setting.MYSQL_HOSTNAME)


    @LazyProperty
    def mysql_port(self):
        """
        MySQL数据库连接port
        """
        return str(os.environ.get('MYSQL_PORT', setting.MYSQL_PORT))


    @LazyProperty
    def mysql_username(self):
        """
        MySQL数据库连接username
        """
        return os.environ.get('MYSQL_USERNAME', setting.MYSQL_USERNAME)


    @LazyProperty
    def mysql_password(self):
        """
        MySQL数据库连接password
        """
        return os.environ.get('MYSQL_PASSWORD', setting.MYSQL_PASSWORD)


    @LazyProperty
    def mysql_schema(self):
        """
        MySQL数据库连接schema
        """
        return os.environ.get('MYSQL_SCHEMA', setting.MYSQL_SCHEMA)


    @LazyProperty
    def log_level(self):
        """
        日志级别
        """
        log_level = os.environ.get('LOG_LEVEL', setting.LOG_LEVEL).upper()
        if log_level in logging_level_dict:
            return logging_level_dict[log_level]
        else:
            raise ValueError('LOG_LEVEL 配置错误')


    @LazyProperty
    def log_backup_count(self):
        """
        日志文件保留数量
        """
        return int(os.environ.get('LOG_BACKUP_COUNT', setting.LOG_BACKUP_COUNT))


    @LazyProperty
    def tgcw_zhaobiao_cron(self):
        """
        天工e招 定时配置
        """
        return (os.environ.get('TGCW_ZHAOBIAO_XMGG_CRON', setting.TGCW_ZHAOBIAO_XMGG_CRON),
                os.environ.get('TGCW_ZHAOBIAO_BIDZBGS_CRON', setting.TGCW_ZHAOBIAO_BIDZBGS_CRON),
                os.environ.get('TGCW_ZHAOBIAO_BIDZBGG_CRON', setting.TGCW_ZHAOBIAO_BIDZBGG_CRON))


    @LazyProperty
    def ebnew_cron(self):
        """
        必联网
        """
        return os.environ.get('EBNEW_CRON', setting.EBNEW_CRON)


    @LazyProperty
    def jtsww_cron(self):
        """
        建投商务网 定时配置
        """
        return (os.environ.get('JTSWW_BIDDING_NOTICE_CRON', setting.JTSWW_BIDDING_NOTICE_CRON),
                os.environ.get('JTSWW_CANDIDATEAN_NO_CRON', setting.JTSWW_CANDIDATEAN_NO_CRON),
                os.environ.get('JTSWW_WIN_NOTICE_CRON', setting.JTSWW_WIN_NOTICE_CRON))


if __name__ == '__main__':
    conf = ConfigHandler()
    print(conf.jtsww_cron)
