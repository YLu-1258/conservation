const toggleSidebar = () => {
    const sidebar = document.getElementById("mySidebar");
    const sidebarWidth = window.getComputedStyle(sidebar).width;

    if (sidebarWidth === "0px") {
        var elements = document.querySelectorAll(".sidebar-link");
        for (var i = 0; i < elements.length; i++) {
            elements[i].style.display = "block";
        }
        sidebar.style.width = "250px";
        document.getElementById("main").style.marginLeft = "250px";
        document.getElementById("header").style.marginLeft = "250px";
        document.getElementById("footer").style.marginLeft = "250px";
        document.getElementById("openbtn").style.backgroundColor="#ffffff";
        document.getElementById("openbtn").style.color = "#000000";
    } else {
        var elements = document.querySelectorAll(".sidebar-link");
        for (var i = 0; i < elements.length; i++) {
            elements[i].style.display = "none";
        }
        sidebar.style.width = "0";
        document.getElementById("main").style.marginLeft = "0";
        document.getElementById("header").style.marginLeft = "0";
        document.getElementById("footer").style.marginLeft = "0";
        document.getElementById("openbtn").style.backgroundColor="transparent";
        document.getElementById("openbtn").style.color = "#ffffff";
    }
};