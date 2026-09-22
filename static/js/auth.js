const overlay = document.getElementById("authOverlay");

const loginPopup = document.getElementById("loginPopup");
const registerPopup = document.getElementById("registerPopup");

const loginBtn = document.getElementById("loginBtn");
// const registerBtn = document.getElementById("registerBtn");

const loginCloseBtn = document.getElementById("loginCloseBtn");
const registerCloseBtn = document.getElementById("registerCloseBtn");

const showRegisterBtn = document.getElementById("showRegisterBtn");
const showLoginBtn = document.getElementById("showLoginBtn");

function openLogin() {
    overlay.classList.add("visible");
    loginPopup.classList.add("visible");
    registerPopup.classList.remove("visible");
}

function openRegister() {
    overlay.classList.add("visible");
    registerPopup.classList.add("visible");
    loginPopup.classList.remove("visible");
}

function closeAuth() {
    overlay.classList.remove("visible");
    loginPopup.classList.remove("visible");
    registerPopup.classList.remove("visible");
}

// ================= EVENT LISTENERS =================
loginBtn.addEventListener("click", openLogin);
// registerBtn.addEventListener("click", openRegister);
loginCloseBtn.addEventListener("click", closeAuth);
registerCloseBtn.addEventListener("click", closeAuth);
showRegisterBtn.addEventListener("click", openRegister);
showLoginBtn.addEventListener("click", openLogin);
overlay.addEventListener("click", closeAuth);

openLogin();

const loginForm = document.getElementById("loginForm");
loginForm.addEventListener("submit", async function (event) {
    // Stop the browser from refreshing the page
    event.preventDefault();

    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;

    // Clear previous errors before submitting
    document.getElementById("loginEmailError").textContent = "";
    document.getElementById("loginPasswordError").textContent = "";

    try {
        const response = await fetch("/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                email: email,
                password: password
            })
        });

        const data = await response.json();
        if (response.ok) {
            localStorage.setItem("access_token", data.access_token);
            closeAuth();
        } else {
            document.getElementById("loginEmail").value = "";
            document.getElementById("loginPassword").value = "";

            document.getElementById("loginPasswordError").textContent = data.message;
        }

    } catch (error) {
        document.getElementById("loginPasswordError").textContent =
        "Something went wrong. Please try again.";
    }
});


const registerForm = document.getElementById("registerForm");
registerForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const username = document.getElementById("registerUsername").value;
    const email = document.getElementById("registerEmail").value;
    const password = document.getElementById("registerPassword").value;
    const confirmPassword = document.getElementById("registerConfirmPassword").value;

    // Clear previous errors
    document.getElementById("registerUsernameError").textContent = "";
    document.getElementById("registerEmailError").textContent = "";
    document.getElementById("registerPasswordError").textContent = "";
    document.getElementById("registerConfirmPasswordError").textContent = "";

    // Check whether passwords match
    if (password !== confirmPassword) {
        document.getElementById("registerConfirmPasswordError").textContent ="Passwords do not match.";
        return;
    }

    try {
        const response = await fetch("/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                username: username,
                email: email,
                password: password
            })
        });

        const data = await response.json();

        if (response.ok) {
            openLogin();
        } else {
            document.getElementById("registerUsername").value = "";
            document.getElementById("registerEmail").value = "";
            document.getElementById("registerPassword").value = "";
            document.getElementById("registerConfirmPassword").value = "";

            document.getElementById("registerEmailError").textContent = data.message;
        }

    } catch (error) {
        document.getElementById("registerEmailError").textContent =
            "Something went wrong. Please try again.";
    }
});
