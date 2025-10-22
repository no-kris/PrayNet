/**
 * Theme Toggle Script with System Preference Detection
 * Supports manual override and remembers user preference
 */

// Initialize theme on page load (before DOM loads to prevent flash)
(function () {
  const savedTheme = localStorage.getItem("theme");
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;

  if (savedTheme === "dark" || (!savedTheme && prefersDark)) {
    document.documentElement.classList.add("dark-mode");
  }
})();

// Main initialization after DOM loads
document.addEventListener("DOMContentLoaded", function () {
  const themeToggle = document.getElementById("theme-toggle");
  const html = document.documentElement;

  function updateToggleIcon() {
    if (html.classList.contains("dark-mode")) {
      themeToggle.textContent = "☀️";
      themeToggle.setAttribute("aria-label", "Switch to light mode");
    } else {
      themeToggle.textContent = "🌙";
      themeToggle.setAttribute("aria-label", "Switch to dark mode");
    }
  }

  function toggleTheme() {
    html.classList.toggle("dark-mode");

    const theme = html.classList.contains("dark-mode") ? "dark" : "light";
    localStorage.setItem("theme", theme);

    updateToggleIcon();
  }

  if (themeToggle) {
    themeToggle.addEventListener("click", toggleTheme);
    updateToggleIcon();
  }

  // Listen for system theme changes (only if user hasn't set manual preference)
  window
    .matchMedia("(prefers-color-scheme: dark)")
    .addEventListener("change", (e) => {
      const savedTheme = localStorage.getItem("theme");

      if (!savedTheme) {
        if (e.matches) {
          html.classList.add("dark-mode");
        } else {
          html.classList.remove("dark-mode");
        }
        updateToggleIcon();
      }
    });
});

// Keyboard shortcut (Ctrl/Cmd + Shift + D)
document.addEventListener("keydown", function (e) {
  if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === "D") {
    e.preventDefault();
    const themeToggle = document.getElementById("theme-toggle");
    if (themeToggle) {
      themeToggle.click();
    }
  }
});
