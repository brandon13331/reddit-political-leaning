//alert("wakanda");

document.addEventListener("DOMSubtreeModified", function () {
    colorized();
});

colorized();

function colorized() {
    let cont = document.querySelectorAll('p');
// Put the user name here; Something to keep in mind if a user is politically biased in one comment highlight all the comments from the user
    let userNameElements = document.querySelectorAll("a[href='/user/user_name/']");
    for (userNameElement of userNameElements) {
        userNameElement.style['background-color'] = "red";
    }

    for (elt of cont) {
        //if (elt.toString() === "k") {
        elt.style['background-color'] = setColor(90);
//}
    }
}

function setColor(p) {
    var red = p<50 ? 255 : Math.round(256 - (p-50)*5.12);
    var green = p>50 ? 255 : Math.round((p)*5.12);
    return "#" + red.toString(16) + green.toString(16) + "00";
}

let currentUrl = window.location.href;
let userAndComments = [];
init();

function init() {
    if (document.readyState != 'loading') {
        loadApp();
    } else {
        document.addEventListener('DOMContentLoaded', loadApp());
    }
}

function status(response) {
    if (response.status >= 200 && response.status < 300) {
        return Promise.resolve(response)
    } else {
        return Promise.reject(new Error(response.statusText))
    }
}

function json(response) {
    return response.json();
}

function loadApp() {
    fetch(currentUrl + '.json')
        .then((response) => {return status(response)})
        .then((response) => {return json(response)})
        .then((json) => {return getCommentsFromJSON(json)})
        .then((arr) => {return filterUsers(arr)})
        .catch(function(error) {
            console.log('request failed', error.message)
        });
}

function getCommentsFromJSON(json) {
    return getUserAndCommentsFromArray(json[1].data.children);
}

//Recursively go through the object tree and compile all the comments
function getUserAndCommentsFromArray(arr) {
    arr.forEach(function(item) {
        if (item !== undefined) {
            userAndComments.push({username: item.data.author, comment: item.data.body});
            if (item.data.replies !== undefined && item.data.replies !== '') {
                getUserAndCommentsFromArray(item.data.replies.data.children);
            }
        }
    });
    return userAndComments;
}

function filterUsers(arr) {
   let filteredArray = arr.filter((element) => element.username !== "[deleted]" && element.comment !== "[deleted]");
   console.log(filteredArray);
   return filteredArray;
}
