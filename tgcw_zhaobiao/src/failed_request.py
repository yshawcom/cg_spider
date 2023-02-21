# -*- coding: utf-8 -*-


"""
失败的请求及次数
"""

__author__ = 'shaw'

import logging.config

import yaml

# 加载日志配置文件
with open('./logconf.yml', 'r', encoding='utf-8') as f:
    dict_conf = yaml.safe_load(f)
logging.config.dictConfig(dict_conf)
logger = logging.getLogger(__name__)

# 失败的请求及次数
requests = {}


def get(url):
    return requests.get(url, 0)


def add(url):
    requests[url] = get(url) + 1
    logger.info('失败的请求及次数: %s', requests)


def remove(url):
    if url in requests:
        requests.pop(url)
    logger.info('失败的请求及次数: %s', requests)
