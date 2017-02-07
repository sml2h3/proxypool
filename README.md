# proxypool
土豪专用代理池，IP质量高，稳定，快，提供本地api
# 前言
翻遍了github，发现大部分线程池都是围绕着各大网站上提供的免费代理IP抓取验证，进库。
拜托，作为一个爬虫程序员连买代理IP的钱都没有，还是回家种田得了，像我这么土豪的，当然是要直接从外部网站api中提取代理啊！然后用自己的本地api提取裤子中的代理啊
# 用法
首先,你需要安转以下第三方库，并且python版本>=2.7
##安装依赖
```
sudo pip install requests
sudo pip install gevent
sudo pip install urlparse
```
##配置
然后打开配置文件config.py
###api列表
TARGET_CONFIG列表中支持多个api,如下
```[
  'api1',
  'api2'
]
```
###本地api端口
API_CONFIG中的PORT参数，默认8082
其余的根据注释配吧
##启动
```
python proxypool.py
```
##调取本地裤子中的proxy
默认本地api的端口为8082则api为：http://127.0.0.1:8082/?num=100&proctl=https
默认num为100，proctl为http
#作者
作者博客：https://www.fkgeek.com
本轮子地址：https://www.fkgeek.com/archives/42
作者邮箱：sml2h3@gmail.com
