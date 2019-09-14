#!/usr/bin/env python3

"""
Python backend program that connects to an SQLite database.

Semi-RESTful API.

Test URL http://localhost:8086/user/create/?val=key&val2=key2

"""

import sqlite3
from sqlite3 import Error

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


def create_media(connection, uid, media_type, file_name):
    sql = 'INSERT INTO Media(OwnerID, MediaType, FileName) VALUES(?,?,?)'
    cursor = connection.cursor()
    cursor.execute(sql,(uid,media_type,file_name))
    connection.commit()
    return cursor.lastrowid


def create_collection(connection, collection):
    """
    Create a new collection entry in the database

    :param connection: The active connection to the database.
    :param collection: The collection information to be stored in the database. 
                    Should be in a list in form (OwnerID, CollectionName)
    :return: the row id of the inserted value
    """
    sql = 'INSERT INTO Collection(OwnerId, CollectionName) VALUES(?,?)'
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
    :param friend_junction: The friend junction information to be stored in the database. 
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
    cursor.execute(sql, (id,))
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
    cursor.execute(sql, (id,))
    connection.commit()


def delete_collection(connection, id):
    """
    Delete a collection with a given id

    :param connection: The active connection to the database.
    :param id: The collection's id to be deleted.
    """
    sql = 'DELETE from Collection WHERE cID=?'
    cursor = connection.cursor()
    cursor.execute(sql, (id,))
    connection.commit()


def delete_request_media(connection, id):
    """
    Delete a request media with a given id

    :param connection: The active connection to the database.
    :param id: The media request's id to be deleted.
    """
    sql = 'DELETE from RequestMedia WHERE rmID=?'
    cursor = connection.cursor()
    cursor.execute(sql, (id,))
    connection.commit()


def delete_media(connection, id):
    """
    Delete a media with a given id

    :param connection: The active connection to the database.
    :param id: The media's id to be deleted.
    """
    sql = 'DELETE from Media WHERE mID=?'
    cursor = connection.cursor()
    cursor.execute(sql, (id,))
    connection.commit()


def delete_media_connection_junction(connection, id):
    """
    Delete a media connection junction with a given id

    :param connection: The active connection to the database.
    :param id: The media connection junction's id to be deleted.
    """
    sql = 'DELETE from MediaCollectionJunction WHERE mcjID=?'
    cursor = connection.cursor()
    cursor.execute(sql, (id,))
    connection.commit()


def delete_friend(connection, uid, friendid):
    sql = "DELETE from FriendsJunction WHERE Person1ID=? AND Person2ID=?"
    cursor = connection.cursor()
    cursor.execute(sql,(uid, friendid))
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


def update_media_status(connection, new_value, rmid):
    sql_get = "SELECT MediaID FROM RequestMedia WHERE rmID=?"
    sql = 'UPDATE Media SET IsBeingLoaned=? WHERE mID=?'
    cursor = connection.cursor()
    cursor.execute(sql_get,(rmid,))
    mid = cursor.fetchall()
    if mid:    
        cursor.execute(sql,(new_value,mid[0][0]))
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
        
        
def get_user(connection, uid):
    """
    Method to retrieve a user by id
    
    :param connection: Opened connection to the database
    :param uid: the user's id that is being retrieved
    :return: the row that matches a given ID
    """
    sql = 'SELECT * FROM Users WHERE uID=?'
    cursor = connection.cursor()
    cursor.execute(sql, (uid,))
    rows = cursor.fetchall() # rows is a list that contains the user's row from the database table    
    return rows[0]


def get_media_by_mid(connection, mid):
    sql = 'SELECT * FROM Media WHERE mID=?'
    cursor = connection.cursor()
    cursor.execute(sql, (mid,))
    rows = cursor.fetchall()
    return rows


def get_media_by_cid(connection, cID):
    sql_prepare = "SELECT MediaID FROM MediaCollectionJunction WHERE CollectionID=?"
    sql = 'SELECT * FROM Media WHERE mID=?'
    cursor = connection.cursor()
    cursor.execute(sql_prepare, (cID,))
    mid = cursor.fetchall()[0][0]
    
    cursor.execute(sql, (mid,))
    rows = cursor.fetchall()
    return rows


def get_media_by_uid(connection, uid):
    sql = 'SELECT * FROM Media WHERE OwnerID=?'
    cursor = connection.cursor()
    cursor.execute(sql, (uid,))
    rows = cursor.fetchall()
    return rows


def get_media_by_uid_if_loaned(connection, uid):
    sql = 'SELECT * FROM Media WHERE OwnerID=? AND IsBeingLoaned=TRUE'
    cursor = connection.cursor()
    cursor.execute(sql, (uid,))
    rows = cursor.fetchall()
    return rows


def get_media_by_uid_if_not_loaned(connection, uid):
    sql = 'SELECT * FROM Media WHERE OwnerID=? AND IsBeingLoaned=FALSE'
    cursor = connection.cursor()
    cursor.execute(sql, (uid,))
    rows = cursor.fetchall()
    return rows


def get_friend_request(connection, rfID):
    """
    Method to retrieve a friend request by id
    
    :param connection: Opened connection to the database
    :param rfID: the friend request id to be retrieved
    :return: the row that matches the given ID
    """
    sql = 'SELECT * FROM RequestFriend WHERE rfID=?'
    cursor = connection.cursor()
    cursor.execute(sql, (rfID,))
    rows = cursor.fetchall()
    return rows[0]


def get_friend_junction_by_userid(connection, uid):
    sql = 'SELECT * FROM FriendsJunction WHERE Person1ID=?'
    cursor = connection.cursor()
    cursor.execute(sql, (uid,))
    rows = cursor.fetchall()
    return rows


def get_loan_request_by_uid(connection, uid):
    sql = 'SELECT * FROM RequestMedia WHERE FromID=?'
    cursor = connection.cursor()
    cursor.execute(sql, (uid,))
    rows = cursor.fetchall()
    return rows


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


def select_collection_by_username(connection, username):
    sql = 'SELECT * FROM Collection WHERE OwnerID=?'
    cursor = connection.cursor()
    cursor.execute(sql, (username,))
    rows = cursor.fetchall()
    return rows


def select_collection_by_collection(connection, cid):
    sql = 'SELECT * FROM Collection WHERE cID=?'
    cursor = connection.cursor()
    cursor.execute(sql, (cid,))
    rows = cursor.fetchall()
    return rows


def try_login(connection, username, password):
    """
    Attempt to login based on a username and passworddatetime A combination of a date and a time. Attributes: ()
    :param connection: active connection to the sqlite db
    :param username: the username to match the password too
    :param password: the password to attempt to match to the password stored in the database.
    """
    sql = 'SELECT uID FROM Users WHERE username=? AND password=?'
    cursor = connection.cursor()
    cursor.execute(sql,(username, password))
    uID = cursor.fetchall()
    if uID:
        return str(uID[0][0])
    else:
        return "no"


def close_connection(connection):
    """
    Make sure that the database connection is closed at the end.
    """

    if connection:
        connection.close()
        print("Database connection closed.")
