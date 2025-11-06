document.addEventListener("DOMContentLoaded", function() {
  const carousel = document.querySelector(".carousel");
  const images = carousel.querySelectorAll("img");
  const prevBtn = document.getElementById("prev-btn");
  const nextBtn = document.getElementById("next-btn");
  let currentIndex = 0;

  function showImage(index) {
    // Hide all images
    images.forEach(img => {
      img.style.display = "none";
    });

    // Display the image at the specified index
    images[index].style.display = "block";
  }

  // Initialize the slider
  showImage(currentIndex);

  // Event listeners for previous and next buttons
  prevBtn.addEventListener("click", () => {
    currentIndex = (currentIndex - 1 + images.length) % images.length;
    showImage(currentIndex);
  });

  nextBtn.addEventListener("click", () => {
    currentIndex = (currentIndex + 1) % images.length;
    showImage(currentIndex);
  });
  function toggleLoginForm() {
    var loginForm = document.getElementById("login-form");
    if (loginForm.style.display === "none") {
        loginForm.style.display = "block";
    } else {
        loginForm.style.display = "none";
    }
}
});
