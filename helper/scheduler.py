# -*- coding: utf-8 -*-


__author__ = 'shaw'

from apscheduler.schedulers.blocking import BlockingScheduler

from const import tgcwZhaobiaoConst as tgcw, ebnewConst as ebnew, jtswwConst as jtsww
from handler.configHandler import ConfigHandler
from spider.ebnewThread import EbnewThread
from spider.jtswwSpider import JtswwSpider
from spider.tgcwZhaobiaoSpider import TgcwZhaobiaoSpider
from util.commonUtil import cron_2_trigger


conf = ConfigHandler()


def run_ebnew_thread():
    """
    必联网 招标项目 多线程
    """
    for i in range(conf.max_thread):
        thread = EbnewThread(i, 'EbnewThread-' + str(i))
        thread.start()


def run_scheduler():
    scheduler = BlockingScheduler()

    # 天工e招
    for i in range(3):
        trigger = cron_2_trigger(conf.tgcw_zhaobiao_cron[i])
        scheduler.add_job(TgcwZhaobiaoSpider(tgcw.TYPES[i]).run, id=tgcw.IDS[i], **trigger)

    # 必联网
    trigger = cron_2_trigger(conf.ebnew_cron)
    scheduler.add_job(run_ebnew_thread, id=ebnew.NAME, **trigger)

    # 建投商务网
    for i in range(3):
        trigger = cron_2_trigger(conf.jtsww_cron[i])
        scheduler.add_job(JtswwSpider(jtsww.TYPES[i]).run, id=jtsww.IDS[i], **trigger)

    scheduler.start()
