# -*- coding: utf-8 -*-


"""
天工e招（天工开物电子招投标交易平台）
"""

__author__ = 'shaw'

NAME = 'tgcw_zhaobiao'

BASE_URL = 'http://zhaobiao.tgcw.net.cn'
# 列表页URL
LIST_URL = BASE_URL + '/cms/channel/%s/index.htm?pageNo=%s'

# 招标公告
XMGG = 'xmgg'

# 中标候选人公示
BIDZBGS = 'bidzbgs'

# 中标结果公告
BIDZBGG = 'bidzbgg'

# 公告类型名称
TYPE_DICT = {XMGG: '招标公告',
             BIDZBGS: '中标候选人公示',
             BIDZBGG: '中标结果公告'}

TYPES = (XMGG,
         BIDZBGS,
         BIDZBGG)

IDS = (NAME + '_' + XMGG,
       NAME + '_' + BIDZBGS,
       NAME + '_' + BIDZBGG)
