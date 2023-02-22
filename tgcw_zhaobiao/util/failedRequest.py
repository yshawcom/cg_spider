# -*- coding: utf-8 -*-


"""
失败的请求及次数
"""

__author__ = 'shaw'


from handler.logHandler import LogHandler

log = LogHandler('tgcw_zhaobiao')

# 失败的请求及次数
requests = {}


def get(url):
    return requests.get(url, 0)


def add(url):
    requests[url] = get(url) + 1
    log.info('失败的请求及次数: %s', requests)


def remove(url):
    if url in requests:
        requests.pop(url)
    log.info('失败的请求及次数: %s', requests)
