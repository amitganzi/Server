

//nav bar- know where we at
const activePge=window.location.href;
const navList = document.querySelectorAll('nav a').
    forEach(link => {
    if(link.href == activePge){
        console.log(activePge);
        link.classList.add('active');
    }
    });

//after clicking submit
let form = document.getElementsByTagName("form")[0];
form.addEventListener("submit", (e) => {
e.preventDefault();
alert("Form Submitted!");
const inputs = document.querySelectorAll('#FirstName, #LastName, #email, #checking1, #checking2, #checking3, #checking4 #addings');
  inputs.forEach(input => {
    input.value = '';
  });
});

