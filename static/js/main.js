/* Azeez portfolio — vanilla JS : reveal au scroll, nav, modal. Aucune dépendance. */
(function () {
  'use strict';

  var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Reveal au scroll (IntersectionObserver) ---------- */

  function setupReveals(root) {
    if (reducedMotion || !('IntersectionObserver' in window)) return;
    var items = (root || document).querySelectorAll('[data-reveal]:not(.revealed):not(.reveal-pending)');
    if (!items.length) return;

    var observer = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('revealed');
        obs.unobserve(entry.target);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

    items.forEach(function (el) {
      // Déjà dans le viewport au chargement : ne pas masquer, laisser tel quel.
      var rect = el.getBoundingClientRect();
      if (rect.top < window.innerHeight * 0.92) return;
      el.classList.add('reveal-pending');
      el.style.setProperty('--stagger', el.dataset.stagger || 0);
      observer.observe(el);
    });
  }

  /* ---------- Navigation : état scrolled + menu mobile + scrollspy ---------- */

  function setupNav() {
    var nav = document.getElementById('navbar');
    if (!nav) return;

    var onScroll = function () {
      nav.classList.toggle('scrolled', window.scrollY > 24);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });

    var burger = document.getElementById('nav-burger');
    var menu = document.getElementById('nav-mobile');
    if (burger && menu) {
      burger.addEventListener('click', function () {
        var open = menu.classList.toggle('hidden') === false;
        burger.setAttribute('aria-expanded', String(open));
        document.querySelectorAll('#nav-burger svg').forEach(function (icon) {
          icon.classList.toggle('hidden');
        });
      });
      menu.querySelectorAll('a').forEach(function (link) {
        link.addEventListener('click', function () {
          menu.classList.add('hidden');
          burger.setAttribute('aria-expanded', 'false');
          document.querySelectorAll('#nav-burger svg').forEach(function (icon) {
            icon.classList.toggle('hidden');
          });
        });
      });
    }

    // Scrollspy : souligne le lien de la section visible
    var sections = document.querySelectorAll('main section[id]');
    var links = document.querySelectorAll('.nav-link[href^="#"]');
    if (!sections.length || !('IntersectionObserver' in window)) return;

    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        links.forEach(function (link) {
          link.classList.toggle('active', link.getAttribute('href') === '#' + entry.target.id);
        });
      });
    }, { rootMargin: '-38% 0px -55% 0px' });

    sections.forEach(function (section) { spy.observe(section); });
  }

  /* ---------- Onglets de filtre projets (état actif) ---------- */

  function setupFilters() {
    document.querySelectorAll('.filter-tab').forEach(function (tab) {
      tab.addEventListener('click', function () {
        document.querySelectorAll('.filter-tab').forEach(function (other) {
          other.classList.toggle('is-active', other === tab);
        });
      });
    });
  }

  /* ---------- Modal HTMX (détail projet) ---------- */

  function setupModal() {
    var root = document.getElementById('modal-root');
    if (!root) return;

    function close() {
      root.innerHTML = '';
      document.body.classList.remove('modal-open');
    }

    root.addEventListener('click', function (event) {
      if (event.target.closest('[data-modal-close]')) { close(); return; }
      // Clic sur le backdrop (hors panneau)
      if (event.target.classList.contains('modal-backdrop')) close();
    });

    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && root.firstElementChild) close();
    });

    document.body.addEventListener('htmx:afterSwap', function (event) {
      if (event.detail.target === root && root.firstElementChild) {
        document.body.classList.add('modal-open');
        var closeBtn = root.querySelector('[data-modal-close]');
        if (closeBtn) closeBtn.focus();
      }
    });
  }

  /* ---------- Theme Toggle (Light / Dark) ---------- */

  function setupThemeToggle() {
    var toggles = document.querySelectorAll('#theme-toggle, #theme-toggle-mobile, [data-theme-toggle]');
    if (!toggles.length) return;

    function applyTheme(theme) {
      if (theme === 'light') {
        document.documentElement.classList.add('light');
        document.documentElement.classList.remove('dark');
      } else {
        document.documentElement.classList.add('dark');
        document.documentElement.classList.remove('light');
      }
      try {
        localStorage.setItem('theme', theme);
      } catch (e) {}
      updateIcons();
    }

    function updateIcons() {
      var isLight = document.documentElement.classList.contains('light');
      document.querySelectorAll('.theme-icon-dark').forEach(function (el) {
        el.style.display = isLight ? 'none' : 'inline-block';
      });
      document.querySelectorAll('.theme-icon-light').forEach(function (el) {
        el.style.display = isLight ? 'inline-block' : 'none';
      });
    }

    toggles.forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        var current = document.documentElement.classList.contains('light') ? 'light' : 'dark';
        var next = current === 'light' ? 'dark' : 'light';
        applyTheme(next);
      });
    });

    updateIcons();
  }

  /* ---------- Init ---------- */

  document.addEventListener('DOMContentLoaded', function () {
    setupThemeToggle();
    setupReveals(document);
    setupNav();
    setupFilters();
    setupModal();

    // Ré-applique le reveal aux éléments injectés par HTMX (filtres projets)
    document.body.addEventListener('htmx:afterSettle', function (event) {
      setupReveals(event.detail.target);
    });
  });
})();
