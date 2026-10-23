// Light/dark toggle. The choice is stored per browser; theme-init.js applies it
// on the next page load before first paint.
const STORAGE_KEY = "theme";
const prefersDark = window.matchMedia("(prefers-color-scheme: dark)");
const root = document.documentElement;

function currentTheme() {
  return root.dataset.theme || (prefersDark.matches ? "dark" : "light");
}

export function initTheme() {
  const button = document.querySelector("[data-theme-toggle]");
  if (!button) return;

  const sync = () => button.setAttribute("aria-pressed", String(currentTheme() === "dark"));

  button.hidden = false;
  sync();

  button.addEventListener("click", () => {
    const next = currentTheme() === "dark" ? "light" : "dark";
    root.dataset.theme = next;
    try {
      localStorage.setItem(STORAGE_KEY, next);
    } catch {
      // Storage blocked: the choice lasts until the next page load.
    }
    sync();
  });

  prefersDark.addEventListener("change", sync);
}
