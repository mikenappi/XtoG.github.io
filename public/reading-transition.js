// Save the opening link on its own history entry so nested expansions close in order.
(() => {
  const links = () => [...document.querySelectorAll('main a[href]')];
  const heading = () => document.querySelector('main h1');
  const reduced = () => matchMedia('(prefers-reduced-motion: reduce)').matches;
  const savedLink = () => window.navigation?.currentEntry?.getState()?.readingLink ?? history.state?.readingLink;
  let closing = false;

  function openingLink(url) {
    const saved = savedLink();
    const list = links();
    const original = saved?.url === url && list[saved.index];
    return original?.href === url ? original : list.find(link => link.href === url);
  }

  function canGoBack(home) {
    const nav = window.navigation;
    if (nav?.currentEntry) {
      const previous = nav.entries().find(entry => entry.index === nav.currentEntry.index - 1);
      return previous?.getState()?.readingLink?.url === location.href;
    }
    return history.length > 1 && document.referrer.startsWith(home);
  }

  document.addEventListener('click', event => {
    if (event.defaultPrevented || event.button !== 0 || event.metaKey ||
        event.ctrlKey || event.shiftKey || event.altKey) return;
    const link = event.target.closest?.('a[href]');
    if (!link || link.origin !== location.origin || link.target === '_blank') return;
    if (link.hasAttribute('data-close')) {
      closing = true;
      if (canGoBack(link.href)) {
        event.preventDefault();
        history.back();
      }
      return;
    }
    if (!link.closest('main') || link.pathname === location.pathname) return;
    const readingLink = { url: link.href, index: links().indexOf(link), y: scrollY };
    const nav = window.navigation;
    if (nav?.updateCurrentEntry) {
      nav.updateCurrentEntry({ state: { ...nav.currentEntry.getState(), readingLink } });
    } else {
      history.replaceState({ ...history.state, readingLink }, '');
    }
  });

  function snapshot(element, transition) {
    if (!element || reduced()) { transition.skipTransition(); return; }
    element.style.viewTransitionName = 'reading-selection';
    const clear = () => { element.style.viewTransitionName = ''; };
    transition.finished.then(clear, clear);
  }

  addEventListener('pageswap', event => {
    if (!event.viewTransition) return;
    const goingBack = event.activation?.navigationType === 'traverse' &&
      event.activation.entry.index < event.activation.from.index;
    snapshot(closing || goingBack ? heading() : openingLink(event.activation?.entry?.url),
      event.viewTransition);
  });

  function returnTarget() {
    const activation = window.navigation?.activation;
    const from = activation?.from;
    if (!from?.url) return;
    const back = activation.navigationType === 'traverse' &&
      activation.entry.index < from.index;
    if (!back && !document.body?.classList.contains('argument-page')) return;
    const link = openingLink(from.url);
    if (link) {
      const saved = savedLink();
      if (saved?.url === from.url) scrollTo(0, saved.y);
      else link.scrollIntoView({ block: 'center' });
      link.focus({ preventScroll: true });
    }
    return link;
  }

  addEventListener('pagereveal', event => {
    closing = false;
    const target = returnTarget();
    if (event.viewTransition) snapshot(target || heading(), event.viewTransition);
  });
  addEventListener('pageshow', () => {
    closing = false;
    if (!('onpagereveal' in window)) returnTarget();
  });
})();
