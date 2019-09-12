#!/usr/bin/env python3

"""
Python backend program that dispatches GET requests.

Semi-RESTful API.

Test URL http://localhost:8086/user/create/?val=key&val2=key2

"""

# Imports
import sqlite3
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import StringIO
from sqlite3 import Error
from urllib.parse import urlparse
import backend_sql as bsql

hostName = ""
hostPort = 8086

def queryDictionary( queryString:str):
    thisDict = {}
    for p in queryString.split('&'):
        if(p is ''): break # If no parameters were requested, just skip
        ps = p.split('=')
        key = ps[0]
        val = ps[1]
        thisDict[key] = val
    return thisDict

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def end_headers (self):
        self.send_header('Access-Control-Allow-Origin', '*')
        BaseHTTPRequestHandler.end_headers(self)

    def do_GET(self):
        parsedURL = urlparse(self.path)
        #queries = queryDictionary(str(parsedURL.query))
        #self.wfile.write(bytes(queries['val'], 'utf-8'))

        if("favicon" in parsedURL.path):
            self.end_headers()
            self.send_response(204)
        elif("USER" in parsedURL.path):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"bob")
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"wat")

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


if __name__ == '__main__':
    database_connection = bsql.create_connection(bsql.database_file_path)
    bsql.sql_fetch_tables(database_connection)

    #sql_select_users(database_connection)

    if database_connection:
        print(database_connection)
        user = ("test", "test@a.com", "12345")
        media = ("jpg", "img", "Blah", "Over There", 2, 3, None, False)
        #result = create_user(database_connection, user)
        #result = create_media(database_connection, media)
        
        #sql_select_users(database_connection)
        
        #delete_user(database_connection, ("17",))
        #update_user(database_connection, ("OIII", "l@l.org", "passwor2", 42,))
        #clear_users(database_connection)
        #clear_media(database_connection)
        #sql_fetch_all_users(database_connection)

        

    httpd = HTTPServer((hostName, hostPort), SimpleHTTPRequestHandler)
    print("Press ctrl+c to stop server.")
    httpd.serve_forever()
    bsql.close_connection(database_connection)
