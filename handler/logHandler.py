# -*- coding: utf-8 -*-


"""
日志
"""

__author__ = 'shaw'

import logging
import os
# 解决日志文件多线程写入问题
# https://github.com/Preston-Landers/concurrent-log-handler
from datetime import datetime

from concurrent_log_handler import ConcurrentRotatingFileHandler

import setting
from handler.configHandler import ConfigHandler

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(CURRENT_PATH, os.pardir)
LOG_PATH = os.path.join(ROOT_PATH, 'log')

if not os.path.exists(LOG_PATH):
    try:
        os.mkdir(LOG_PATH)
    except FileExistsError:
        pass

conf = ConfigHandler()


class LogHandler(logging.Logger):

    def __init__(self, name, level=conf.log_level, stream=True, file=True):
        self.name = name
        self.level = level
        logging.Logger.__init__(self, self.name, level=level)
        if stream:
            self.__setStreamHandler__()
        if file:
            self.__setFileHandler__()

    def __setFileHandler__(self, level=None):
        """
        set file handler
        :param level:
        :return:
        """

        time = datetime.now().strftime("%Y%m%d%H")
        file_name = os.path.join(LOG_PATH, '%s-%s.log' % (self.name, time))
        # file_handler = TimedRotatingFileHandler(filename=file_name, when='D', interval=1, backupCount=conf.log_backup_count, encoding='utf-8')
        # file_handler.suffix = '%Y%m%d%H%M.log'
        # 日志滚动，日志文件最大2M
        file_handler = ConcurrentRotatingFileHandler(file_name,
                                                     maxBytes=2 * 1024 * 1024,
                                                     backupCount=conf.log_backup_count,
                                                     encoding='utf-8')
        if not level:
            file_handler.setLevel(self.level)
        else:
            file_handler.setLevel(level)
        formatter = logging.Formatter(setting.LOG_FORMATTER)

        file_handler.setFormatter(formatter)
        self.file_handler = file_handler
        self.addHandler(file_handler)

    def __setStreamHandler__(self, level=None):
        """
        set stream handler
        :param level:
        :return:
        """
        stream_handler = logging.StreamHandler()
        formatter = logging.Formatter(setting.LOG_FORMATTER)
        stream_handler.setFormatter(formatter)
        if not level:
            stream_handler.setLevel(self.level)
        else:
            stream_handler.setLevel(level)
        self.addHandler(stream_handler)


if __name__ == '__main__':
    log = LogHandler('test')
    log.info('this is a test msg')
    log.error('这是一条测试信息')
