#!/usr/bin/env python3

"""
Python backend program that connects with a web-based frontend and with a database.
"""

# Imports
from http.server import HTTPServer, BaseHTTPRequestHandler

hostName = ""
hostPort = 80

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Hello, world!')
        
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'This is the POST request. ')
        response.write(b'Received: ')
        response.write(body)
        self.wfile.write(response.getvalue())

httpd = HTTPServer((hostName, hostPort), SimpleHTTPRequestHandler)
print("Press ctrl+c to stop server.")
httpd.serve_forever()