const menuToggle = document.querySelector(".menu-toggle");
const navLinks = document.querySelector(".nav-links");

menuToggle.addEventListener("click", () => {
  navLinks.classList.toggle("show");
});

document.addEventListener("DOMContentLoaded", () => {
  const toggleBtn = document.querySelector(".category-toggle");
  const list = document.querySelector(".category-list");

  toggleBtn.addEventListener("click", () => {
    list.classList.toggle("show");
    // rotate arrow ▼ to ▲
    toggleBtn.textContent = list.classList.contains("show")
      ? "Categories ▲"
      : "Categories ▼";
  });
});
