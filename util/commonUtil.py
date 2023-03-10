# -*- coding: utf-8 -*-


__author__ = 'shaw'

from datetime import datetime, timedelta

import requests


def with_metaclass(meta, *bases):
    """Create a base class with a metaclass."""

    # This requires a bit of explanation: the basic idea is to make a dummy
    # metaclass for one level of class instantiation that replaces itself with
    # the actual metaclass.
    class MetaClass(meta):

        def __new__(cls, name, this_bases, d):
            return meta(name, bases, d)

    return type.__new__(MetaClass, 'temporary_class', (), {})


def judge_expired(date_str, interval_days):
    """
    判断公告是否过期
    :param date_str:
    :param interval_days:
    :return:
    """

    bid_date = datetime.strptime(date_str, "%Y-%m-%d")
    expired_date = datetime.now() - timedelta(days=interval_days)
    return bid_date < expired_date


def cron_2_trigger(cron_str):
    """
    cron表达式转 APScheduler trigger 参数
    """
    trigger_dict = {'trigger': 'cron',
                    'timezone': 'Asia/Shanghai'}
    for index, value in enumerate(cron_str.split(' ')):
        if index == 0:
            trigger_dict['minute'] = value
        elif index == 1:
            trigger_dict['hour'] = value
        elif index == 2:
            trigger_dict['day'] = value
        elif index == 3:
            trigger_dict['month'] = value
        elif index == 4:
            trigger_dict['day_of_week'] = value
    return trigger_dict


def cookie_str_2_jar(cookie_str):
    """
    cookie字符串转cookiejar
    """
    cookie_dict = {}
    for item in cookie_str.split(';'):
        item_kv = item.split('=')
        key = item_kv[0].strip()
        if len(item_kv) == 1:
            cookie_dict[key] = ''
        else:
            cookie_dict[key] = item_kv[1].strip()
    return requests.utils.cookiejar_from_dict(cookie_dict)
