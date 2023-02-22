# -*- coding: utf-8 -*-


__author__ = 'shaw'

import logging
import os

import setting
from util.commonUtil import with_metaclass
from util.lazyProperty import LazyProperty
from util.singleton import Singleton


class ConfigHandler(with_metaclass(Singleton)):

    def __init__(self):
        pass

    @LazyProperty
    def max_retry(self):
        """
        最大重试次数
        :return:
        """
        return int(os.environ.get('MAX_RETRY', setting.MAX_RETRY))

    @LazyProperty
    def need_proxy(self):
        """
        是否需要IP代理
        :return:
        """
        return bool(os.environ.get('NEED_PROXY', setting.NEED_PROXY))

    @LazyProperty
    def proxy_pool_url(self):
        """
        代理IP池url
        :return:
        """
        return os.environ.get('PROXY_POOL_URL', setting.PROXY_POOL_URL)

    @LazyProperty
    def interval_days(self):
        """
        每次执行爬取过去几天的数据
        :return:
        """
        return int(os.environ.get('INTERVAL_DAYS', setting.INTERVAL_DAYS))

    @LazyProperty
    def request_timeout(self):
        """
        请求超时（s）
        :return:
        """
        return int(os.environ.get('REQUEST_TIMEOUT', setting.REQUEST_TIMEOUT))

    @LazyProperty
    def mysql_hostname(self):
        """
        MySQL数据库连接hostname
        :return:
        """
        return os.environ.get('MYSQL_HOSTNAME', setting.MYSQL_HOSTNAME)

    @LazyProperty
    def mysql_port(self):
        """
        MySQL数据库连接port
        :return:
        """
        return str(os.environ.get('MYSQL_PORT', setting.MYSQL_PORT))

    @LazyProperty
    def mysql_username(self):
        """
        MySQL数据库连接username
        :return:
        """
        return os.environ.get('MYSQL_USERNAME', setting.MYSQL_USERNAME)

    @LazyProperty
    def mysql_password(self):
        """
        MySQL数据库连接password
        :return:
        """
        return os.environ.get('MYSQL_PASSWORD', setting.MYSQL_PASSWORD)

    @LazyProperty
    def mysql_schema(self):
        """
        MySQL数据库连接schema
        :return:
        """
        return os.environ.get('MYSQL_SCHEMA', setting.MYSQL_SCHEMA)

    @LazyProperty
    def mysql_schema(self):
        """
        MySQL数据库连接schema
        :return:
        """
        return os.environ.get('MYSQL_SCHEMA', setting.MYSQL_SCHEMA)

    @LazyProperty
    def log_level(self):
        """
        日志级别
        :return:
        """
        logging_level = logging.DEBUG
        level = os.environ.get('LOG_LEVEL', setting.LOG_LEVEL).upper()
        if level == 'CRITICAL' or level == 'FATAL':
            logging_level = logging.FATAL
        elif level == 'ERROR':
            logging_level = logging.ERROR
        elif level == 'WARNING' or level == 'WARN':
            logging_level = logging.WARN
        elif level == 'INFO':
            logging_level = logging.INFO
        elif level == 'DEBUG':
            logging_level = logging.DEBUG
        elif level == 'NOTSET':
            logging_level = logging.NOTSET
        else:
            raise ValueError('LOG_LEVEL 配置错误')
        return logging_level

    @LazyProperty
    def log_backup_count(self):
        """
        日志文件保留数量
        :return:
        """
        return int(os.environ.get('LOG_BACKUP_COUNT', setting.LOG_BACKUP_COUNT))