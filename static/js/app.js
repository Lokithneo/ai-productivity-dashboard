function toggleTheme() {
    let body = document.body;
    body.classList.toggle("dark");
    body.classList.toggle("light");

    localStorage.setItem("theme", body.className);
}

window.onload = () => {
    let theme = localStorage.getItem("theme");
    if (theme) document.body.className = theme;
};

function copyText(text) {
    navigator.clipboard.writeText(text);
}