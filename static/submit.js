const submitBtn = document.getElementById('submitBtn');

const username = document.getElementById('uname');
const password = document.getElementById('pword');

submitBtn.onclick = () => {
    dataToPass = {
        "username" : username.value,
        "password" : password.value
    }

    fetch('/login', {
        method: 'POST',
        body: JSON.stringify(dataToPass)
    })
}
