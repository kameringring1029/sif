#!/usr/bin/env python
#-*- coding:utf-8 -*-


from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import json

class MyHandler(SimpleHTTPRequestHandler):

    def do_GET(self):

        uri = self.path
        ret = parse_qs(urlparse(uri).query, keep_blank_values = True)

        if ('foo' in ret.keys()) and (ret['foo'][0] == 'bar'):
            ret = json.dumps({ 'msg': 'ok' })
        else:
            ret = json.dumps({ 'msg': 'failure' })

        body = bytes(ret, 'utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-length', len(body))
        self.end_headers()
        self.wfile.write(body)
		
host = 'localhost'
port = 8000
httpd = HTTPServer((host, port), MyHandler)
print('serving at port', port)
httpd.serve_forever()

