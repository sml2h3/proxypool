# coding:utf-8

HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2693.2 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate',
}

#api数组，支持多个api一起获取代理
TARGET_CONFIG = [
    'http://api.com/?tip=xxxxx&num=2222'
]


PROXYPOOL_CONFIG = {
    'MIN_IP_NUM': 500,  # 代理池中最小可用ip数量，若检测到小于此数量，启动爬虫
    'DELETE_TIME': 10,  # minutes, 删除更新时间在该时间之前的ip
    'SLEEP_TIME': 30,  # second, 两次爬取间隔
    'UPDATE_TIME': 0,   #minutes, 重新眼验证在这次执行前x分钟的代理
    'CRAWL_TIME': 30,  # minutes, 计算可用ip数量时, 取距当前多少分钟内验证过的ip
}

VALIDATE_CONFIG = {
    'THREAD_NUM': 1000,
    'TIMEOUT': 5,
    'PROXY_TYPE': [0, 1],# 0 为http，1为https
    'HTTP_TARGET': 'http://www.ip138.com/',
    'HTTPS_TARGET': 'https://www.baidu.com'
}

DB_CONFIG = {
    'SQLITE': './data/proxy.db'
}

API_CONFIG = {
    'PORT': 8082
}