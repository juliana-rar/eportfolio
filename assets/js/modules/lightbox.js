// Screenshot lightbox on a native <dialog>: focus trapping, Esc to close and
// the backdrop come from the browser. Adds arrows, keys and swipe navigation.
export function initLightbox() {
  const dialog = document.querySelector("[data-lightbox-dialog]");
  const links = [...document.querySelectorAll("[data-lightbox]")];
  if (!dialog || !links.length || typeof dialog.showModal !== "function") return;

  const image = dialog.querySelector(".lightbox__img");
  const caption = dialog.querySelector(".lightbox__caption");
  const counter = dialog.querySelector("[data-lightbox-counter]");
  const prev = dialog.querySelector("[data-lightbox-prev]");
  const next = dialog.querySelector("[data-lightbox-next]");
  let index = 0;
  let opener = null;

  if (links.length < 2) {
    prev.hidden = true;
    next.hidden = true;
  }

  function show(i) {
    index = (i + links.length) % links.length;
    const link = links[index];
    image.src = link.href;
    image.alt = link.querySelector("img")?.alt ?? "";
    caption.textContent = link.dataset.caption || "";
    counter.textContent = links.length > 1 ? `${index + 1} / ${links.length}` : "";
  }

  links.forEach((link, i) => {
    link.addEventListener("click", (event) => {
      event.preventDefault();
      opener = link;
      show(i);
      dialog.showModal();
    });
  });

  prev.addEventListener("click", () => show(index - 1));
  next.addEventListener("click", () => show(index + 1));
  dialog.querySelector("[data-lightbox-close]").addEventListener("click", () => dialog.close());

  dialog.addEventListener("keydown", (event) => {
    if (links.length < 2) return;
    if (event.key === "ArrowLeft") show(index - 1);
    if (event.key === "ArrowRight") show(index + 1);
  });

  // A click on the empty area around the image closes the viewer.
  dialog.addEventListener("click", (event) => {
    if (event.target === dialog) dialog.close();
  });

  // Horizontal swipe on touch screens.
  let startX = null;
  dialog.addEventListener("pointerdown", (event) => { startX = event.clientX; });
  dialog.addEventListener("pointerup", (event) => {
    if (startX === null || links.length < 2) return;
    const delta = event.clientX - startX;
    startX = null;
    if (Math.abs(delta) > 50) show(delta < 0 ? index + 1 : index - 1);
  });

  dialog.addEventListener("close", () => {
    image.removeAttribute("src");
    opener?.focus();
  });
}
