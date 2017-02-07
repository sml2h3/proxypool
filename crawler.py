# -*-coding:utf-8 -*-
from config import *
import requests
from logger import Logger

class Crawler(object):
    def __init__(self):
        self.proxylist = []
        self.logger = Logger('crawler.py')

    def run(self):
        self.targetList = TARGET_CONFIG
        return self.crwaler()

    def crwaler(self):
        for api in TARGET_CONFIG:
            r = requests.get(api,timeout=20)
            if r.status_code == 200 and 'Error' not in r.text:
                proxytext = r.text
                tmp = proxytext.split("\r\n")
                if len(tmp)>0:
                    #合并去重复
                    self.proxylist = list(set(self.proxylist+tmp))
        self.logger.info("通过API获取的proxy的数目为"+str(len(self.proxylist)))
        return self.proxylist

if __name__ == '__main__':
    print Crawler().run()


