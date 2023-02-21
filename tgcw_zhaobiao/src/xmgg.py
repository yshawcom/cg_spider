# -*- coding: utf-8 -*-


"""
招标公告
"""

__author__ = 'shaw'

import logging.config
from datetime import timedelta, datetime

import requests
import yaml
from bs4 import BeautifulSoup

import failed_request
import setting
import xmgg_notice_dao
from util import user_agent, proxy
from xmgg_notice import XmggNotice

expired_date = datetime.now() - timedelta(days=setting.INTERVAL_DAYS)

# 加载日志配置文件
with open('./logconf.yml', 'r', encoding='utf-8') as f:
    dict_conf = yaml.safe_load(f)
logging.config.dictConfig(dict_conf)
log = logging.getLogger(__name__)


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
    notice = xmgg_notice_dao.find_top_by_ori_id(int(id))
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
    xmgg_notice_dao.save(notice)
    log.info('公告 %s 已保存到数据库', id)


def retry_request_detail(url):
    """
    重试公告页
    :param url:
    :return:
    """
    failed_request.add(url)
    failed_times = failed_request.get(url)
    if failed_request.get(url) < setting.MAX_RETRY:
        # 重试
        log.info('================ 第 %s 次请求公告页: %s', failed_times + 1, url)
        request_detail(url)
    else:
        log.error('公告页请求 %s 已失败 %s 次，停止请求', url, failed_times)


def request_detail(url):
    """
    请求公告页
    :param url:
    :return:
    """
    log.info('公告页URL: %s', url)
    headers = {'User-Agent': user_agent.get()}
    proxies = {}
    if setting.NEED_PROXY:
        proxies = proxy.get(setting.BASE_URL)
        log.info('使用代理IP: %s', proxies)

    try:
        resp = requests.get(setting.BASE_URL + url, headers=headers, proxies=proxies, timeout=setting.REQUEST_TIMEOUT)
        log.info('公告页请求状态: %s', resp.status_code)
        if resp.status_code == 200:
            # 请求成功后，删除之前的失败记录
            failed_request.remove(url)
            parse_detail_html(url, resp.text)
        else:
            retry_request_detail(url)
    except Exception as e:
        log.error('公告页请求失败: %s', url)
        log.exception(e)
        retry_request_detail(url)

    pass


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

        href = li.a['href']
        log.info('================ 第 1 次请求公告页: %s', href)
        request_detail(href)

    return expired_notice


def retry_request_list(url, page_no):
    """
    重试列表页
    :param url:
    :param page_no:
    :return:
    """
    failed_request.add(url)
    failed_times = failed_request.get(url)
    if failed_request.get(url) < setting.MAX_RETRY:
        # 重试
        log.info('')
        log.info('---------------- 第 %s 次请求列表第 %s 页', failed_times + 1, page_no)
        request_list(page_no)
    else:
        log.error('列表请求 %s 已失败 %s 次，停止请求', url, failed_times)


def request_list(page_no):
    """
    请求列表页
    :param page_no:
    :return:
    """

    url = setting.LIST_URL + str(page_no)
    log.info('列表URL: %s', url)
    headers = {'User-Agent': user_agent.get()}
    proxies = {}
    if setting.NEED_PROXY:
        proxies = proxy.get(setting.LIST_URL)
        log.info('使用代理IP: %s', proxies)

    try:
        resp = requests.get(url, headers=headers, proxies=proxies, timeout=setting.REQUEST_TIMEOUT)
        log.info('列表第 %s 页请求状态: %s', page_no, resp.status_code)
        if resp.status_code == 200:
            # 请求成功后，删除之前的失败记录
            failed_request.remove(url)
            expired_notice = parse_list_html(resp.text)
            if expired_notice is False:
                # 整个列表都没有过期的公告，继续爬下一页
                log.info('')
                log.info('---------------- 第 1 次请求列表第 %s 页', page_no + 1)
                request_list(page_no + 1)
            else:
                log.info('已没有待爬取的公告数据')
        else:
            retry_request_list(url, page_no)
    except Exception as e:
        log.error('列表第 %s 页请求失败', page_no)
        log.exception(e)
        retry_request_list(url, page_no)


def run():
    # 页数
    page_no = 1
    log.info('')
    log.info('---------------- 第 1 次请求列表第 %s 页', page_no)
    request_list(page_no)
