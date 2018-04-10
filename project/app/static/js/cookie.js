// Set cookie
function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toUTCSstring();
    document.cookie = cname + "=" + cvalue + ";" + expires;
}

// Get cookie
function getCookie(cname) {
    var name = cname + "=";
    var cl = document.cookie.split(';');
    for (var i = 0; i < cl.length; i++) {
        var c = cl[i];
        while (c.charAt(0) == ' ')
            c = c.substring(1);
        if (c.indexOf(name) != -1)
            return c.substring(name.length, c.length);
    }
    return "";
}

// Clear cookie
function clearCookie() {
    var user = getCookie("username");
    if (user != "") {
        alert("Welcome again " + user);
    } else {
        user = prompt("Please enter your time:", "");
        if (user != "" && user != null) {
            setCookie("username", user, 365);
        }
    }
}

checkCookie();