#!/usr/bin/env python3

"""
Python backend program that connects with a web-based frontend and with a database.

Semi-RESTful API.

Test URL http://localhost:8086/user/create/?val=key&val2=key2

"""

# Imports
import sqlite3
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import StringIO
from sqlite3 import Error
from urllib.parse import urlparse

hostName = ""
hostPort = 8086
database_file_path = "./database/media.db"

def create_connection(database_file):
    """
        Create and connect to a SQLite database
        :param database_file: is a string that contains the path to the database.
        :return: A connection object or None
    """
    connection = None
    try:
        connection = sqlite3.connect(database_file)
    except Error as e:
        print(e)

    return connection


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


def create_user(connection, user):
    """
    Create a new user entry in the database

    :param connection: The active connection to the database.
    :param user: The user information to be stored in the database. 
                    Should be in a list in form (Username, Email, Password)
    :return: the row id of the inserted value
    """
    sql = 'INSERT INTO Users(Username,Email,Password) VALUES(?,?,?)'
    cursor = connection.cursor()
    cursor.execute(sql,user)
    connection.commit()
    return cursor.lastrowid


def create_media(connection, media_item):
    """
    Create a new media entry in the database

    :param connection: The active connection to the database.
    :param media_item: The media information to be stored in the database.
                          Should be in a list in form (File Type, Media Type, File Name, 
                          File Location, OwnerID,LoanerID,LoanReturnTime,IsBeingLoaded)
    :return: the row id of the inserted value
    """
    sql = 'INSERT INTO Media(FileType, MediaType, FileName, FileLocation, OwnerID, LoanerID,'+
            'LoanReturnTime,IsBeingLoaned) VALUES(?,?,?,?,?,?,?,?)'
    cursor = connection.cursor()
    cursor.execute(sql,media_item)
    connection.commit()
    return cursor.lastrowid


def create_collection(connection, collection):
    """
    Create a new collection entry in the database

    :param connection: The active connection to the database.
    :param collection: The collection information to be stored in the database. 
                    Should be in a list in form (OwnerID, DateCreated, CollectionName)
    :return: the row id of the inserted value
    """
    sql = 'INSERT INTO Collection(OwnerId, DateCreated, CollectionName) VALUES(?,?,?)'
    cursor = connection.cursor()
    cursor.execute(sql,collection)
    connection.commit()
    return cursor.lastrowid


def create_mcJunction(connection, mcJunction):
    """
    Create a new Media Collection Junction entry in the database

    :param connection: The active connection to the database.
    :param user: The media collection junction information to be stored in the database. 
                    Should be in a list in form (MediaID, CollectionID)
    :return: the row id of the inserted value
    """
    sql = 'INSERT INTO MediaCollectionJunction(MediaID,CollectionID) VALUES(?,?)'
    cursor = connection.cursor()
    cursor.execute(sql,mcJunction)
    connection.commit()
    return cursor.lastrowid


def create_friend_junction(connection, friend_junction):
    """
    Create a new Friend Junction entry in the database

    :param connection: The active connection to the database.
    :param user: The friend junction information to be stored in the database. 
                    Should be in a list in form (Person1ID, Person2ID)
    :return: the row id of the inserted value
    """
    sql = 'INSERT INTO FriendJunction(Person1ID,Person2ID) VALUES(?,?)'
    cursor = connection.cursor()
    cursor.execute(sql,friend_junction)
    connection.commit()
    return cursor.lastrowid


def create_request_friend(connection, request_friend):
    """
    Create a new request friend entry in the database

    :param connection: The active connection to the database.
    :param user: The friend request information to be stored in the database. 
                    Should be in a list in form (FromID, ToID)
    :return: the row id of the inserted value
    """
    sql = 'INSERT INTO RequestFriend(FromID,ToID) VALUES(?,?)'
    cursor = connection.cursor()
    cursor.execute(sql,request_friend)
    connection.commit()
    return cursor.lastrowid


def create_request_media(connection, media_request):
    """
    Create a new media request entry in the database

    :param connection: The active connection to the database.
    :param user: The media request information to be stored in the database. 
                    Should be in a list in form (RequestedLoanTime, MediaID, FromID, ToID)
    :return: the row id of the inserted value
    """
    sql = 'INSERT INTO RequestMedia(RequestedLoanTime,MediaID,FromID,ToID) VALUES(?,?,?)'
    cursor = connection.cursor()
    cursor.execute(sql,media_request)
    connection.commit()
    return cursor.lastrowid


def sql_fetch(con):
    cursor = con.cursor()
    cursor.execute('SELECT name from sqlite_master where type= "table"')
    print(cursor.fetchall())


def sql_fetchall(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Users')
    rows = cursor.fetchall()
    for row in rows:
        print(row)


def close_connection(conn):
    if conn:
        conn.close()
        print("Database connection closed.")





if __name__ == '__main__':
    database_connection = create_connection(database_file_path)
    sql_fetch(database_connection)
    sql_fetchall(database_connection)
    if database_connection:
        print(database_connection)
        user = ("test", "test@c.com", "12345")
        media = ("jpg", "img", "Blah", "Over There", 2, 3, None, False)
        result = create_user(database_connection, user)
        result = create_media(database_connection, media)
        

    httpd = HTTPServer((hostName, hostPort), SimpleHTTPRequestHandler)
    print("Press ctrl+c to stop server.")
    httpd.serve_forever()
    close_connection(database_connection)
