const user_history = http_get(base_url + "api/history?user_id=" + get_cookie("user_id"));

function add_history_entry(type, content) {
	// retrieve our grid
	var grid_container = document.getElementById(type);

	// create entry element
	var entry = document.createElement("div");
	entry.classList.add("history-entry");

	// create mission info container
	var container = document.createElement("div");
	container.classList.add("mission-info-container");

	// mission info details
	var points = document.createElement("div");
	var visibility = document.createElement("div");
	var time = document.createElement("div");
	var location = document.createElement("div");
	points.classList.add("mission-info");
	points.classList.add("mission-points");
	visibility.classList.add("mission-info");
	visibility.classList.add("mission-visibility");
	time.classList.add("mission-info");
	time.classList.add("mission-time");
	location.classList.add("mission-info");
	location.classList.add("mission-location");

	// mission info content
	points.innerHTML = '<p><i class="fas fa-globe-americas"></i> ' + content["points"] + '</p>'
	visibility.innerHTML = '<p><i class="far fa-eye"></i> ' + content["visibility"] + '</p>'
	time.innerHTML = '<p><i class="far fa-clock"></i> ' + content["time"] + '</p>'
	location.innerHTML = '<p><i class="fas fa-map-marker-alt"></i> ' + content["location"] + '</p>'

	// add mission info to container
	container.appendChild(points);
	container.appendChild(visibility);
	container.appendChild(time);
	container.appendChild(location);

	// creating additional elements
	divider = document.createElement("hr");
	divider.classList.add("mission-divider");
	title = document.createElement("h1");
	title.classList.add("mission-title");
	title.innerHTML = content["title"];
	description = document.createElement("p");
	description.innerHTML = content["description"];

	//append all
	entry.appendChild(container);
	entry.appendChild(divider);
	entry.appendChild(title);
	entry.appendChild(description);

	if (content["points"] >= 7500) {
		entry.style.backgroundColor = "gold";
		entry.style.boxShadow = "0 0 40px 10px gold"
	} else if (content["points"] >= 5000) {
		entry.style.backgroundColor = "purple";
		entry.style.boxShadow = "0 0 40px 5px purple"
	} else if (content["points"] <= 2500) {
		entry.style.boxShadow = "0px 0px 0px 0px lightgrey";
		entry.style.backgroundColor = "lightgreen";
	} else {
		entry.style.backgroundColor = "rgb(78, 174, 212)"
		entry.style.boxShadow = "0 0 40px 1px rgb(78, 174, 212)"
	}

	grid_container.append(entry);
}

function render_history() {
	in_progress = user_history["in_progress"]
	completed = user_history["completed"]

	for (let i = 0; i < in_progress.length; i++) {
		let history = {"title": in_progress[i]["name"], 
		"points": in_progress[i]["value"], 
		"visibility": http_get(base_url + "api/users?user_id=" + in_progress[i]["visibility"])["username"], 
		"time": in_progress[i]["time"],
		"location": in_progress[i]["location"],
		"description": (in_progress[i]["description"] < 100) ? in_progress[i]["description"] : in_progress[i]["description"].substring(0,100) + "..."};

		add_history_entry("in-progress", history);

	}

	for (let i = 0; i < completed.length; i++) {
		let history = {"title": completed[i]["name"], 
		"points": completed[i]["value"], 
		"visibility": http_get(base_url + "api/users?user_id=" + completed[i]["visibility"])["username"], 
		"time": completed[i]["time"],
		"location": completed[i]["location"],
		"description": (completed[i]["description"] < 100) ? completed[i]["description"] : completed[i]["description"].substring(0,100) + "..."};

		add_history_entry("completed", history);

	}
}

render_history()