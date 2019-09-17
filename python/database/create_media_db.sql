BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Users" (
	"uID"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"Username"	STRING NOT NULL,
	"Email"	STRING NOT NULL,
	"Password"	STRING
);
CREATE TABLE IF NOT EXISTS "Collection" (
	"cID"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"OwnerID"	INTEGER,
	"DateCreated"	DATE,
	"CollectionName"	STRING,
	FOREIGN KEY("OwnerID") REFERENCES "Users"("uID")
);
CREATE TABLE IF NOT EXISTS "RequestMedia" (
	"rmID"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"RequestedLoanTime"	DATETIME,
	"FromID"	INTEGER,
	"ToID"	INTEGER,
	"MediaID"	INTEGER,
	FOREIGN KEY("ToID") REFERENCES "Users"("uID"),
	FOREIGN KEY("FromID") REFERENCES "Users"("uID"),
	FOREIGN KEY("MediaID") REFERENCES "Media"("mID")
);
CREATE TABLE IF NOT EXISTS "RequestFriend" (
	"rfID"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"FromID"	INTEGER,
	"ToID"	INTEGER,
	FOREIGN KEY("ToID") REFERENCES "Users"("uID"),
	FOREIGN KEY("FromID") REFERENCES "Users"("uID")
);
CREATE TABLE IF NOT EXISTS "FriendsJunction" (
	"fjID"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"Person1ID"	INTEGER,
	"Person2ID"	INTEGER,
	FOREIGN KEY("Person2ID") REFERENCES "Users"("uID"),
	FOREIGN KEY("Person1ID") REFERENCES "Users"("uID")
);
CREATE TABLE IF NOT EXISTS "Media" (
	"mID"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"FileType"	STRING,
	"MediaType"	STRING,
	"FileName"	STRING,
	"FileLocation"	STRING,
	"OwnerID"	INTEGER,
	"LoanerID"	INTEGER,
	"LoanReturnTime"	DATETIME,
	"IsBeingLoaned"	BOOLEAN DEFAULT ('FALSE'),
	FOREIGN KEY("LoanerID") REFERENCES "Users"("uID"),
	FOREIGN KEY("OwnerID") REFERENCES "Users"("uID")
);
CREATE TABLE IF NOT EXISTS "MediaCollectionJunction" (
	"mcjID"	INTEGER PRIMARY KEY AUTOINCREMENT,
	"MediaID"	INTEGER,
	"CollectionID"	INTEGER
);
COMMIT;