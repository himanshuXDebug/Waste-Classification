const slides = document.querySelectorAll('.slide');
const dots = document.querySelectorAll('.dot');

let currentIndex = 0;
const slideInterval = 10000; 

function showSlide(index) {
    slides.forEach(slide => slide.classList.remove('active'));
    dots.forEach(dot => dot.classList.remove('active'));

    slides[index].classList.add('active');
    dots[index].classList.add('active');

    document.querySelector('.slider').style.transform = `translateX(-${index * 100}%)`;
}

function nextSlide() {
    currentIndex = (currentIndex + 1) % slides.length; 
    showSlide(currentIndex);
}

setInterval(nextSlide, slideInterval);

dots.forEach(dot => {
    dot.addEventListener('click', () => {
        currentIndex = parseInt(dot.getAttribute('data-index'));
        showSlide(currentIndex);
    });
});
