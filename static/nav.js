export default class Nav extends HTMLElement {
    constructor() {
        super();
    }

    render() {
        return(
            <div class="nav">
                <ul class="navbar">
                    <li><a href="/login">Login</a></li>
                    <li><a href="/logout">Logout</a></li>
                    <li><a href="/home">Home</a></li>
                </ul>
            </div>
        );
    }

    connectedCallback() {
        console.log("Connected");

        if (!this.rendered) {
            this.render();
            this.rendered = true;
        }
    };

    disconnectedCallback() {
        console.error("Disconnected");
    }
}

customElements.define('nav-bar', Nav);
