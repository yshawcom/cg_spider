#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = 'shaw'

import setting
from spider.zhaobiaoSpider import ZhaobiaoSpider

if __name__ == '__main__':
    # 招标公告
    ZhaobiaoSpider(setting.TYPE_XMGG).run()
    # 中标候选人公示
    ZhaobiaoSpider(setting.TYPE_BIDZBGS).run()
    # 中标结果公告
    ZhaobiaoSpider(setting.TYPE_BIDZBGG).run()
