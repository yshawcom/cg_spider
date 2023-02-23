# -*- coding: utf-8 -*-


"""
天工e招（天工开物电子招投标交易平台）
"""

__author__ = 'shaw'

from datetime import datetime

from bs4 import BeautifulSoup

import setting
from const import tgcwZhaobiaoConst
from dao import tgcwZhaobiaoDao
from handler.configHandler import ConfigHandler
from handler.logHandler import LogHandler
from model.tgcwZhaobiaoModel import TgcwZhaobiaoModel
from util import commonUtil
from util.webRequest import WebRequest


class TgcwZhaobiaoSpider:

    def __init__(self, notice_type):
        self.type = notice_type
        self.conf = ConfigHandler()
        self.log = LogHandler(tgcwZhaobiaoConst.NAME)

    def parse_detail_html(self, url, html):
        """
        格式化公告详情
        :param url:
        :param html:
        :return:
        """

        id = url[url.rindex('/') + 1: url.rindex('.')]
        self.log.info('公告ID: %s', id)

        # 判断数据库是否已存在相同id数据
        notice = tgcwZhaobiaoDao.find_top_by_ori_id_and_type_code(int(id), self.type)
        if notice is not None:
            self.log.info('公告 %s 已存在', id)
            return

        soup = BeautifulSoup(html, 'lxml')

        ninfo_title_h2s = soup.select('#main > div.listPage.wrap > div > div.mleft > div > div > div.ninfo-title > h2')
        if len(ninfo_title_h2s) <= 0:
            return

        title = ninfo_title_h2s[0].text
        self.log.info('公告名称: %s', title)

        ninfo_title_spans = soup.select(
            '#main > div.listPage.wrap > div > div.mleft > div > div > div.ninfo-title > span')
        publish_time_text = ninfo_title_spans[0].text
        publish_time = publish_time_text[publish_time_text.index('：') + 1:].strip()
        self.log.info('发布时间: %s', publish_time)

        notice_content = soup.select('#main > div.listPage.wrap > div > div.mleft > div > div > div.ninfo-con')[0]
        # self.log.info('公告正文: %s', str(notice_content))

        # 保存到数据库
        notice = TgcwZhaobiaoModel()
        notice.ori_id = id
        notice.type_code = self.type
        notice.type_name = setting.TYPE_DICT.get(self.type, '')
        notice.notice_title = title
        notice.publish_time = datetime.strptime(publish_time, "%Y-%m-%d %H:%M:%S")
        notice.notice_content = str(notice_content).replace('\n', '').strip()
        notice.update_time = datetime.now()
        tgcwZhaobiaoDao.save(notice)
        self.log.info('公告 %s 已保存到数据库', id)

    def request_detail(self, url):
        """
        请求公告页
        :param url:
        :return:
        """

        self.log.info('请求公告页URL: %s', url)
        resp_text = WebRequest(self.log).get(tgcwZhaobiaoConst.BASE_URL + url).text
        self.parse_detail_html(url, resp_text)

    def parse_list_html(self, html):
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

        # self.log.error(uls)
        ul = uls[0]
        for li in ul.find_all('li'):
            self.log.info('')
            date_str = li.find_all('span', class_='bidDate')[0].text
            title = li.find_all('span', class_='bidLink')[0].text
            self.log.info('[%s] %s', date_str, title)

            if commonUtil.judge_expired(date_str, self.conf.interval_days):
                self.log.info('该公告已过期，停止爬取')
                expired_notice = True
                break

            self.request_detail(li.a['href'])

        return expired_notice

    def request_list(self, page_no):
        """
        请求列表页
        :param page_no:
        :return:
        """

        url = tgcwZhaobiaoConst.LIST_URL % (self.type, page_no)
        self.log.info('请求列表URL: %s', url)

        resp_text = WebRequest(self.log).get(url).text
        expired_notice = self.parse_list_html(resp_text)
        if expired_notice is False:
            # 整个列表都没有过期的公告，继续爬下一页
            self.log.info('')
            self.log.info('---------------- 请求列表第 %s 页', page_no + 1)
            self.request_list(page_no + 1)
        else:
            self.log.info('已没有待爬取的公告数据')

    def run(self):
        # 页数
        page_no = 1
        self.log.info('')
        self.log.info('---------------- 请求列表第 %s 页', page_no)
        self.request_list(page_no)


if __name__ == '__main__':
    # 招标公告
    TgcwZhaobiaoSpider(tgcwZhaobiaoConst.XMGG).run()
    # 中标候选人公示
    TgcwZhaobiaoSpider(tgcwZhaobiaoConst.BIDZBGS).run()
    # 中标结果公告
    TgcwZhaobiaoSpider(tgcwZhaobiaoConst.BIDZBGG).run()
