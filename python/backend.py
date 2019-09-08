#!/usr/bin/env python3

"""
Python backend program that connects with a web-based frontend and with a database.

Semi-RESTful API.

Test URL http://localhost:8086/user/create/?val=key&val2=key2

"""

# Imports
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import StringIO
from urllib.parse import urlparse

hostName = ""
hostPort = 8086

def queryDictionary( queryString:str):
    thisDict = {}
    for p in queryString.split('&'):
        ps = p.split('=')
        thisDict[ps[0]] = ps[1]
    return thisDict

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'<html><head><title>Sharzo</title></head><body><h1>Sharzo</h1>')

        self.wfile.write(b'<br>Request Path: ')
        self.wfile.write(bytes(self.path, 'utf-8'))

        self.wfile.write(b'<br><h2>Url Parse</h2><br>')
        o = urlparse(self.path)
        self.wfile.write(b'Parse Path: ')
        self.wfile.write(bytes(o.path, 'utf-8'))
        self.wfile.write(b'<br>Parse Params: ')
        self.wfile.write(bytes(str(o.params), 'utf-8'))
        self.wfile.write(b'<br>Parse Queries: ')
        self.wfile.write(bytes(str(o.query), 'utf-8'))

        self.wfile.write(b'<br>"User" in uri: ')
        if("user" in self.path):
            self.wfile.write(b'Yes')
        else:
            self.wfile.write(b'No')

        self.wfile.write(b'<br>Value for query item "val": ')
        queries = queryDictionary(str(o.query))
        self.wfile.write(bytes(queries['val'], 'utf-8'))

        self.wfile.write(b'</body></html>')

        
        
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = StringIO()
        response.write(b'This is the POST request. ')
        response.write(b'Received: ')
        response.write(body)
        self.wfile.write(response.getvalue())

httpd = HTTPServer((hostName, hostPort), SimpleHTTPRequestHandler)
print("Press ctrl+c to stop server.")
httpd.serve_forever()