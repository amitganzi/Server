
//nav bar- know where we at
const activePge=window.location.href;
const navList = document.querySelectorAll('nav a').
    forEach(link => {
    if(link.href == activePge){
        console.log(activePge);
        link.classList.add('active');
    }
    });



//clicking a picture and make it fullscreen
let modal = document.getElementById("myModal");
let img = document.getElementById("flowerShop");
let modalImg = document.getElementById("img01");
let captionText = document.getElementById("caption");


window.onload = function() {
    if (img != null) {
        img.onclick = function () {
            modal.style.display = "block";
            modalImg.src = this.src;
            captionText.innerHTML = this.alt;
        }
        let span = document.getElementsByClassName("close")[0];

        span.onclick = function () {
            modal.style.display = "none";
        }
    }
}





