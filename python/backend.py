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
database_connection = None

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
        queries = queryDictionary(str(parsedURL.query))
        if("favicon" in parsedURL.path):
            self.end_headers()
            self.send_response(204)
        elif("user" in parsedURL.path):
            strOut = ""
            if ("get" in parsedURL.path):
                user = bsql.get_user(database_connection, queries["uid"])
                strOut = "uID=" + str(user[0])
                strOut += "\nusername=" + user[1]
                strOut += "\nemail=" + user[2]
                strOut += "\npassword=" + user[3]
            elif ("create" in parsedURL.path):
                user = (queries["username"],queries["email"], queries["password"])
                uid = bsql.create_user(database_connection, user)
                strOut = str(uid)
            elif ("delete" in parsedURL.path):
                bsql.delete_user(database_connection, queries["uid"])
            elif ("login" in parsedURL.path):
                strOut = bsql.try_login(database_connection, queries["username"], queries["password"])
            self.send_response(200)
            self.end_headers()
            strOut = strOut.encode('utf-8')
            self.wfile.write(strOut)
        elif("friendrequests" in parsedURL.path):
            strOut = ""
            if ("get" in parsedURL.path):
                friend_request = bsql.get_friend_request(database_connection, queries["uid"])
                strOut = str(friend_request)
            elif ("accept" in parsedURL.path):
                friend_request = bsql.get_friend_request(database_connection, queries["frid"])
                friends = (friend_request[1],friend_request[2])
                bsql.create_friend_junction(database_connection, friends)
                bsql.delete_request_friend(database_connection, queries["frid"])
            elif("decline" in parsedURL.path):
                friend_request = bsql.delete_request_friend(database_connection, queries["frid"])
            self.send_response(200)
            self.end_headers()
            strOut = strOut.encode('utf-8')
            self.wfile.write(strOut)
        elif("friends" in parsedURL.path):
            strOut = ""
            if("get" in parsedURL.path):
                friends = bsql.get_friend_junction_by_userid(database_connection, queries["uid"])
                for friend in friends:
                    strOut += "\n"
                    strOut += str(friend)
            elif("delete" in parsedURL.path):
                friends = bsql.delete_friend(database_connection, queries["uid"], queries["frid"])
            self.send_response(200)
            self.end_headers()
            strOut = strOut.encode('utf-8')
            self.wfile.write(strOut)
        elif("loanrequest" in parsedURL.path):
            strOut = ""
            if("get" in parsedURL.path):
                request = bsql.get_loan_request_by_uid(database_connection, queries["uid"])
                for item in request:
                    strOut += "\n"
                    strOut += str(item)
            elif("accept" in parsedURL.path):
                bsql.update_media_status(database_connection, 'True', queries["rmid"])
                bsql.delete_request_media(database_connection, queries["rmid"])
            elif("decline" in parsedURL.path):
                bsql.delete_request_media(database_connection, queries["rmid"])
            self.send_response(200)
            self.end_headers()
            strOut = strOut.encode('utf-8')
            self.wfile.write(strOut)
        elif("collections" in parsedURL.path):
            strOut = ""
            if("get" in parsedURL.path):
                if "uid" in queries.keys():
                    return_value = bsql.select_collection_by_username(database_connection, queries["uid"])
                elif "cid" in queries.keys():
                    return_value = bsql.select_collection_by_collection(database_connection, queries["cid"])
                for i in return_value[0]:
                    strOut += '\n'
                    strOut += str(i)
            elif ("create" in parsedURL.path):
                cid = bsql.create_collection(database_connection, (queries["uid"],queries["name"]))
                strOut = str(cid)
            elif("delete" in parsedURL.path):
                bsql.delete_collection(database_connection, queries["cid"])
            self.send_response(200)
            self.end_headers()
            strOut = strOut.encode('utf-8')
            self.wfile.write(strOut)
        elif("media" in parsedURL.path):
            strOut = ""
            if("get" in parsedURL.path):
                if "mid" in queries.keys():
                    return_value = bsql.get_media_by_mid(database_connection, queries["mid"])
                elif "cid" in queries.keys():
                    return_value = bsql.get_media_by_cid(database_connection, queries["cid"])
                elif "uid" in queries.keys():
                    if len(queries.keys()) == 1:
                        return_value = bsql.get_media_by_uid(database_connection, queries["uid"])
                    elif queries["onloan"] == "true":
                        return_value = bsql.get_media_by_uid_if_loaned(database_connection, queries["uid"])
                    elif queries["onloan"] == "false":
                        return_value = bsql.get_media_by_uid_if_not_loaned(database_connection, queries["uid"])
                for i in return_value[0]:
                    strOut += '\n'
                    strOut += str(i)
            elif("create" in parsedURL.path):
                print(queries)
                mid = bsql.create_media(database_connection, queries["ownerid"], queries["mediatype"], queries["filename"])
                strOut = str(mid)
            elif("delete" in parsedURL.path):
                bsql.delete_media(database_connection, queries["mid"])
            self.send_response(200)
            self.end_headers()
            strOut = strOut.encode('utf-8')
            self.wfile.write(strOut)
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
    database_connection = bsql.create_connection()
    print(database_connection)
    bsql.sql_fetch_tables(database_connection)        
    httpd = HTTPServer((hostName, hostPort), SimpleHTTPRequestHandler)
    print("Press ctrl+c to stop server.")
    httpd.serve_forever()
    bsql.close_connection(database_connection)
