# -*- coding: utf-8 -*-


__author__ = 'shaw'

from handler.configHandler import ConfigHandler
from handler.logHandler import LogHandler


log = LogHandler('launcher')
conf = ConfigHandler()


def __show_configure():
    log.info('')
    log.info('======================= request ==============================')
    log.info('REQUEST_RETRY_TIME    : %s', conf.request_retry_time)
    log.info('REQUEST_RETRY_INTERVAL: %s', conf.request_retry_interval)
    log.info('REQUEST_TIMEOUT       : %s', conf.request_timeout)
    log.info('NEED_PROXY            : %s', conf.need_proxy)
    log.info('PROXY_POOL_URL        : %s', conf.proxy_pool_url)
    log.info('INTERVAL_DAYS         : %s', conf.interval_days)
    log.info('MAX_THREAD            : %s', conf.max_thread)
    log.info('')
    log.info('=============== database ==============================')
    log.info('MYSQL_HOSTNAME: %s', conf.mysql_hostname)
    log.info('MYSQL_PORT    : %s', conf.mysql_port)
    log.info('MYSQL_USERNAME: %s', conf.mysql_username)
    log.info('MYSQL_PASSWORD: %s', conf.mysql_password)
    log.info('MYSQL_SCHEMA  : %s', conf.mysql_schema)
    log.info('')
    log.info('================= log ==============================')
    log.info('LOG_LEVEL       : %s', conf.log_level)
    log.info('LOG_BACKUP_COUNT: %s', conf.log_backup_count)
    log.info('')
    log.info('=========================== cron ==============================')
    log.info('TGCW_ZHAOBIAO_XMGG_CRON   : %s', conf.tgcw_zhaobiao_cron[0])
    log.info('TGCW_ZHAOBIAO_BIDZBGS_CRON: %s', conf.tgcw_zhaobiao_cron[1])
    log.info('TGCW_ZHAOBIAO_BIDZBGG_CRON: %s', conf.tgcw_zhaobiao_cron[2])
    log.info('EBNEW_CRON                : %s', conf.ebnew_cron)
    log.info('JTSWW_BIDDING_NOTICE_CRON : %s', conf.jtsww_cron[0])
    log.info('JTSWW_CANDIDATEAN_NO_CRON : %s', conf.jtsww_cron[1])
    log.info('JTSWW_WIN_NOTICE_CRON     : %s', conf.jtsww_cron[2])
    log.info('')


def start_scheduler():
    __show_configure()
    from helper.scheduler import run_scheduler

    run_scheduler()


if __name__ == '__main__':
    start_scheduler()
