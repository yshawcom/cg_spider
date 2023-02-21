# -*- coding: utf-8 -*-


__author__ = 'shaw'

import requests

"""
代理IP池
https://github.com/jhao104/proxy_pool
"""

PROXY_POOL_URL = 'http://127.0.0.1:5010/get/'


def get_proxy(need_https):
    json = requests.get(PROXY_POOL_URL).json()
    if need_https == json.get('https'):
        return json.get('proxy')
    return get_proxy(need_https)


def get(url):
    if url.startswith('https://'):
        return {'https': 'http://' + get_proxy(True)}
    if url.startswith('http://'):
        return {'http': 'http://' + get_proxy(False)}
    return {}
