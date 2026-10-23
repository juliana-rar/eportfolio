// Runs in <head> before first paint (classic script, not a module):
// marks JS support and applies the theme saved by the toggle, avoiding a flash.
(function () {
  var root = document.documentElement;
  root.classList.remove("no-js");
  root.classList.add("js");
  try {
    var theme = localStorage.getItem("theme");
    if (theme === "light" || theme === "dark") {
      root.setAttribute("data-theme", theme);
    }
  } catch (error) {
    // Storage blocked: follow the system preference.
  }
})();
