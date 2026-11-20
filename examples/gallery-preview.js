(() => {
  const button = document.querySelector('.preview-motion');
  const spanish = document.documentElement.lang === 'es';
  button.addEventListener('click', () => {
    const paused = document.body.classList.toggle('gallery-paused');
    button.setAttribute('aria-pressed', String(paused));
    button.textContent = spanish
      ? (paused ? 'Activar efectos al señalar' : 'Pausar efectos al señalar')
      : (paused ? 'Enable hover effects' : 'Pause hover effects');
  });
})();
