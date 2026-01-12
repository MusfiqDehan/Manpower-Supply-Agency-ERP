/**
 * Modern Theme Manager for Manpower Supply Agency ERP
 * Handles dark/light theme switching and persistence
 */

class ThemeManager {
  constructor() {
    this.themeKey = 'msa-theme';
    this.currentTheme = this.getStoredTheme() || 'light';
    this.init();
  }

  init() {
    // Apply stored theme on page load
    this.applyTheme(this.currentTheme);
    
    // Create theme toggle button
    this.createToggleButton();
    
    // Listen for system theme changes
    this.watchSystemTheme();
  }

  getStoredTheme() {
    return localStorage.getItem(this.themeKey);
  }

  setStoredTheme(theme) {
    localStorage.setItem(this.themeKey, theme);
  }

  applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    this.currentTheme = theme;
    this.setStoredTheme(theme);
    this.updateToggleButton();
  }

  toggleTheme() {
    const newTheme = this.currentTheme === 'light' ? 'dark' : 'light';
    this.applyTheme(newTheme);
    
    // Smooth transition effect
    document.body.style.transition = 'background-color 0.3s ease, color 0.3s ease';
  }

  createToggleButton() {
    // Check if button already exists
    if (document.querySelector('.theme-toggle')) {
      return;
    }

    const button = document.createElement('button');
    button.className = 'theme-toggle';
    button.setAttribute('aria-label', 'Toggle theme');
    button.setAttribute('title', 'Toggle dark/light theme');
    
    button.addEventListener('click', () => this.toggleTheme());
    
    document.body.appendChild(button);
    this.updateToggleButton();
  }

  updateToggleButton() {
    const button = document.querySelector('.theme-toggle');
    if (!button) return;
    
    if (this.currentTheme === 'dark') {
      button.innerHTML = '<i class="fas fa-sun"></i>';
      button.setAttribute('title', 'Switch to light mode');
    } else {
      button.innerHTML = '<i class="fas fa-moon"></i>';
      button.setAttribute('title', 'Switch to dark mode');
    }
  }

  watchSystemTheme() {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    
    // Only auto-switch if user hasn't manually set a theme
    if (!this.getStoredTheme()) {
      this.applyTheme(mediaQuery.matches ? 'dark' : 'light');
    }
    
    mediaQuery.addEventListener('change', (e) => {
      if (!this.getStoredTheme()) {
        this.applyTheme(e.matches ? 'dark' : 'light');
      }
    });
  }
}

// Initialize theme manager when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    window.themeManager = new ThemeManager();
  });
} else {
  window.themeManager = new ThemeManager();
}
