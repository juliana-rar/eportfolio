// Collapsible mobile menu. Adds .nav-enhanced to <html> only once it works,
// so a failed script never leaves the menu hidden.
const DESKTOP = window.matchMedia("(min-width: 48rem)");

export function initNav() {
  const toggle = document.querySelector("[data-nav-toggle]");
  const nav = toggle && document.getElementById(toggle.getAttribute("aria-controls"));
  if (!toggle || !nav) return;

  const isOpen = () => toggle.getAttribute("aria-expanded") === "true";
  const setOpen = (open) => {
    toggle.setAttribute("aria-expanded", String(open));
    nav.classList.toggle("site-nav--open", open);
  };

  toggle.hidden = false;
  document.documentElement.classList.add("nav-enhanced");

  toggle.addEventListener("click", () => setOpen(!isOpen()));

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && isOpen()) {
      setOpen(false);
      toggle.focus();
    }
  });

  document.addEventListener("click", (event) => {
    if (isOpen() && !nav.contains(event.target) && !toggle.contains(event.target)) {
      setOpen(false);
    }
  });

  DESKTOP.addEventListener("change", (event) => {
    if (event.matches) setOpen(false);
  });
}
