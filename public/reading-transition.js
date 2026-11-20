// The browser snapshots the chosen link in place and the heading at its new position.
let selectedLink;
const reduceMotion = () => matchMedia('(prefers-reduced-motion: reduce)').matches;
document.addEventListener('click', (event) => {
  selectedLink = event.target.closest?.('main a[href]');
}, true);

addEventListener('pageswap', (event) => {
  if (!event.viewTransition) return;
  const next = event.activation?.entry?.url;
  if (reduceMotion() || !selectedLink || selectedLink.href !== next ||
      new URL(next).pathname === location.pathname) {
    event.viewTransition.skipTransition();
    return;
  }
  const link = selectedLink;
  link.style.viewTransitionName = 'reading-selection';
  event.viewTransition.finished.finally(() => { link.style.viewTransitionName = ''; });
});

addEventListener('pagereveal', (event) => {
  if (!event.viewTransition || reduceMotion()) return;
  const heading = document.querySelector('main h1');
  if (!heading) return;
  heading.style.viewTransitionName = 'reading-selection';
  event.viewTransition.finished.finally(() => { heading.style.viewTransitionName = ''; });
});
