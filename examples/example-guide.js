/* Show the values of the controls that are already used by each demonstration. */
(() => {
  const controls = [];
  document.querySelectorAll('input[type="range"]').forEach(input => {
    // Group P and the tangent demo already have dedicated, contextual readouts.
    if (document.querySelector('.source-tools') || document.getElementById('neighborhood')) return;
    const label = input.closest('label'); if (!label) return;
    const output = document.createElement('output');
    output.className = 'control-live'; output.setAttribute('for', input.id);
    label.append(output); controls.push({input, output});
  });
  function update() {
    for (const {input, output} of controls) {
      output.textContent = input.value + (input.dataset.displayUnit || '');
    }
  }
  document.addEventListener('input', update);
  document.addEventListener('change', update);
  document.addEventListener('click', () => queueMicrotask(update));
  update();
})();
