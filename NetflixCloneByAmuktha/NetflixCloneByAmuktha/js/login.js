let btnEnter = document.querySelector('#btnEnter');
btnEnter.addEventListener('click', enter);

function enter(e){
    e.preventDefault();
    window.location.href = "user.html";
}