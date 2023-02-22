# -*- coding: utf-8 -*-


"""
招标公告
"""

__author__ = 'shaw'

from datetime import timedelta, datetime

from bs4 import BeautifulSoup

import setting
from dao import xmggNoticeDao
from handler.configHandler import ConfigHandler
from handler.logHandler import LogHandler
from model.xmggNotice import XmggNotice
from util.webRequest import WebRequest

conf = ConfigHandler()
log = LogHandler('tgcw_zhaobiao_xmgg')

expired_date = datetime.now() - timedelta(days=conf.interval_days)


def judge_expired(date_str):
    """
    判断公告是否过期
    :param date_str:
    :return:
    """

    bid_date = datetime.strptime(date_str, "%Y-%m-%d")
    return bid_date < expired_date


def parse_detail_html(url, html):
    """
    格式化公告详情
    :param url:
    :param html:
    :return:
    """

    id = url[url.rindex('/') + 1: url.rindex('.')]
    log.info('公告ID: %s', id)

    # 判断数据库是否已存在相同id数据
    notice = xmggNoticeDao.find_top_by_ori_id(int(id))
    if notice is not None:
        log.info('公告 %s 已存在', id)
        return

    soup = BeautifulSoup(html, 'lxml')

    title = soup.select('#main > div.listPage.wrap > div > div.mleft > div > div > div.ninfo-title > h2')[0].text
    log.info('公告名称: %s', title)

    ninfo_title_spans = soup.select('#main > div.listPage.wrap > div > div.mleft > div > div > div.ninfo-title > span')
    publish_time_text = ninfo_title_spans[0].text
    publish_time = publish_time_text[publish_time_text.index('：') + 1:].strip()
    log.info('发布时间: %s', publish_time)

    notice_content = soup.select('#main > div.listPage.wrap > div > div.mleft > div > div > div.ninfo-con')[0]
    # log.info('公告正文: %s', str(notice_content))

    # 保存到数据库
    notice = XmggNotice()
    notice.ori_id = id
    notice.notice_title = title
    notice.publish_time = datetime.strptime(publish_time, "%Y-%m-%d %H:%M:%S")
    notice.notice_content = str(notice_content).replace('\n', '').strip()
    notice.update_time = datetime.now()
    xmggNoticeDao.save(notice)
    log.info('公告 %s 已保存到数据库', id)


def request_detail(url):
    """
    请求公告页
    :param url:
    :return:
    """

    log.info('请求公告页URL: %s', url)
    resp_text = WebRequest(log).get(setting.BASE_URL + url).text
    parse_detail_html(url, resp_text)


def parse_list_html(html):
    """
    解析列表页
    :param html:
    :return:
    """

    # 列表中是否有已过期的公告
    expired_notice = False

    soup = BeautifulSoup(html, 'lxml')
    uls = soup.select('#main > div.listPage.wrap > div > div.mleft > div > div.m-bd > div > div > ul')
    if len(uls) <= 0:
        return expired_notice

    # log.error(uls)
    ul = uls[0]
    for li in ul.find_all('li'):
        log.info('')
        date_str = li.find_all('span', class_='bidDate')[0].text
        title = li.find_all('span', class_='bidLink')[0].text
        log.info('[%s] %s', date_str, title)

        if judge_expired(date_str):
            log.info('该公告已过期，停止爬取')
            expired_notice = True
            break

        request_detail(li.a['href'])

    return expired_notice


def request_list(page_no):
    """
    请求列表页
    :param page_no:
    :return:
    """

    url = setting.LIST_URL + str(page_no)
    log.info('请求列表URL: %s', url)

    resp_text = WebRequest(log).get(url).text
    expired_notice = parse_list_html(resp_text)
    if expired_notice is False:
        # 整个列表都没有过期的公告，继续爬下一页
        log.info('')
        log.info('---------------- 请求列表第 %s 页', page_no + 1)
        request_list(page_no + 1)
    else:
        log.info('已没有待爬取的公告数据')


def run():
    # 页数
    page_no = 1
    log.info('')
    log.info('---------------- 请求列表第 %s 页', page_no)
    request_list(page_no)
