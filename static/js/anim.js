const myImage = document.getElementById("d-block-w-100");
const imageSources = ["../static/image/1.jpg", "../static/image/2.jpg", "../static/image/3.jpg", "../static/image/4.jpg", "../static/image/5.jpg", "../static/image/6.jpg", "../static/image/7.jpg"];
let currentImageIndex = 0;

function changeImage() {
  currentImageIndex++;
  if (currentImageIndex >= imageSources.length) {
    currentImageIndex = 0;
  }
  myImage.src = imageSources[currentImageIndex];
}

setInterval(changeImage, 3000);

$(".animated-element").waypoint(function() {
  $(this.element).addClass("fadeIn"); // добавляем класс с нужной анимацией
}, { offset: "75%" }); // задаем точку прохода - 75% от верхней границы экрана

