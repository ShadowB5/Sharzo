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
    var params = "uID="+uID;
    xhttp.open("GET", url+"/USER/GET"+"?"+params, true);

    xhttp.onreadystatechange = function() {
        if (this.readyState == readyState.done && this.status == httpStatus.ok) {
            let val = this.responseText;
            document.getElementById("JakeTesting").innerHTML = val;
        }
    };

    xhttp.send();
}


// POST createAccount
function createAccount(username, email, password){
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

// POST removeAccount DELETE?

// GET Friends

// GET FriendRequest
// POST AcceptFriendRequest
// POST DeclineFriendRequest DELETE?

// GET LoanRequest
// POST AcceptLoanRequest
// POST DeclineLoanRequest DELETE?

// GET Collection
// POST AddCollection
// POST RemoveCollection DELETE?

// GET Media
// POST AddMedia
// POST RemoveMedia DELETE?

