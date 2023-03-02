# -*- coding: utf-8 -*-


__author__ = 'shaw'

from apscheduler.schedulers.blocking import BlockingScheduler

from const import tgcwZhaobiaoConst
from handler.configHandler import ConfigHandler
from spider.tgcwZhaobiaoSpider import TgcwZhaobiaoSpider
from util import commonUtil

conf = ConfigHandler()
timezone = 'Asia/Shanghai'
trigger = 'cron'


def run_scheduler():
    scheduler = BlockingScheduler()

    extra = commonUtil.cron_2_trigger(conf.tgcw_zhaobiao_cron[tgcwZhaobiaoConst.ID_XMGG])
    scheduler.add_job(TgcwZhaobiaoSpider(tgcwZhaobiaoConst.XMGG).run, id=tgcwZhaobiaoConst.ID_XMGG,
                      name='天工e招 招标公告', timezone=timezone, trigger=trigger, **extra)

    extra = commonUtil.cron_2_trigger(conf.tgcw_zhaobiao_cron[tgcwZhaobiaoConst.ID_BIDZBGS])
    scheduler.add_job(TgcwZhaobiaoSpider(tgcwZhaobiaoConst.BIDZBGS).run, id=tgcwZhaobiaoConst.ID_BIDZBGS,
                      name='天工e招 中标候选人公示', timezone=timezone, trigger=trigger, **extra)

    extra = commonUtil.cron_2_trigger(conf.tgcw_zhaobiao_cron[tgcwZhaobiaoConst.ID_BIDZBGG])
    scheduler.add_job(TgcwZhaobiaoSpider(tgcwZhaobiaoConst.BIDZBGG).run, id=tgcwZhaobiaoConst.ID_BIDZBGG,
                      name='天工e招 中标结果公告', timezone=timezone, trigger=trigger, **extra)

    scheduler.start()
