
var missions_api_url = base_url + "api/missions/retrieve?uuaid=" + user_info["uuaid"];
const missions_list = httpGet(missions_api_url)
console.log(missions_list)

if (get_cookie("page_num") == null){
    document.cookie = "page_num=" + 0;
}


// 8 + 9*(page-1)
function render_missions(page){
    let start = 9*page;
    for (let i = 0; i < 9; i++) {
        let mission_json = missions_list[start + i];

        let mission_element = document.getElementById("mission"+i);
        let meta_info = mission_element.getElementsByClassName('meta-info')[0];
        let mission_details = mission_element.getElementsByClassName('main-mission')[0];

        let value = meta_info.getElementsByClassName('point-value')[0];
        let advisor = meta_info.getElementsByClassName('advisor-name')[0];
        let mission_name = mission_details.getElementsByClassName('mission-name')[0];
        let description = mission_details.getElementsByClassName('mission-description')[0];

        value.innerHTML = mission_json["value"];
        if (mission_json["value"] >= 7500) {
            mission_element.style.backgroundColor = "gold";
            mission_element.style.boxShadow = "0 0 40px 10px gold"
        } else if (mission_json["value"] >= 5000) {
            mission_element.style.backgroundColor = "purple";
            mission_element.style.boxShadow = "0 0 40px 5px purple"
        } else if (mission_json["value"] <= 2500) {
            mission_element.style.backgroundColor = "lightgreen";
        } else {
            mission_element.style.boxShadow = "0 0 40px 1px rgb(78, 174, 212)"
        }
        advisor.innerHTML = httpGet(base_url + "api/users?user_id=" + mission_json["visibility"])["username"];
        mission_name.innerHTML = mission_json["name"];
        description.innerHTML = (mission_json["description"].length < 50) ? mission_json["description"] : mission_json["description"].substring(0,50) + "...";
    }
}

function increment_page(){
    curr = get_cookie("page_num")
    document.cookie = "page_num=" + (++curr);
    render_missions(get_cookie("page_num"))
}

function decrement_page(){
    curr = get_cookie("page_num")
    document.cookie = "page_num=" + (--curr);
    render_missions(get_cookie("page_num"))
}

render_missions(get_cookie("page_num"))


