document.addEventListener("DOMContentLoaded", function () {
  const hamburger = document.querySelector(".hamburger");
  const navList = document.querySelector(".nav__list__container");

  hamburger.addEventListener("click", function () {
    hamburger.classList.toggle("active");
    navList.classList.toggle("active");
  });

  // Close menu when clicking outside
  document.addEventListener("click", function (e) {
    if (!hamburger.contains(e.target) && !navList.contains(e.target)) {
      hamburger.classList.remove("active");
      navList.classList.remove("active");
    }
  });
});
