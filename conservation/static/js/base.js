var base_url = "http://127.0.0.1:8133/"
var user_api_url = base_url + "api/users?user_id=" + get_cookie("user_id");
const user_info = http_get(user_api_url);

function get_cookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function http_get(url){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", url, false );
    xmlHttp.send( null );
    return JSON.parse(xmlHttp.responseText);
}

function http_post(url, payload){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "POST", url, false );
    xmlHttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xmlHttp.send(JSON.stringify(payload));
    return JSON.parse(xmlHttp.responseText);
}

function http_put(url, payload){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "PUT", url, false );
    xmlHttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xmlHttp.send(JSON.stringify(payload));
    return JSON.parse(xmlHttp.responseText);
}

function http_delete(url, payload){
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "DELETE", url, false );
    xmlHttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xmlHttp.send(JSON.stringify(payload));
    return JSON.parse(xmlHttp.responseText);
}

function configure_sidebar_visibility() {
    let role = user_info["role"];

    let leaderboard = document.getElementById("leaderboard-link");
    let tutorial = document.getElementById("tutorial-link");
    let missions = document.getElementById("missions-link");

    leaderboard.innerHTML = '<i class="fas fa-trophy"></i> Leaderboard';
    leaderboard.setAttribute("href", "/leaderboard")
    leaderboard.classList.remove("hidden-link");

    tutorial.innerHTML = '<i class="fas fa-question-circle"></i> Help/Tutorial';
    tutorial.setAttribute("href", "/tutorial")
    tutorial.classList.remove("hidden-link");

    missions.innerHTML = '<i class="fas fa-home"></i> Missions';
    missions.setAttribute("href", "/")
    missions.classList.remove("hidden-link");
    // Normal users are privileged to see history
    if (role === 2) {
        let history = document.getElementById("history-link");

        history.innerHTML = '<i class="fas fa-history"></i> History';
        history.setAttribute("href", "/history")
        history.classList.remove("hidden-link");
    // Advisor level users can see the advisor panel to manage their students
    } else if (role === 1) {
        let advisor = document.getElementById("advisors-link");

        advisor.innerHTML = '<i class="fas fa-users-cog"></i> Advisor panel';
        advisor.setAttribute("href", "/advisor-panel")
        advisor.classList.remove("hidden-link");
    // Admin level users can use the admin pane to manage their students
    } else if (role === 0) {
        let admin = document.getElementById("admin-link");

        admin.innerHTML = '<i class="fas fa-cog"></i> Admin panel';
        admin.setAttribute("href", "/admin-panel")
        admin.classList.remove("hidden-link");
    }
}

function mark_current_tab() {
    var currentUrl = window.location.pathname;

    var links = document.getElementsByClassName("sidebar-link");
    console.log(links);
    for (var i = 0; i < links.length; i++) {
        var linkUrl = links[i].getAttribute("href");

        if (currentUrl === linkUrl) {
            links[i].firstChild.style.color = "#ffffff";
            links[i].classList.add("sidebar-link-current");
            links[i].setAttribute("aria-disabled", "true");
            links[i].classList.remove("sidebar-link");
        }
    }
}

document.addEventListener("DOMContentLoaded", function() {
    configure_sidebar_visibility();
    mark_current_tab();
});