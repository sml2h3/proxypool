# -*-coding:utf-8 -*-
from gevent import monkey
monkey.patch_all()
from config import *
import requests
from logger import Logger
from crawler import Crawler
from gevent.pool import Pool
import datetime


class Validator(object):
    def __init__(self):
        self.logger = Logger('validator.py')
        self.valid_cfg = VALIDATE_CONFIG
        self.result = []
        self.proxies = {}

    def run(self, proxylist):
        if len(proxylist) == 0:
            return []
        pool = Pool(VALIDATE_CONFIG['THREAD_NUM'])
        self.result = filter(lambda x: x, pool.map(self.valid, proxylist))
        return self.result

    def valid(self, proxy):
        self.proxies = {
            'http': 'http://' + proxy,
            'https': 'http://' + proxy
        }
        isval = 0
        try:
            r = requests.get(self.valid_cfg['HTTP_TARGET'],proxies=self.proxies,timeout=self.valid_cfg['TIMEOUT'])
        except Exception as e:
            return
        if r.status_code == 200 and '1212.ip138.com/ic.asp' in r.text:
            isval = 1
            try:
                r2 = requests.get(self.valid_cfg['HTTPS_TARGET'], proxies=self.proxies, timeout=self.valid_cfg['TIMEOUT'])
                if r2.status_code == 200 and 'www.baidu.com/more/' in r2.text:
                    tmp = (proxy, 'https', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                else:
                    tmp = (proxy, 'http', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            except Exception as e:
                tmp = (proxy, 'http', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            return tmp

if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding("utf-8")
    result = crawler = Crawler().run()
    print result
    print Validator().run(result)




