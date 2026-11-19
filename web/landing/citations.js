/* Copy only on an explicit button click; retain a selectable fallback. */
document.querySelectorAll('[data-copy]').forEach(button => {
  button.addEventListener('click', async () => {
    const source = document.getElementById(button.dataset.copy);
    const status = document.getElementById('copy-status');
    try {
      await navigator.clipboard.writeText(source.textContent.trim());
      status.textContent = button.dataset.copy.startsWith('bib-') ? 'BibTeX copied.' : 'Reference copied.';
    } catch {
      const range = document.createRange(); range.selectNodeContents(source);
      const selection = window.getSelection(); selection.removeAllRanges(); selection.addRange(range);
      status.textContent = 'Reference selected. Press Ctrl+C or ⌘C to copy.';
    }
  });
});
