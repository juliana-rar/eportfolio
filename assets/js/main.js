// Entry module. Every feature is an enhancement: the site works without JS.
import { initNav } from "./modules/nav.js";
import { initTheme } from "./modules/theme.js";

initNav();
initTheme();

// Page-specific modules are only downloaded where they are needed.
if (document.querySelector("[data-lightbox]")) {
  import("./modules/lightbox.js").then(({ initLightbox }) => initLightbox());
}

if (document.querySelector("[data-filter]")) {
  import("./modules/filter.js").then(({ initFilter }) => initFilter());
}
