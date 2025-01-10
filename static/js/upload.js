const h2Element = document.getElementById('Pre-text');
function previewImage(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            const preview = document.getElementById('preview-image');
            const Check = document.getElementById('Check');
            const upload_container = document.getElementById('upload-container');
            const result_container = document.getElementById('result-container');
            preview.src = e.target.result;
            preview.style.display = 'block';
            h2Element.textContent = "Previewing...";
            upload_container.style.display = 'none';
            result_container.style.display = 'none';
            Check.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }
}

const feedbackFormBtn = document.getElementById('feedbackForm');
const feedbackTextarea = document.getElementById('feedbackText');
const feedbackSubmitBtn = document.getElementById('feedback_submit');
const feedbackMessage = document.getElementById('feedbackMessage');

feedbackFormBtn.addEventListener('click', () => {
    feedbackTextarea.style.display = 'block';
    feedbackSubmitBtn.style.display = 'inline-block';
    feedbackFormBtn.style.display = 'none';
});

feedbackSubmitBtn.addEventListener('click', () => {
    const feedbackContent = feedbackTextarea.value.trim();
    if (feedbackContent === '') {
        alert('Please write some feedback before submitting.');
        return;
    }
    feedbackTextarea.style.display = 'none';
    feedbackSubmitBtn.style.display = 'none';
    feedbackMessage.style.display = 'block';

    feedbackTextarea.value = '';

    setTimeout(() => {
        feedbackMessage.style.display = 'none';
        feedbackFormBtn.style.display = 'inline-block';
    }, 3000);
});

document.addEventListener("DOMContentLoaded", function () {
    const complainButton = document.getElementById("complain-button");
    const modal = document.getElementById("complain-modal");
    const closeButton = document.querySelector(".close-button");

    complainButton.addEventListener("click", function () {
        modal.style.display = "block";
        document.body.classList.add("modal-open"); // Add blur
    });

    closeButton.addEventListener("click", function () {
        modal.style.display = "none";
        document.body.classList.remove("modal-open");
    });

});
// window.addEventListener('click', function(event) {
//     const box = document.getElementById("complain-model");
//     if (!box.contains(event.target)) {
//         box.style.display = 'none';
//     }
// });``

setTimeout(function() {
    document.getElementById('reward-notification').style.display = 'none';
}, 6000);
