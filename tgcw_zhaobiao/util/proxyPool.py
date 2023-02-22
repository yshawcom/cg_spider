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
    json = requests.get(conf.proxy_pool_url).json()
    if need_https == json.get('https'):
        return json.get('proxy')
    return get_proxy(need_https)


def get(url):
    if url.startswith('https://'):
        return {'https': 'http://' + get_proxy(True)}
    if url.startswith('http://'):
        return {'http': 'http://' + get_proxy(False)}
    return {}
