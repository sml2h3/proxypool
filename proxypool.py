# -*-coding:utf-8 -*-
from gevent import monkey
monkey.patch_all()
from logger import Logger
from crawler import Crawler
from validator import Validator
import sqlite3
from server import Server
from config import *
import requests
import threading
logger = Logger('proxypool')
import time as systime
import datetime


class Proxypool:
    def __init__(self):
        self.crawler = Crawler()
        self.validator = Validator()
        self.proxyList = []

    def _master(self):
        #代理池中央控制
        while True:
            self.sqlite = sqlite3.connect(DB_CONFIG['SQLITE'])
            self._update(PROXYPOOL_CONFIG['UPDATE_TIME'])
            self._delete(PROXYPOOL_CONFIG['DELETE_TIME'])
            self._crawl(PROXYPOOL_CONFIG['CRAWL_TIME'])
            logger.info('System going to wait for next begin')
            systime.sleep(PROXYPOOL_CONFIG['SLEEP_TIME'])

    def _update(self, time):
        #重新验证IP列表
        logger.info('Update proxy begining')
        query = "SELECT ip FROM proxy WHERE updatetime<'%s'" % (
            (datetime.datetime.now() - datetime.timedelta(minutes=time)).strftime('%Y-%m-%d %H:%M:%S'))
        result = self.sqlite.execute(query).fetchall()
        proxieslist = [ip[0] for ip in result]
        result = self.validator.run(proxieslist)
        valid_success = [val[0] for val in result]
        valid_fail = [(val,) for val in proxieslist if val not in valid_success]
        query = "DELETE FROM proxy WHERE ip = ?"
        self.sqlite.executemany(query, valid_fail)
        self.sqlite.commit()
        logger.info("Update proxy end，本次共更新合格代理" + str(len(valid_success)-1) + "个,删除不合格代理"+str(len(valid_fail)-1)+"个")
        return

    def _delete(self,time):
        #删除过期IP
        logger.info("delete expired proxy beginning")
        query = "DELETE FROM proxy WHERE updatetime<'%s'" % (
            (datetime.datetime.now() - datetime.timedelta(minutes=time)).strftime('%Y-%m-%d %H:%M:%S'))
        self.sqlite.execute(query)
        self.sqlite.commit()
        logger.info("delete expired proxy end")
        return

    def _crawl(self, time):
        #爬取系统
        query = "SELECT COUNT(*) FROM proxy WHERE updatetime>'%s'" % \
                ((datetime.datetime.now() - datetime.timedelta(minutes=time)).strftime('%Y-%m-%d %H:%M:%S'))
        count = self.sqlite.execute(query).fetchone()[0]
        query2 = "SELECT COUNT(*) FROM proxy"
        countall = self.sqlite.execute(query2).fetchone()[0]
        logger.info("当前数据库proxy总量为" + countall)
        if count < PROXYPOOL_CONFIG['MIN_IP_NUM']:
            logger.info("Crawl Beginning")
            self.proxyList = self.crawler.run()
            logger.info('Crawl proxy end')
            logger.info('Validate proxy begin')
            result = self.validator.run(self.proxyList)
            logger.info("Validate proxy end，本次共抓取到合格代理" + str(len(result)) + "个")
            if DB_CONFIG['SQLITE']:
                self.save2sqlite(result)
            systime.sleep(3)
            self._crawl(time)
        else:
            return

    def save2sqlite(self,proxylist):
        query = "INSERT INTO proxy (ip,proctl,updatetime) VALUES (? , ? , ?)"
        for proxy in proxylist:
            try:
                self.sqlite.execute(query, proxy)
            except Exception as e:
                continue
        self.sqlite.commit()



    def _api(self):
        #对外提供Api接口
        Server(API_CONFIG['PORT'])
        return

    def run(self):
        t1 = threading.Thread(target=self._api)
        t2 = threading.Thread(target=self._master)
        t1.start()
        t2.start()


if __name__ == '__main__':
    Proxypool().run()


