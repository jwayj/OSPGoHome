document.addEventListener('DOMContentLoaded', function () {
    const toggleBtn = document.querySelector('.navbar__toogleBtn');
    const menu = document.querySelector('.navbar__menu');

    toggleBtn.addEventListener('click', function () {
        menu.classList.toggle('active');
    });
});
function openPopup(id) {
    document.getElementById(id).style.display = 'flex';
}

function closePopup(id) {
    document.getElementById(id).style.display = 'none';
}