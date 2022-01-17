function onLoad() {
    const accessKey = localStorage.getItem('accessKey');

}

function setToken(username, password) {

    const url = 'http://127.0.0.1:8000/api/login/'
    const json = {"username": username, "password": password};
    const request = new XMLHttpRequest();
    request.open('POST', url, true);
    request.setRequestHeader('Content-Type', 'application/json');
    request.onload = function () {
        console.log(request.responseText);
        const obj = JSON.parse(request.responseText);
        // save access key in session storage

        localStorage.setItem("accessKey", obj.access);
        localStorage.setItem("username", username);
    }
    request.send(JSON.stringify(json));
}

function onSubmit() {
    const username = document.getElementsByName("username");
    const password = document.getElementsByName("password");

    setToken(username, password);
    console.log(window.sessionStorage.getItem("accessKey"));


}



