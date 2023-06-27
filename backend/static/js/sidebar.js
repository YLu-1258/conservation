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
        document.getElementById("openbtn").style.color="#00da3e";
    } else {
        var elements = document.querySelectorAll(".sidebar-link");
        for (var i = 0; i < elements.length; i++) {
            elements[i].style.display = "none";
        }
        sidebar.style.width = "0";
        document.getElementById("main").style.marginLeft = "0";
        document.getElementById("openbtn").style.color="#2b9348";
    }
};