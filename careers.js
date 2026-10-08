const form = document.querySelector('#talent-application');
form?.addEventListener('submit', (event) => {
  event.preventDefault();
  if (!form.reportValidity()) return;
  const data = new FormData(form);
  const body = ['Aurora Publishing — Talent Network Expression of Interest',
    ...['name', 'email', 'discipline', 'location', 'languages', 'portfolio', 'availability', 'rate', 'notes'].map(key => `${key}: ${data.get(key) || 'Not provided'}`),
    'Consent: I agree to Aurora reviewing this information and contacting me about relevant opportunities.'].join('\n\n');
  const subject = `Aurora Talent Network — ${data.get('discipline')} — ${data.get('name')}`;
  window.location.href = `mailto:publishing@aurora-studio.org?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
  document.querySelector('#application-status').hidden = false;
});
