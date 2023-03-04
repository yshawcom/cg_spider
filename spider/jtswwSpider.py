# -*- coding: utf-8 -*-


"""
建投商务网
"""

__author__ = 'shaw'

from datetime import datetime

from bs4 import BeautifulSoup

from const import jtswwConst
from dao import jtswwDao
from handler.configHandler import ConfigHandler
from handler.logHandler import LogHandler
from model.jtswwModel import JtswwModel
from util import commonUtil
from util.webRequest import WebRequest


conf = ConfigHandler()
log = LogHandler(jtswwConst.NAME)


class JtswwSpider:

    def __init__(self, notice_type):
        self.type = notice_type
        self.list_current_page = 1


    def parse_detail_html(self, record, html):
        guid = record['guid']
        log.info('原id: %s', guid)

        log.info('公告类型编码: %s', self.type)

        type_name = jtswwConst.TYPE_DICT[self.type]
        log.info('公告类型: %s', type_name)

        name = record['name'].strip()
        log.info('公告标题: %s', name)

        log.info('发布时间: %s', record['time'])

        project_type = record.get('projecttype', '')
        log.info('项目类型编码: %s', project_type)

        log.info('类型: %s', record['type'])

        bid_section_code = record.get('bid_section_code', '')
        log.info('项目编号: %s', bid_section_code)

        doc_get_start_time = record.get('docgetstarttime', None)
        log.info('文件获取时间: %s', doc_get_start_time)

        tender_agency_lxr = record.get('tenderagencylxr', '')
        log.info('项目经理: %s', tender_agency_lxr)

        tender_agency_name = record.get('tenderagencyname', '')
        log.info('招标机构名称: %s', tender_agency_name)

        tenderer_name = record.get('tenderername', '')
        log.info('招标人: %s', tenderer_name)

        # file = open('../other/jtsww_' + guid + '.html', mode='w+', encoding='utf-8')
        # file.write(html)
        # file.close()

        soup = BeautifulSoup(html, 'lxml')
        div_detail_texts = soup.select('#__layout > div > div.page-body > div > div > div > div.detail > div.text')
        if len(div_detail_texts) <= 0:
            log.info('---------------- 公告 %s 未解析出数据', guid)
            log.info('')
            return

        notice_content = str(div_detail_texts[0]) \
            .replace('\n', '') \
            .replace('	', '') \
            .replace('  ', ' ')
        # log.info('公告内容: %s', notice_content)

        # 保存到数据库
        model = JtswwModel()
        model.guid = guid
        model.type_code = self.type
        model.type_name = type_name
        model.name = name
        model.time = datetime.strptime(record['time'], "%Y-%m-%d")
        model.project_type = project_type
        model.type = record['type']
        model.bid_section_code = bid_section_code
        if doc_get_start_time:
            model.doc_get_start_time = datetime.strptime(doc_get_start_time, "%Y-%m-%d")
        model.tender_agency_lxr = tender_agency_lxr
        model.tender_agency_name = tender_agency_name
        model.tenderer_name = tenderer_name
        model.notice_content = notice_content
        model.update_time = datetime.now()
        jtswwDao.save(model)
        log.info('---------------- 公告 %s 已保存到数据库', guid)
        log.info('')


    def request_detail(self, record):
        """
        请求详情页
        """
        guid = record['guid']
        log.info('---------------- 公告ID: %s', guid)

        # 判断数据库是否已存在相同id数据
        notice = jtswwDao.find_top_by_guid_and_type_code(guid, self.type)
        if notice is not None:
            log.info('---------------- 公告 %s 已存在', guid)
            log.info('')
            return

        params = {'id': guid,
                  'type': self.type}
        resp = WebRequest(log).get(jtswwConst.DETAIL_URL, params=params)
        self.parse_detail_html(record, resp.text)


    def handle_list_data(self, records):
        """
        处理列表数据
        """
        # 列表中是否有已过期的公告
        expired_notice = False
        log.info('================================ 列表第 %s 页共有公告 %s 条', self.list_current_page, len(records))

        for i, record in enumerate(records):
            log.info('---------------- 列表第 %s 页公告第 %s 条', self.list_current_page, i + 1)
            log.info('---------------- [%s] %s', record['time'], record['name'].strip())

            if commonUtil.judge_expired(record['time'], conf.interval_days):
                log.info('该公告已过期，停止爬取')
                expired_notice = True
                break

            self.request_detail(record)

        return expired_notice


    def request_list(self):
        """
        请求列表页
        """
        expired_notice = False
        params = {'t_ignore': datetime.timestamp(datetime.now()),
                  'current': self.list_current_page,
                  'size': 20,
                  'name': '',
                  'type': self.type}
        json = WebRequest(log).get(jtswwConst.LIST_URL, params=params).json
        if len(json) == 0:
            log.info('================================ 列表第 %s 页未请求到数据', self.list_current_page)
        else:
            log.info('================================ 请求列表第 %s 页响应: %s, %s, %s',
                     self.list_current_page, json['success'], json['code'], json['msg'])
            expired_notice = self.handle_list_data(json['data']['records'])

        if expired_notice:
            log.info('================================ 已没有待爬取的公告数据')
        else:
            # 整个列表都没有过期的公告，继续爬下一页
            self.list_current_page += 1
            log.info('================================ 请求列表第 %s 页', self.list_current_page)
            self.request_list()


    def run(self):
        log.info('================================ 请求列表第 %s 页', self.list_current_page)
        self.request_list()


if __name__ == '__main__':
    JtswwSpider(jtswwConst.BIDDING_NOTICE).run()
    JtswwSpider(jtswwConst.CANDIDATEAN_NO).run()
    JtswwSpider(jtswwConst.WIN_NOTICE).run()
