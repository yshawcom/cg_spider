# -*- coding: utf-8 -*-


__author__ = 'shaw'

import threading

from const import ebnewConst
from handler.configHandler import ConfigHandler
from spider.ebnewSpider import EbnewSpider

conf = ConfigHandler()


class EbnewThread(threading.Thread):
    def __init__(self, thread_id, name):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name

    def run(self):
        # 计算出每个线程的页面数
        page_per_thread = ebnewConst.LIST_MAX_PAGE // conf.max_thread

        for index in range(ebnewConst.LIST_MAX_PAGE):
            page = index + 1
            if page // page_per_thread + 1 == self.thread_id:
                print('thread=%s, page=%s' % (self.thread_id, page))
                EbnewSpider().run(page)


if __name__ == '__main__':
    for i in range(conf.max_thread):
        thread = EbnewThread(i, 'EbnewThread-' + str(i))
        thread.start()
