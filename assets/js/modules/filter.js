// Progressive enhancement for the projects filter: the links are normal
// server-side ?tech= links; here they fetch the page and swap only the
// [data-filter] region, keeping scroll position and browser history.
export function initFilter() {
  const region = document.querySelector("[data-filter]");
  if (!region) return;

  region.addEventListener("click", (event) => {
    const link = event.target.closest("a[data-filter-link], .pagination a");
    if (!link || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) {
      return;
    }
    event.preventDefault();
    load(link.href, { push: true, focusHref: link.getAttribute("href") });
  });

  window.addEventListener("popstate", () => load(window.location.href, { push: false }));

  async function load(url, { push, focusHref = null }) {
    region.setAttribute("aria-busy", "true");
    try {
      const response = await fetch(url, { headers: { "X-Requested-With": "fetch" } });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const doc = new DOMParser().parseFromString(await response.text(), "text/html");
      const fresh = doc.querySelector("[data-filter]");
      if (!fresh) throw new Error("Filter region missing");

      region.replaceChildren(...fresh.childNodes);
      document.title = doc.title;
      if (push) window.history.pushState({}, "", url);

      // Keep keyboard users where they were; otherwise announce the new count.
      const target =
        (focusHref && region.querySelector(`a[data-filter-link][href="${CSS.escape(focusHref)}"]`)) ||
        region.querySelector("[data-filter-status]");
      target?.focus({ preventScroll: true });
    } catch {
      window.location.assign(url);
    } finally {
      region.removeAttribute("aria-busy");
    }
  }
}
