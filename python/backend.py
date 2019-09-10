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
    sql = 'INSERT INTO Media(FileType, MediaType, FileName, FileLocation, OwnerID, LoanerID, LoanReturnTime,IsBeingLoaned) VALUES(?,?,?,?,?,?,?,?)'
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
    sql = 'INSERT INTO FriendsJunction(Person1ID,Person2ID) VALUES(?,?)'
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


def delete_user(connection, id):
    """
    Delete a user with a given id

    :param connection: The active connection to the database.
    :param id: The user's id to be deleted.
    """
    sql = 'DELETE from Users WHERE uID=?'
    cursor = connection.cursor()
    cursor.execute(sql, id)
    connection.commit()


def delete_request_friend(connection, id):
    """
    Delete a friend request with a given id

    :param connection: The active connection to the database.
    :param id: The friend request's id to be deleted.
    """
    sql = 'DELETE from RequestFriend WHERE rfID=?'
    cursor = connection.cursor()
    cursor.execute(sql, id)
    connection.commit()


def delete_friend_junction(connection, id):
    """
    Delete a friend junction with a given id

    :param connection: The active connection to the database.
    :param id: The friend junction's id to be deleted.
    """
    sql = 'DELETE from FriendsJunction WHERE fjID=?'
    cursor = connection.cursor()
    cursor.execute(sql, id)
    connection.commit()


def delete_collection(connection, id):
    """
    Delete a collection with a given id

    :param connection: The active connection to the database.
    :param id: The collection's id to be deleted.
    """
    sql = 'DELETE from Collection WHERE cID=?'
    cursor = connection.cursor()
    cursor.execute(sql, id)
    connection.commit()


def delete_request_media(connection, id):
    """
    Delete a request media with a given id

    :param connection: The active connection to the database.
    :param id: The media request's id to be deleted.
    """
    sql = 'DELETE from RequestMedia WHERE rmID=?'
    cursor = connection.cursor()
    cursor.execute(sql, id)
    connection.commit()


def delete_media(connection, id):
    """
    Delete a media with a given id

    :param connection: The active connection to the database.
    :param id: The media's id to be deleted.
    """
    sql = 'DELETE from Media WHERE mID=?'
    cursor = connection.cursor()
    cursor.execute(sql, id)
    connection.commit()


def delete_media_connection_junction(connection, id):
    """
    Delete a media connection junction with a given id

    :param connection: The active connection to the database.
    :param id: The media connection junction's id to be deleted.
    """
    sql = 'DELETE from MediaCollectionJunction WHERE mcjID=?'
    cursor = connection.cursor()
    cursor.execute(sql, id)
    connection.commit()


def clear_users(connection):
    """
    Delete all rows in the user table
    "param connection" Active connection to a sqlite db
    """

    sql = 'DELETE FROM Users'
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()


def clear_media(connection):
    """
    Delete all rows in the media table
    "param connection" Active connection to a sqlite db
    """

    sql = 'DELETE FROM Media'
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()


def clear_media_collection_junction(connection):
    """
    Delete all rows in the media collection junction table
    "param connection" Active connection to a sqlite db
    """

    sql = 'DELETE FROM MediaCollectionJunction'
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()


def clear_collection(connection):
    """
    Delete all rows in the collection table
    "param connection" Active connection to a sqlite db
    """

    sql = 'DELETE FROM Collection'
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()


def clear_request_media(connection):
    """
    Delete all rows in the RequestMedia table
    "param connection" Active connection to a sqlite db
    """

    sql = 'DELETE FROM RequestMedia'
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()


def clear_request_friend(connection):
    """
    Delete all rows in the RequestFriend table
    "param connection" Active connection to a sqlite db
    """

    sql = 'DELETE FROM RequestFriend'
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()


def clear_friend_junction(connection):
    """
    Delete all rows in the FriendJunction table
    "param connection" Active connection to a sqlite db
    """

    sql = 'DELETE FROM FriendsJunction'
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()


def update_user(connection, user):
    """
    update a username, email address, or password for a user
    :param connection: active connection to a sqlite db
    :param user: a list of user information to store in the database
    """
    sql = ''' UPDATE Users 
              SET Username = ? , 
                  Email = ? , 
                  Password = ? 
              WHERE uID = ?'''
    cursor = connection.cursor()
    cursor.execute(sql,user)
    connection.commit()


def update_media(connection, media):
    """
    update a FileType, Media Type, File Name, File Location, Owner ID, Loaner ID, Loan Return Time, or Is Being Loaned for a media item
    :param connection: active connection to a sqlite db
    :param media: a list of media information to store in the database
    """
    sql = ''' UPDATE Media 
              SET FileType = ? , 
                  MediaType = ? , 
                  FileName = ? ,
                  FileLocation = ?,
                  OwnerID = ? ,
                  LoanerID = ? ,
                  LoanReturnTime = ? ,
                  IsBeingLoaned = ?
              WHERE mID = ?'''
    cursor = connection.cursor()
    cursor.execute(sql,media)
    connection.commit()


def update_collection(connection, collection):
    """
    update a OwnerID, Date Created, or Collection Name for a collection
    :param connection: active connection to a sqlite db
    :param collection: a list of collection information to store in the database
    """
    sql = ''' UPDATE Collection 
              SET OwnerID = ? , 
                  DateCreated = ? , 
                  CollectionName = ? 
              WHERE cID = ?'''
    cursor = connection.cursor()
    cursor.execute(sql,collection)
    connection.commit()


def update_request_media(connection, media_request):
    """
    update a Requested Loan Time, MediaID, FromID, or ToID for a media request
    :param connection: active connection to a sqlite db
    :param media_request: a list of media request's information to store in the database
    """
    sql = ''' UPDATE RequestMedia 
              SET RequestedLoanTime = ? , 
                  MediaID = ? , 
                  FromID = ? ,
                  ToID = ?
              WHERE rmID = ?'''
    cursor = connection.cursor()
    cursor.execute(sql,media_request)
    connection.commit()


def update_request_friend(connection, friend_request):
    """
    update a FromID and a ToID for a friend request
    :param connection: active connection to a sqlite db
    :param friend_request: a list of friend_request information to store in the database
    """
    sql = ''' UPDATE RequestFriend 
              SET FromID = ? , 
                  ToID = ? 
              WHERE rfID = ?'''
    cursor = connection.cursor()
    cursor.execute(sql,friend_request)
    connection.commit()


def update_friend_junction(connection, friends_junction):
    """
    update a Person1ID and a Person2ID for a friend request
    :param connection: active connection to a sqlite db
    :param friends_junction: a list of friends junction information to store in the database
    """
    sql = ''' UPDATE FriendsJunction 
              SET Person1ID = ? , 
                  Person2ID = ? 
              WHERE fjID = ?'''
    cursor = connection.cursor()
    cursor.execute(sql,friends_junction)
    connection.commit()


def update_media_collection_junction(connection, media_collection_junction):
    """
    update a MediaID and a CollectionID for a media collection junction request
    :param connection: active connection to a sqlite db
    :param media_collection_junction: a list of media collection junction information to store in the database
    """
    sql = ''' UPDATE MediaCollectionJunction 
              SET MediaID = ? , 
                  CollectionID = ? 
              WHERE mcjID = ?'''
    cursor = connection.cursor()
    cursor.execute(sql,media_collection_junction)
    connection.commit()


def sql_fetch_tables(connection):
    """
    Debugging method to display all tables in the database.

    :param connection: The opened connection to the database to show its tables.
    """
    cursor = connection.cursor()
    cursor.execute('SELECT name from sqlite_master where type= "table"')
    print(cursor.fetchall())


def select_users(connection):
    """
    Method to display the user table's contents

    :param connection: Opened connection to the database
    """
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Users')
    rows = cursor.fetchall()
    for row in rows:
        print(row)


def select_media(connection):
    """
    Method to display the media table's contents

    :param connection: Opened connection to the database
    """
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Media')
    rows = cursor.fetchall()
    for row in rows:
        print(row)


def select_request_friend(connection):
    """
    Method to display the RequestFriend table's contents

    :param connection: Opened connection to the database
    """
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM RequestFriend')
    rows = cursor.fetchall()
    for row in rows:
        print(row)


def select_friends_junction(connection):
    """
    Method to display the FriendsJunction table's contents

    :param connection: Opened connection to the database
    """
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM FriendsJunction')
    rows = cursor.fetchall()
    for row in rows:
        print(row)


def select_collection(connection):
    """
    Method to display the collection table's contents

    :param connection: Opened connection to the database
    """
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Collection')
    rows = cursor.fetchall()
    for row in rows:
        print(row)


def select_request_media(connection):
    """
    Method to display the RequestMedia table's contents

    :param connection: Opened connection to the database
    """
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM RequestMedia')
    rows = cursor.fetchall()
    for row in rows:
        print(row)


def select_media_collection_junction(connection):
    """
    Method to display the MediaCollectionJunction table's contents

    :param connection: Opened connection to the database
    """
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM MediaCollectionJunction')
    rows = cursor.fetchall()
    for row in rows:
        print(row)


def select_user_by_username(connection, username):
    """
    Query users by username -- sample of how to do this
    :param connection: active connection to the sqlite db
    :param username: the username that is being queried for
    """
    sql = 'SELECT * FROM Users WHERE Username = ?'
    cursor = connection.cursor(sql, username)

    rows = cursor.fetchall()

    for row in rows:
        print(row)


def close_connection(connection):
    """
    Make sure that the database connection is closed at the end.
    """

    if connection:
        connection.close()
        print("Database connection closed.")





if __name__ == '__main__':
    database_connection = create_connection(database_file_path)
    sql_fetch_tables(database_connection)
    sql_select_users(database_connection)
    if database_connection:
        print(database_connection)
        user = ("test", "test@a.com", "12345")
        media = ("jpg", "img", "Blah", "Over There", 2, 3, None, False)
        #result = create_user(database_connection, user)
        #result = create_media(database_connection, media)
        sql_select_users(database_connection)
        #delete_user(database_connection, ("17",))
        #update_user(database_connection, ("OIII", "l@l.org", "passwor2", 42,))
        #clear_users(database_connection)
        #clear_media(database_connection)
        #sql_fetch_all_users(database_connection)

        

    httpd = HTTPServer((hostName, hostPort), SimpleHTTPRequestHandler)
    print("Press ctrl+c to stop server.")
    httpd.serve_forever()
    close_connection(database_connection)
