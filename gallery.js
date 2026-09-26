(() => {
  const gallery = document.querySelector('.gallery-grid');
  const dialog = document.getElementById('numazu-lightbox');
  if (!gallery || !dialog || typeof dialog.showModal !== 'function') return;

  const links = [...gallery.querySelectorAll('a')];
  const image = dialog.querySelector('.lightbox-image');
  const caption = dialog.querySelector('.lightbox-caption');
  const count = dialog.querySelector('.lightbox-count');
  const close = dialog.querySelector('.lightbox-close');
  let current = 0;
  let opener = null;
  let touchStart = null;

  function show(index) {
    current = (index + links.length) % links.length;
    const link = links[current];
    image.src = link.href;
    image.alt = link.querySelector('img').alt;
    caption.textContent = image.alt;
    count.textContent = `${current + 1} / ${links.length}`;
  }

  links.forEach((link, index) => link.addEventListener('click', event => {
    event.preventDefault();
    opener = link;
    show(index);
    dialog.showModal();
    close.focus();
  }));
  dialog.querySelector('.lightbox-prev').addEventListener('click', () => show(current - 1));
  dialog.querySelector('.lightbox-next').addEventListener('click', () => show(current + 1));
  close.addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => {
    if (event.target === dialog) dialog.close();
  });
  dialog.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault();
      show(current + (event.key === 'ArrowRight' ? 1 : -1));
    }
  });
  dialog.addEventListener('touchstart', event => {
    touchStart = event.touches.length === 1 ? event.touches[0].clientX : null;
  }, { passive: true });
  dialog.addEventListener('touchend', event => {
    if (touchStart === null || event.changedTouches.length !== 1) return;
    const distance = event.changedTouches[0].clientX - touchStart;
    touchStart = null;
    if (Math.abs(distance) > 50) show(current + (distance < 0 ? 1 : -1));
  }, { passive: true });
  dialog.addEventListener('close', () => {
    image.removeAttribute('src');
    opener?.focus();
  });
})();
