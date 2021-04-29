console.log("Submit Script Loaded");

function submit(path) {
    const username = document.getElementById('uname');
    const password = document.getElementById('pword');

    console.log("Submit Clicked");

    dataToPass = {
        "username": username.value,
        "password": password.value,
    }

    fetch(path, {
        headers: {
            'Content-type': 'application/json'
        },
        method: 'POST',
        body: JSON.stringify(dataToPass)
    }).then((res) => {return res.text()}
    ).then((text) => {
        console.log("Response: ");
        console.log(text);
    })

    username.value = '';
    password.value = '';
};
