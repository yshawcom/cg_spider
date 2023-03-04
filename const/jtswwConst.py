# -*- coding: utf-8 -*-


"""
建投商务网
"""

__author__ = 'shaw'

NAME = 'jtsww'

BASE_URL = 'https://www.jtsww.com/'
# 列表请求URL
LIST_URL = BASE_URL + 'bidding-portalsite/information/indexnotice'
# 详情页URL
DETAIL_URL = BASE_URL + 'notice/detail'

# 招标公告
BIDDING_NOTICE = 'biddingnotice'

# 中标候选人公示
CANDIDATEAN_NO = 'candidateanno'

# 中标结果公告
WIN_NOTICE = 'winnotice'

# 公告类型名称
TYPE_DICT = {BIDDING_NOTICE: '招标公告',
             CANDIDATEAN_NO: '中标候选人公示',
             WIN_NOTICE: '中标结果公告'}

TYPES = (BIDDING_NOTICE,
         CANDIDATEAN_NO,
         WIN_NOTICE)

IDS = (NAME + '_' + BIDDING_NOTICE,
       NAME + '_' + CANDIDATEAN_NO,
       NAME + '_' + WIN_NOTICE)
