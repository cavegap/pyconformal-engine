/* Native links work without JavaScript. Storage is an optional convenience. */
(() => {
  const current = document.documentElement.lang;
  const explicit = new URL(location.href).searchParams.get('lang');
  let preferred = explicit === 'es' || explicit === 'en' ? explicit : null;
  try {
    if (explicit === 'es' || explicit === 'en') localStorage.setItem('pyconformal-language', explicit);
    preferred = preferred || localStorage.getItem('pyconformal-language');
  } catch { /* Browsing with storage blocked remains fully usable. */ }
  document.addEventListener('DOMContentLoaded', () => {
    const links = document.querySelectorAll('.language-picker a');
    for (const link of links) {
      const destination = link.getAttribute('href').split('#')[0];
      link.setAttribute('href', destination + location.hash);
      link.addEventListener('click', () => {
        try { localStorage.setItem('pyconformal-language', link.lang); } catch { /* optional */ }
      });
    }
    if (preferred && preferred !== current) {
      const link = [...links].find(item => item.lang === preferred);
      if (link) location.replace(link.href);
    }
  });
})();
