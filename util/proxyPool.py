# -*- coding: utf-8 -*-


"""
代理IP池
https://github.com/jhao104/proxy_pool
"""

__author__ = 'shaw'

import requests

from handler.configHandler import ConfigHandler

conf = ConfigHandler()


def get_proxy(need_https):
    if need_https:
        type = '?type=https'
    else:
        type = '?type=http'
    resp = requests.get(conf.proxy_pool_url + type)
    return resp.json().get('proxy')


def get(url):
    if url.startswith('https://'):
        return {'https': 'https://' + get_proxy(True)}
    if url.startswith('http://'):
        return {'http': 'http://' + get_proxy(False)}
    return {}
