const overlay = document.getElementById("authOverlay");
const loginModal = document.getElementById("loginModal");
const registerModal = document.getElementById("registerModal");

const loginBtn = document.getElementById("loginBtn");
const registerBtn = document.getElementById("registerBtn");

const closeLogin = document.getElementById("closeLogin");
const closeRegister = document.getElementById("closeRegister");

const showRegister = document.getElementById("showRegister");
const showLogin = document.getElementById("showLogin");


function openLogin() {
    overlay.classList.add("show");
    loginModal.classList.add("show");
    registerModal.classList.remove("show");
}


function openRegister() {
    overlay.classList.add("show");
    registerModal.classList.add("show");
    loginModal.classList.remove("show");
}


function closeAuth() {
    overlay.classList.remove("show");
    loginModal.classList.remove("show");
    registerModal.classList.remove("show");
}


loginBtn.addEventListener("click", openLogin);

registerBtn.addEventListener("click", openRegister);

closeLogin.addEventListener("click", closeAuth);

closeRegister.addEventListener("click", closeAuth);

showRegister.addEventListener("click", openRegister);

showLogin.addEventListener("click", openLogin);

overlay.addEventListener("click", closeAuth);