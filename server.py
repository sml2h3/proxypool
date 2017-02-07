# -*-coding:utf-8 -*-
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import sqlite3
from config import *
from logger import Logger
from urlparse import urlparse, parse_qs


class Server(object):
    def __init__(self,PORT):
        self.port = PORT
        self.logger = Logger('server.py')
        self.run()

    def run(self):
        http_server = HTTPServer(('localhost', self.port), self.ProxyPoolHandle)
        self.logger.info('listened on localhost:%s' % self.port)
        http_server.serve_forever()

    class ProxyPoolHandle(BaseHTTPRequestHandler):
        def __init__(self, request, client_address, server):
            self.sqlite = sqlite3.connect(DB_CONFIG['SQLITE'])
            self.table_name = 'proxy'
            BaseHTTPRequestHandler.__init__(self, request, client_address, server)

        def do_GET(self):
            if '/favicon.ico' in self.path:
                return
            params = parse_qs(urlparse(self.path).query)
            data = self.get_data(params)
            self.protocal_version = "HTTP / 1.1"
            self.send_response(200)
            self.send_header("Welcome", "Contect")
            self.end_headers()
            self.wfile.write(data)

        def get_data(self,params):
            query = {
                'num': '100',
                'proctl': 'http',
            }
            if params:
                for (k, v) in params.items():
                    try:
                        k = k.lower()
                        if k == 'num':
                            query['num'] = v[0]
                        elif k == 'proctl':
                            query['proctl'] = v[0]
                        else:
                            continue
                    except:
                        continue
            querystr = "SELECT ip FROM proxy WHERE proctl = '%s'" % \
                    (query['proctl'])
            resultobject = self.sqlite.execute(querystr)
            result = ''
            for i in range(0, int(query['num'])):
                try:
                    result = result + resultobject.fetchone()[0] + "\r\n"
                except Exception:
                    continue
            return result
