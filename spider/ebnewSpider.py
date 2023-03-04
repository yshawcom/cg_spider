# -*- coding: utf-8 -*-


"""
必联网
"""

__author__ = 'shaw'

from datetime import datetime

from bs4 import BeautifulSoup

from const import ebnewConst
from dao import ebnewDao
from handler.configHandler import ConfigHandler
from handler.logHandler import LogHandler
from model.ebnewModel import EbnewModel
from spider import ebnewSpiderExtra
from util import commonUtil
from util.webRequest import WebRequest


log = LogHandler(ebnewConst.NAME)
conf = ConfigHandler()


class EbnewSpider:

    def __init__(self):
        self.list_current_page = 1


    def parse_detail_html(self, ori_id, html):
        """
        格式化公告详情
        """

        soup = BeautifulSoup(html, 'lxml')

        # 页面内容
        div_ebnew_details_contents = soup.select('div.ebnew-details-content')
        if len(div_ebnew_details_contents) <= 0:
            log.info('---------------- 公告 %s 未解析出数据', ori_id)
            log.info('')
            return

        div_ebnew_details_content = div_ebnew_details_contents[0]

        h2_details_title = div_ebnew_details_content.select('h2.details-title')[0]
        details_title = h2_details_title.get_text()
        log.info('公告名称: %s', details_title)

        span_release_time = div_ebnew_details_content.select('div.details-widget > span:nth-child(2)')[0]
        release_time = span_release_time.get_text().replace('发布时间：', '')
        log.info('发布时间: %s', release_time)

        # 项目信息
        ul_ebnew_project_information = div_ebnew_details_content.select('ul.ebnew-project-information')[0]

        span_bidcode = ul_ebnew_project_information.select('#bidcode > span:nth-child(2)')[0]
        bidcode = span_bidcode.get_text()
        log.info('项目编号: %s', bidcode)

        span_announcement_type = ul_ebnew_project_information.select('li:nth-child(2) > span.item-value')[0]
        announcement_type = span_announcement_type.get_text().strip()
        log.info('公告类型: %s', announcement_type)

        span_tender_method = ul_ebnew_project_information.select('li:nth-child(3) > span.item-value')[0]
        tender_method = span_tender_method.get_text()
        log.info('招标方式: %s', tender_method)

        span_deadline = ul_ebnew_project_information.select('li:nth-child(4) > span.item-value')[0]
        deadline = span_deadline.get_text()
        log.info('截止时间: %s', deadline)

        span_orgname = ul_ebnew_project_information.select('#orgname > span.item-value')[0]
        orgname = span_orgname.get_text().strip()
        log.info('招标机构: %s', orgname)

        span_tender_area = ul_ebnew_project_information.select('li:nth-child(6) > span.item-value')[0]
        tender_area = span_tender_area.get_text()
        log.info('招标地区: %s', tender_area)

        span_tender_products = ul_ebnew_project_information.select('li:nth-child(7) > span.item-value')[0]
        tender_products = span_tender_products.get_text()
        log.info('招标产品: %s', tender_products)

        span_industry = ul_ebnew_project_information.select('li:nth-child(8) > span.item-value')[0]
        industry_l = span_industry.get_text().split(';')
        industry_l_f = filter(lambda i: i != '', industry_l)
        industry = ','.join(list(industry_l_f))
        log.info('所属行业: %s', industry)

        div_details_content = div_ebnew_details_content.select('div#notLogin')[0]
        details_content = str(div_details_content) \
            .replace('\n', '') \
            .replace('	', '') \
            .replace('  ', ' ')
        # log.info('主体内容: %s', details_content)

        # 保存到数据库
        model = EbnewModel()
        model.ori_id = ori_id
        model.details_title = details_title
        model.release_time = datetime.strptime(release_time, "%Y-%m-%d %H:%M")
        model.bidcode = bidcode
        model.announcement_type = announcement_type
        model.tender_method = tender_method
        if deadline:
            model.deadline = datetime.strptime(deadline, "%Y-%m-%d %H:%M:%S")
        model.orgname = orgname
        model.tender_area = tender_area
        model.tender_products = tender_products
        model.industry = industry
        model.details_content = details_content
        model.update_time = datetime.now()
        ebnewDao.save(model)
        log.info('---------------- 公告 %s 已保存到数据库', ori_id)
        log.info('')


    def request_detail(self, url, cookies=None):
        """
        请求公告详情页
        """

        ori_id = url[url.rindex('/') + 1: url.rindex('.')]
        log.info('---------------- 公告ID: %s', ori_id)

        # 判断数据库是否已存在相同id数据
        notice = ebnewDao.find_top_by_ori_id(int(ori_id))
        if notice is not None:
            log.info('---------------- 公告 %s 已存在', ori_id)
            log.info('')
            return

        url = url.replace('http://', 'https://')
        log.info('---------------- 请求公告页URL: %s', url)

        resp = WebRequest(log).post(url, cookies=cookies)
        log.info('---------------- HTTP_CODE: %s', resp.response.status_code)
        if resp.response.status_code == 521:
            # 如果响应的为反爬的js，则处理后再次请求
            cookie_jar = ebnewSpiderExtra.cookie_jar_from_521(resp.text)
            self.request_detail(url, cookies=cookie_jar)
        else:
            self.parse_detail_html(ori_id, resp.text)


    def parse_list_html(self, html):
        """
        解析列表页
        """

        # 列表中是否有已过期的公告
        expired_notice = False

        soup = BeautifulSoup(html, 'lxml')

        div_content_lists = soup.select('div.ebnew-content-list')
        if len(div_content_lists) <= 0:
            log.info('================================ 列表第 %s 页未解析出公告数据', self.list_current_page)
            log.info('')
            return expired_notice

        div_content_list = div_content_lists[0]
        content_list = div_content_list.find_all('div', class_='abstract-box mg-t25 ebnew-border-bottom mg-r15')

        log.info('================================ 列表第 %s 页共有公告 %s 条', self.list_current_page, len(content_list))

        for i, content in enumerate(content_list):
            log.info('---------------- 列表第 %s 页公告第 %s 条', self.list_current_page, i + 1)

            title_a = content.select('div.abstract-head.bg-fff.clearfix > a')[0]
            title = title_a.get_text()

            date_i = content.select('div.abstract-head.bg-fff.clearfix > i.fr.font-12.color-999.mg-t5.mg-r5')[0]
            date_text = date_i.get_text()
            date_str = date_text[date_text.index(':') + 1:]

            log.info('---------------- [%s] %s', date_str, title)

            if commonUtil.judge_expired(date_str, conf.interval_days):
                log.info('该公告已过期，停止爬取')
                expired_notice = True
                break

            self.request_detail(title_a['href'])

        return expired_notice


    def request_list(self, cookies=None):
        """
        请求公告列表
        """

        data = {
            'projectType': 'bid',
            'sortMethod': 'timeDesc',
            'currentPage': self.list_current_page
        }
        resp = WebRequest(log).post(ebnewConst.LIST_URL, data=data, cookies=cookies)
        log.info('================================ HTTP_CODE: %s', resp.response.status_code)
        if resp.response.status_code == 521:
            # 如果响应的为反爬的js，则处理后再次请求
            cookie_jar = ebnewSpiderExtra.cookie_jar_from_521(resp.text)
            return self.request_list(cookies=cookie_jar)
        else:
            expired_notice = self.parse_list_html(resp.text)

        """
        if expired_notice:
            log.info('================================ 已没有待爬取的公告数据')
        elif self.list_current_page >= ebnewConst.LIST_MAX_PAGE:
            log.info('================================ 已爬到列表最大页数 %s', ebnewConst.LIST_MAX_PAGE)
        else:
            # 整个列表都没有过期的公告，继续爬下一页
            self.list_current_page += 1
            log.info('================================ 请求列表第 %s 页', self.list_current_page)
            self.request_list()
        """


    def run(self, current_page):
        self.list_current_page = current_page
        log.info('================================ 请求列表第 %s 页', self.list_current_page)
        self.request_list()


if __name__ == '__main__':
    EbnewSpider().run(1)
