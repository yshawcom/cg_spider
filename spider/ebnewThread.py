# -*- coding: utf-8 -*-

"""
必联网
"""

__author__ = 'shaw'

import threading

from const import ebnewConst
from handler.configHandler import ConfigHandler
from handler.logHandler import LogHandler
from spider.ebnewSpider import EbnewSpider

log = LogHandler(ebnewConst.NAME)
conf = ConfigHandler()


class EbnewThread(threading.Thread):
    def __init__(self, thread_id, name):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name

    def run(self):
        # 计算出每个线程的页面数
        page_per_thread = ebnewConst.LIST_MAX_PAGE / conf.max_thread

        for index in range(ebnewConst.LIST_MAX_PAGE):
            if index // page_per_thread == self.thread_id:
                page = index + 1
                log.info('thread=%s, page=%s' % (self.thread_id, page))
                EbnewSpider().run(page)


if __name__ == '__main__':
    for i in range(conf.max_thread):
        thread = EbnewThread(i, 'EbnewThread-' + str(i))
        thread.start()
