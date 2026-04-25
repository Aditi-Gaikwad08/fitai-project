// main.js — shared UI behaviours

// Highlight nav link for current page (already done via Jinja,
// but this handles any edge cases)
document.querySelectorAll('.nav-links a').forEach(link => {
  if (link.href === window.location.href) {
    link.classList.add('active');
  }
});
