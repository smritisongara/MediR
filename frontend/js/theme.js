/**
 * MediR AI - Theme Manager
 * Supports Green Healthcare Light Mode & Dark Mode + System Preference Auto-detection
 */

function initThemeSystem() {
  const savedTheme = localStorage.getItem('medir_theme');
  
  if (savedTheme) {
    applyTheme(savedTheme);
  } else {
    // Detect system theme
    const systemPrefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    applyTheme(systemPrefersDark ? 'dark' : 'light');
  }

  // Listen for system theme changes if user has not explicitly locked a preference
  if (window.matchMedia) {
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
      if (!localStorage.getItem('medir_theme')) {
        applyTheme(e.matches ? 'dark' : 'light');
      }
    });
  }
}

function applyTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('medir_theme', theme);
  updateThemeIcons(theme);

  // Sync with backend user preference endpoint if logged in
  fetch('/api/auth/preferences', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ theme: theme })
  }).catch(() => {});
}

function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme') || 'light';
  const newTheme = current === 'dark' ? 'light' : 'dark';
  applyTheme(newTheme);
}

function updateThemeIcons(theme) {
  document.querySelectorAll('#themeToggleIcon, .theme-toggle-icon').forEach(icon => {
    if (theme === 'dark') {
      icon.className = 'bi bi-sun-fill text-warning theme-toggle-icon';
    } else {
      icon.className = 'bi bi-moon-stars-fill text-success theme-toggle-icon';
    }
  });
}

document.addEventListener('DOMContentLoaded', initThemeSystem);
