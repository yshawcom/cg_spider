# -*- coding: utf-8 -*-


"""
日志
"""

__author__ = 'shaw'

import logging
import os
from logging.handlers import TimedRotatingFileHandler

from handler.configHandler import ConfigHandler

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.join(CURRENT_PATH, os.pardir)
LOG_PATH = os.path.join(ROOT_PATH, 'log')

if not os.path.exists(LOG_PATH):
    try:
        os.mkdir(LOG_PATH)
    except FileExistsError:
        pass

FORMATTER = '%(asctime)s %(levelname)-5s %(name)-7s %(filename)-17s:%(lineno)-4d %(message)s'

conf = ConfigHandler()


class LogHandler(logging.Logger):

    def __init__(self, name, level=conf.log_level, stream=True, file=True):
        self.name = name
        self.level = level
        logging.Logger.__init__(self, self.name, level=level)
        if stream:
            self.__setStreamHandler__()
        if file:
            # Windows下TimedRotatingFileHandler线程不安全
            # if platform.system() != "Windows":
            self.__setFileHandler__()

    def __setFileHandler__(self, level=None):
        """
        set file handler
        :param level:
        :return:
        """

        file_name = os.path.join(LOG_PATH, '{name}.log'.format(name=self.name))
        # 设置日志回滚, 保存在log目录, 一天保存一个文件, 保留15天
        file_handler = TimedRotatingFileHandler(filename=file_name, when='D', interval=1,
                                                backupCount=conf.log_backup_count, encoding='utf-8')
        file_handler.suffix = '%Y%m%d.log'
        if not level:
            file_handler.setLevel(self.level)
        else:
            file_handler.setLevel(level)
        formatter = logging.Formatter(FORMATTER)

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
        formatter = logging.Formatter(FORMATTER)
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
