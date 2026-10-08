// Native disclosure menus also work without JavaScript.
(() => {
 const header = document.querySelector('.organized-header');
 if (!header) return;
 const menus = [...header.querySelectorAll('details')];
 menus.forEach(menu => menu.addEventListener('toggle', () => {
  if (menu.open) menus.forEach(other => { if (other !== menu) other.open = false; });
 }));
 document.addEventListener('click', event => {
  menus.forEach(menu => { if (!menu.contains(event.target)) menu.open = false; });
 });
 document.addEventListener('keydown', event => {
  if (event.key !== 'Escape') return;
  const menu = menus.find(item => item.open);
  if (menu) { menu.open = false; menu.querySelector('summary').focus(); }
 });
 header.addEventListener('focusout', () => {
  setTimeout(() => menus.forEach(menu => {
   if (!menu.contains(document.activeElement)) menu.open = false;
  }), 0);
 });
})();
