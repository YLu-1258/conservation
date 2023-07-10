
var missions_api_url = base_url + "api/missions/retrieve?uuaid=" + user_info["uuaid"];
const missions_list = http_get(missions_api_url)
console.log(missions_list)

var page_num = 0;
var left_disabled = true;
var right_disabled = false;


// 8 + 9*(page-1)
function render_missions(page){
    let start = 9*page;
    if (start+9 > missions_list.length) {
        document.getElementById("right-button").onclick = null;
        right_disabled = true;
    } else {
        document.getElementById("right-button").onclick = increment_page;
        right_disabled = false;
    }
    if (start <= 0) {
        document.getElementById("left-button").onclick = null;
        left_disabled = true;
    } else {
        document.getElementById("left-button").onclick = decrement_page;
        left_disabled = false;
    }

    for (let i = 0; i < 9; i++) {
        let mission_element = document.getElementById("mission"+i);
        let meta_info = mission_element.getElementsByClassName('meta-info')[0];
        let mission_details = mission_element.getElementsByClassName('main-mission')[0];

        let value = meta_info.getElementsByClassName('point-value')[0];
        let advisor = meta_info.getElementsByClassName('advisor-name')[0];
        let mission_name = mission_details.getElementsByClassName('mission-name')[0];
        let description = mission_details.getElementsByClassName('mission-description')[0];

        try {
            let mission_json = missions_list[start + i];
            mission_element.setAttribute("data-mission-id", mission_json["id"]);
            value.innerHTML = mission_json["value"];
            if (mission_json["value"] >= 7500) {
                mission_element.style.backgroundColor = "gold";
                mission_element.style.boxShadow = "0 0 40px 10px gold"
            } else if (mission_json["value"] >= 5000) {
                mission_element.style.backgroundColor = "purple";
                mission_element.style.boxShadow = "0 0 40px 5px purple"
            } else if (mission_json["value"] <= 2500) {
                mission_element.style.boxShadow = "0px 0px 0px 0px lightgrey";
                mission_element.style.backgroundColor = "lightgreen";
            } else {
                mission_element.style.backgroundColor = "rgb(78, 174, 212)"
                mission_element.style.boxShadow = "0 0 40px 1px rgb(78, 174, 212)"
            }
            advisor.innerHTML = http_get(base_url + "api/users?user_id=" + mission_json["visibility"])["username"];
            mission_name.innerHTML = mission_json["name"];
            description.innerHTML = (mission_json["description"].length < 100) ? mission_json["description"] : mission_json["description"].substring(0,100) + "...";
        } catch (e) {
            mission_element.setAttribute("data-mission-id", 0);
            mission_element.style.backgroundColor = "lightgrey";
            mission_element.style.boxShadow = "0px 0px 0px 0px lightgrey"
            value.innerHTML = "";
            advisor.innerHTML = "";
            mission_name.innerHTML = "";
            description.innerHTML = "";
            
        }
    }
}

function increment_page() {
    if (!right_disabled) {
        const grid = document.querySelector('.grid');
        grid.classList.add('slide-out-left');
    
        setTimeout(() => {
            render_missions(++page_num);
            grid.classList.remove('slide-out-left');
            grid.classList.add('slide-in-right');
        }, 500);
    
        setTimeout(() => {
            grid.classList.remove('slide-in-right');
        }, 500);
    }
    
}
  
function decrement_page() {
    if (!left_disabled){
        const grid = document.querySelector('.grid');
        grid.classList.add('slide-out-right');
    
        setTimeout(() => {
            render_missions(--page_num);
            grid.classList.remove('slide-out-right');
            grid.classList.add('slide-in-left');
        }, 500);
    
        setTimeout(() => {
            grid.classList.remove('slide-in-left');
        }, 500);
    }
}

document.addEventListener('keydown', function(event) {
    if (event.key == "ArrowLeft") {
        decrement_page();
    }
});

document.addEventListener('keydown', function(event) {
    if (event.key == "ArrowRight") {
        increment_page();
    }
});

render_missions(page_num);


