const master_url = "http://localhost:8086"
const readyState = {unsent: 0, opened: 1, headers: 2, loading: 3, done: 4}
const httpStatus = {switchingProtocols: 101, ok: 200, created: 201, 
                    accepted:202, noContent: 204,  partialContent:206,
                    permanentRedirect:301, temporaryRedirect:307, found:302, 
                    useProxy:305, badRequest:400, unauthorized: 401, 
                    forbidden:403, notFound: 404, requestTimeout:408, conflict:409,
                    noResponse:444, tooManyRequest:429}

// GET Username
function getUsername(uID){

    var url = master_url;
    var xhttp = new XMLHttpRequest();
    var params = "uid="+uID;
    xhttp.open("GET", url+"/user/get"+"?"+params, true);

    xhttp.onreadystatechange = function() {
        if (this.readyState == readyState.done && this.status == httpStatus.ok) {
            let val = this.responseText;
            document.getElementById("JakeTesting").innerHTML = val;
        }
    };

    xhttp.send();
}

// POST createUser
function createUser(username, email, password, passwordConfirm){
    // If email is not valid, display an alert and leave the method.
    email_regular_expression = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    emailIsValid = email_regular_expression.test(String(email).toLowerCase());

    if(!emailIsValid){
        alert("Please enter a valid Email address.");
        return;
    }

    cleanEmail = encodeURIComponent(email);

    // If password is not approved, display an alert and leave the method.
    if(password != passwordConfirm){
        alert("Passwords do not match. Please renter password.");
        return;
    }
    if(password.length < 8){
        alert("Password length is too short. Must be at least 8 characters.");
        return;
    }

    var url = master_url;
    var xhttp = new XMLHttpRequest();
    var params = "username="+username+"&email="+cleanEmail+"&password="+password;
    xhttp.open("GET", url+"/user/create"+"?"+params, true);

    xhttp.onreadystatechange = function() {

        if (this.readyState == readyState.done && this.status == httpStatus.ok) {
            let val = this.responseText;
            document.getElementById("JakeTesting").innerHTML = val;
        }
    };

    xhttp.send();
}
function createAccount_BY_POST(username, email, password){
    // WARNING: References sha3.min.js by https://github.com/emn178
    var url = master_url;
    var xhttp = new XMLHttpRequest();
    var data = {};
    data.username = username;
    data.email = email;
    data.password = keccak256(password);
    
    var jason = JSON.stringify(data);

    xhttp.onreadystatechange = function() {
        if (this.readyState == readyState.done && this.status == httpStatus.ok) {
            let val = this.responseText;
        }
    };

    xhttp.open("POST", url, true);
    xhttp.send(json);

    while(true){
        // Halt the function until either the response is ready, or something bad happens
        if(xhttp.readyState == readyState.done && xhttp.status == httpStatus.created){
            break;
        }

        if(xhttp.readyState == readyState.done && xhttp.status == httpStatus.conflict){
            throw new Error(xhttp.status + ": Account already exists");
            break;
        }

        if(xhttp.status == httpStatus.noResponse){
            throw new Error(xhttp.status + ": No response");
            break;
        }
        if(xhttp.status == httpStatus.notFound ){
            throw new Error(xhttp.status + ": Not Found");
            break;
        }
        if(xhttp.status == httpStatus.requestTimeout){
            throw new Error(xhttp.status + ": Request Timeout");
            break;
        }
    }

    return this.responseText;
}

// POST Login
function loginUser(username, password){
    
    var url = master_url;
    var xhttp = new XMLHttpRequest();
    var params = "username="+username+"&password="+password;
    xhttp.open("GET", url+"/user/login"+"?"+params, true);

    xhttp.onreadystatechange = function() {
        // TODO: Create login cookie here

        if (this.readyState == readyState.done && this.status == httpStatus.ok) {
            let val = this.responseText;
            document.getElementById("JakeTesting").innerHTML = val;
        }
    };

    xhttp.send();
}

// POST removeAccount DELETE?
function deleteUser(uID){

    var url = master_url;
    var xhttp = new XMLHttpRequest();
    var params = "uid="+uID;
    xhttp.open("GET", url+"/user/delete"+"?"+params, true);

    xhttp.onreadystatechange = function() {
        if (this.readyState == readyState.done && this.status == httpStatus.ok) {
            let val = this.responseText;
            document.getElementById("JakeTesting").innerHTML = val;
        }
    };

    xhttp.send();
}

// GET Friends
function getFriends(uID){

    var url = master_url;
    var xhttp = new XMLHttpRequest();
    var params = "uid="+uID;
    xhttp.open("GET", url+"/friends/get"+"?"+params, true);

    xhttp.onreadystatechange = function() {
        if (this.readyState == readyState.done && this.status == httpStatus.ok) {
            let val = this.responseText;
            document.getElementById("JakeTesting").innerHTML = val;
        }
    };

    xhttp.send();
}

function deleteFriend(uID, friendID){

    var url = master_url;
    var xhttp = new XMLHttpRequest();
    var params = "uid="+uID+"&frid="+friendID;
    xhttp.open("GET", url+"/friends/get"+"?"+params, true);

    xhttp.onreadystatechange = function() {
        if (this.readyState == readyState.done && this.status == httpStatus.ok) {
            let val = this.responseText;
            document.getElementById("JakeTesting").innerHTML = val;
        }
    };

    xhttp.send();
}

// GET FriendRequest
function getFriendRequests(uID){

    var url = master_url;
    var xhttp = new XMLHttpRequest();
    var params = "uid="+uID;
    xhttp.open("GET", url+"/friendsrequest/get"+"?"+params, true);

    xhttp.onreadystatechange = function() {
        if (this.readyState == readyState.done && this.status == httpStatus.ok) {
            let val = this.responseText;
            document.getElementById("JakeTesting").innerHTML = val;
        }
    };

    xhttp.send();
}

// POST AcceptFriendRequest
function acceptFriendRequest(frID){

    var url = master_url;
    var xhttp = new XMLHttpRequest();
    var params = "frid="+frID;
    xhttp.open("GET", url+"/friendsrequest/accept"+"?"+params, true);

    xhttp.onreadystatechange = function() {
        if (this.readyState == readyState.done && this.status == httpStatus.ok) {
            let val = this.responseText;
            document.getElementById("JakeTesting").innerHTML = val;
        }
    };

    xhttp.send();
}

// POST DeclineFriendRequest DELETE?
function declineFriendRequest(frID){

    var url = master_url;
    var xhttp = new XMLHttpRequest();
    var params = "frid="+frID;
    xhttp.open("GET", url+"/friendsrequest/decline"+"?"+params, true);

    xhttp.onreadystatechange = function() {
        if (this.readyState == readyState.done && this.status == httpStatus.ok) {
            let val = this.responseText;
            document.getElementById("JakeTesting").innerHTML = val;
        }
    };

    xhttp.send();
}

// GET LoanRequest
function getLoanRequests(uID){

    var url = master_url;
    var xhttp = new XMLHttpRequest();
    var params = "uid="+uID;
    xhttp.open("GET", url+"/loanrequest/get"+"?"+params, true);

    xhttp.onreadystatechange = function() {
        if (this.readyState == readyState.done && this.status == httpStatus.ok) {
            let val = this.responseText;
            document.getElementById("JakeTesting").innerHTML = val;
        }
    };

    xhttp.send();
}

// POST AcceptLoanRequest
function acceptLoanRequest(rmID){

    var url = master_url;
    var xhttp = new XMLHttpRequest();
    var params = "rmid="+rmID;
    xhttp.open("GET", url+"/loanrequest/accept"+"?"+params, true);

    xhttp.onreadystatechange = function() {
        if (this.readyState == readyState.done && this.status == httpStatus.ok) {
            let val = this.responseText;
            document.getElementById("JakeTesting").innerHTML = val;
        }
    };

    xhttp.send();
}

// POST DeclineLoanRequest DELETE?
function declineLoanRequest(rmID){

    var url = master_url;
    var xhttp = new XMLHttpRequest();
    var params = "rmid="+rmID;
    xhttp.open("GET", url+"/loanrequest/decline"+"?"+params, true);

    xhttp.onreadystatechange = function() {
        if (this.readyState == readyState.done && this.status == httpStatus.ok) {
            let val = this.responseText;
            document.getElementById("JakeTesting").innerHTML = val;
        }
    };

    xhttp.send();
}

// GET Collection
function getCollections(uID){

    var url = master_url;
    var xhttp = new XMLHttpRequest();
    var params = "uid="+uID;
    xhttp.open("GET", url+"/collections/get"+"?"+params, true);

    xhttp.onreadystatechange = function() {
        if (this.readyState == readyState.done && this.status == httpStatus.ok) {
            let val = this.responseText;
            document.getElementById("JakeTesting").innerHTML = val;
        }
    };

    xhttp.send();
}

function getCollection(cID){

    var url = master_url;
    var xhttp = new XMLHttpRequest();
    var params = "cid="+uID;
    xhttp.open("GET", url+"/collections/get"+"?"+params, true);

    xhttp.onreadystatechange = function() {
        if (this.readyState == readyState.done && this.status == httpStatus.ok) {
            let val = this.responseText;
            document.getElementById("JakeTesting").innerHTML = val;
        }
    };

    xhttp.send();
}

// POST AddCollection
function createCollection(uID, collectionName){

    var url = master_url;
    var xhttp = new XMLHttpRequest();
    var params = "uid="+uID+"&name="+collectionName;
    xhttp.open("GET", url+"/collections/create"+"?"+params, true);

    xhttp.onreadystatechange = function() {
        if (this.readyState == readyState.done && this.status == httpStatus.ok) {
            let val = this.responseText;
            document.getElementById("JakeTesting").innerHTML = val;
        }
    };

    xhttp.send();
}

// POST RemoveCollection DELETE?
function deleteCollection(cID){

    var url = master_url;
    var xhttp = new XMLHttpRequest();
    var params = "cid="+cID;
    xhttp.open("GET", url+"/collections/delete"+"?"+params, true);

    xhttp.onreadystatechange = function() {
        if (this.readyState == readyState.done && this.status == httpStatus.ok) {
            let val = this.responseText;
            document.getElementById("JakeTesting").innerHTML = val;
        }
    };

    xhttp.send();
}

// GET Media
function getMedia(mID){

    var url = master_url;
    var xhttp = new XMLHttpRequest();
    var params = "mid="+mID;
    xhttp.open("GET", url+"/media/get"+"?"+params, true);

    xhttp.onreadystatechange = function() {
        if (this.readyState == readyState.done && this.status == httpStatus.ok) {
            let val = this.responseText;
            document.getElementById("JakeTesting").innerHTML = val;
        }
    };

    xhttp.send();
}

function getMediaInCollection(cID){

    var url = master_url;
    var xhttp = new XMLHttpRequest();
    var params = "cid="+cID;
    xhttp.open("GET", url+"/media/get"+"?"+params, true);

    xhttp.onreadystatechange = function() {
        if (this.readyState == readyState.done && this.status == httpStatus.ok) {
            let val = this.responseText;
            document.getElementById("JakeTesting").innerHTML = val;
        }
    };

    xhttp.send();
}

function getMediaByUser(uID){

    var url = master_url;
    var xhttp = new XMLHttpRequest();
    var params = "uid="+uID;
    xhttp.open("GET", url+"/media/get"+"?"+params, true);

    xhttp.onreadystatechange = function() {
        if (this.readyState == readyState.done && this.status == httpStatus.ok) {
            let val = this.responseText;
            document.getElementById("JakeTesting").innerHTML = val;
        }
    };

    xhttp.send();
}

function getMediaByLoan(uID, isOnLoan){

    var url = master_url;
    var xhttp = new XMLHttpRequest();

    var params = ""
    if(isOnLoan){
        params = "uid="+uID+"&onloan=true";
    }
    else{
        params = "uid="+uID+"&onloan=false";
    }
    
    xhttp.open("GET", url+"/media/get"+"?"+params, true);

    xhttp.onreadystatechange = function() {
        if (this.readyState == readyState.done && this.status == httpStatus.ok) {
            let val = this.responseText;
            document.getElementById("JakeTesting").innerHTML = val;
        }
    };

    xhttp.send();
}

// POST AddMedia
function createMedia(ownerID, mediaType, fileName){

    var url = master_url;
    var xhttp = new XMLHttpRequest();
    var params = "ownerid="+ownerID+"&mediatype="+mediaType+"&filename="+fileName;
    xhttp.open("GET", url+"/media/create"+"?"+params, true);

    xhttp.onreadystatechange = function() {
        if (this.readyState == readyState.done && this.status == httpStatus.ok) {
            let val = this.responseText;
            document.getElementById("JakeTesting").innerHTML = val;
        }
    };

    xhttp.send();
}

// POST RemoveMedia DELETE?
function deleteMedia(mid){

    var url = master_url;
    var xhttp = new XMLHttpRequest();
    var params = "mid="+mID;
    xhttp.open("GET", url+"/media/delete"+"?"+params, true);

    xhttp.onreadystatechange = function() {
        if (this.readyState == readyState.done && this.status == httpStatus.ok) {
            let val = this.responseText;
            document.getElementById("JakeTesting").innerHTML = val;
        }
    };

    xhttp.send();
}

