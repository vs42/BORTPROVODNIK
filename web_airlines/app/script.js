var request = new XMLHttpRequest();
function reqReadyStateChange() {
    if (request.readyState == 4) {
        var status = request.status;
        if (status == 200) {
            document.getElementById("output").innerHTML=request.responseText;
        }
    }
}
request.open("POST", "172.31.226.63:80/api/login");
request.onreadystatechange = reqReadyStateChange;
request.send(username, password);