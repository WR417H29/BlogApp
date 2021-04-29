console.log("Nav Script Loaded");

const nav = document.getElementById("nav-bar");

nav.innerHTML = `
    <ul id="nav">
        <li><a href="/home">Home</a></li>
        <li><a href="/login">Login</a></li>
        <li><a href="/register">Register</a></li>
        <li><a href="/logout">Logout</a></li>
    </ul>
`;
