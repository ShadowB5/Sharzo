

function User(uID, username, email){
    this.uID = uID || -1;
    this.username = username || "Not Logged In";
    this.email = email || "null@null.com";
    this.friends = [];
    this.collections = [];
}

function Collection(cID, ownerID, dateCreated, name){
    this.cID = cID;
    this.ownerID = ownerID; // uID
    this.dateCreated = dateCreated;
    this.name = name;
    this.media = []
}

function RequestFriend(rfID, fromID, toID){
    this.rfID = rfID;
    this.fromID = fromID; // uID
    this.toID = toID; //uID
}

function Media(mID, fileType, mediaType, fileName, 
                fileLocation, ownerID, loanerID, 
                loanReturnTime, isBeingLoaned){
    this.mID = mID;
    this.fileType = fileType;
    this.mediaType = mediaType;
    this.filename = fileName;
    this.fileLocation = fileLocation;
    this.ownerID = ownerID;
    this.loanerID = loanerID;
    this.loanReturnTime = loanReturnTime;
    this.isBeingLoaned = isBeingLoaned;
}