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

  /* ---------- Compteurs animés (métriques) ---------- */

  function animateCounter(el, to, suffix, duration) {
    var start = null;
    function tick(now) {
      if (start === null) start = now;
      var progress = Math.min((now - start) / duration, 1);
      var eased = 1 - Math.pow(1 - progress, 3);
      el.textContent = Math.round(eased * to) + suffix;
      if (progress < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  function setupCounters(root) {
    var els = (root || document).querySelectorAll('[data-counter]:not([data-counted])');
    if (!els.length) return;

    if (reducedMotion || !('IntersectionObserver' in window)) {
      els.forEach(function (el) { el.setAttribute('data-counted', ''); });
      return;
    }

    var observer = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        obs.unobserve(el);
        el.setAttribute('data-counted', '');
        animateCounter(el, parseInt(el.dataset.counterTarget, 10), el.dataset.counterSuffix, 1400);
      });
    }, { threshold: 0.4 });

    els.forEach(function (el) {
      var match = /^(\d+)(.*)$/.exec(el.textContent.trim());
      if (!match) return;
      el.dataset.counterTarget = match[1];
      el.dataset.counterSuffix = match[2];
      el.textContent = '0' + match[2];
      observer.observe(el);
    });
  }

  /* ---------- Particules ambiantes (portrait hero) ---------- */

  function setupHeroParticles() {
    var canvas = document.getElementById('hero-particles');
    if (!canvas || !canvas.getContext) return;
    var ctx = canvas.getContext('2d');

    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var width = 0, height = 0, particles = [], raf = null, running = false;

    var COUNT_DENSITY = 11000;   // px² par particule
    var MAX_COUNT = 46;
    var LINK_DIST = 110;
    var SPEED = 0.12;

    function resize() {
      var parent = canvas.parentElement;
      var parentRect = parent.getBoundingClientRect();
      var bleed = window.innerWidth >= 640
        ? parseInt(canvas.dataset.bleedSm, 10) || 64
        : parseInt(canvas.dataset.bleed, 10) || 40;

      width = parentRect.width + bleed * 2;
      height = parentRect.height + bleed * 2;
      canvas.style.left = (-bleed) + 'px';
      canvas.style.top = (-bleed) + 'px';
      canvas.style.width = width + 'px';
      canvas.style.height = height + 'px';
      canvas.width = Math.round(width * dpr);
      canvas.height = Math.round(height * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

      var count = Math.min(MAX_COUNT, Math.round((width * height) / COUNT_DENSITY));
      particles = [];
      for (var i = 0; i < count; i++) {
        particles.push({
          x: Math.random() * width,
          y: Math.random() * height,
          vx: (Math.random() - 0.5) * SPEED,
          vy: (Math.random() - 0.5) * SPEED,
          r: 0.8 + Math.random() * 1.4
        });
      }
    }

    function step() {
      ctx.clearRect(0, 0, width, height);

      for (var i = 0; i < particles.length; i++) {
        var p = particles[i];
        p.x += p.vx;
        p.y += p.vy;
        if (p.x < -10) p.x = width + 10; else if (p.x > width + 10) p.x = -10;
        if (p.y < -10) p.y = height + 10; else if (p.y > height + 10) p.y = -10;
      }

      for (var a = 0; a < particles.length; a++) {
        for (var b = a + 1; b < particles.length; b++) {
          var dx = particles[a].x - particles[b].x;
          var dy = particles[a].y - particles[b].y;
          var dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < LINK_DIST) {
            ctx.strokeStyle = 'rgba(255,255,255,' + (0.12 * (1 - dist / LINK_DIST)).toFixed(3) + ')';
            ctx.lineWidth = 1;
            ctx.beginPath();
            ctx.moveTo(particles[a].x, particles[a].y);
            ctx.lineTo(particles[b].x, particles[b].y);
            ctx.stroke();
          }
        }
      }

      ctx.fillStyle = 'rgba(255,255,255,0.45)';
      for (var j = 0; j < particles.length; j++) {
        var pt = particles[j];
        ctx.beginPath();
        ctx.arc(pt.x, pt.y, pt.r, 0, Math.PI * 2);
        ctx.fill();
      }

      if (running) raf = requestAnimationFrame(step);
    }

    function start() {
      if (running) return;
      running = true;
      raf = requestAnimationFrame(step);
    }

    function stop() {
      running = false;
      if (raf) cancelAnimationFrame(raf);
      raf = null;
    }

    resize();

    if (reducedMotion) {
      step(); // une seule image statique, pas de boucle
    } else {
      start();

      if ('IntersectionObserver' in window) {
        new IntersectionObserver(function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) start(); else stop();
          });
        }, { threshold: 0.05 }).observe(canvas);
      }

      document.addEventListener('visibilitychange', function () {
        if (document.hidden) stop(); else if (!document.hidden) start();
      });

      var resizeTimer;
      window.addEventListener('resize', function () {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(resize, 200);
      }, { passive: true });
    }
  }

  /* ---------- Vidéos décoratives en autoplay (respecte reduced-motion, pause hors écran) ---------- */

  function setupAmbientVideos(root) {
    var videos = (root || document).querySelectorAll('video[autoplay]');
    if (!videos.length) return;

    videos.forEach(function (video) {
      if (reducedMotion) {
        video.removeAttribute('autoplay');
        video.pause();
        return;
      }
      if ('IntersectionObserver' in window) {
        new IntersectionObserver(function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) video.play().catch(function () {});
            else video.pause();
          });
        }, { threshold: 0.15 }).observe(video);
      }
    });
  }

  /* ---------- Animation de saisie de code (carte "Développement Web") ---------- */

  function setupCodeTypewriter(root) {
    var container = (root || document).querySelector('[data-typewriter]');
    if (!container || reducedMotion) return;

    var CODE_LINES = [
      { indent: 0, segs: [{ t: '// Django Service Architecture', c: 'text-white/20' }] },
      { indent: 0, segs: [{ t: 'class ', c: 'text-white/60' }, { t: 'EnterpriseService', c: 'text-white' }, { t: '(models.Model):' }] },
      { indent: 2, segs: [{ t: 'name = models.CharField(max_length=255)' }] },
      { indent: 2, segs: [{ t: 'stack = [' }, { t: '"Django"', c: 'text-emerald-300' }, { t: ', ' }, { t: '"HTMX"', c: 'text-cyan' }, { t: ', ' }, { t: '"MySQL"', c: 'text-white' }, { t: ']' }] },
      { indent: 2, segs: [{ t: 'latency_ms = models.FloatField(default=12.4)' }] },
      { indent: 2, segs: [{ t: 'uptime = models.DecimalField(default=99.98)' }] },
      { indent: 0, segs: [{ t: '' }] },
      { indent: 2, segs: [{ t: 'def ', c: 'text-white/60' }, { t: 'deploy', c: 'text-white' }, { t: '(self):' }] },
      { indent: 4, segs: [{ t: 'return', c: 'text-white/60' }, { t: ' self.build_production_release()' }] }
    ];

    function escapeHtml(s) {
      return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }

    function indentHtml(n) {
      return '&nbsp;&nbsp;'.repeat(n / 2);
    }

    var running = false;

    function typeLoop() {
      if (running) return;
      running = true;
      var lineIndex = 0, segIndex = 0, charIndex = 0, html = '';

      function tick() {
        if (lineIndex >= CODE_LINES.length) {
          setTimeout(function () {
            lineIndex = 0; segIndex = 0; charIndex = 0; html = '';
            setTimeout(tick, 500);
          }, 2400);
          return;
        }
        var line = CODE_LINES[lineIndex];
        if (segIndex === 0 && charIndex === 0) html += indentHtml(line.indent);
        if (segIndex >= line.segs.length) {
          html += '<br>';
          lineIndex++; segIndex = 0; charIndex = 0;
          setTimeout(tick, 110);
          return;
        }
        var seg = line.segs[segIndex];
        charIndex++;
        var partial = escapeHtml(seg.t.slice(0, charIndex));
        var currentLine = seg.c ? '<span class="' + seg.c + '">' + partial + '</span>' : partial;
        container.innerHTML = html + currentLine + '<span class="typewriter-cursor"></span>';
        if (charIndex >= seg.t.length) {
          html += seg.c ? '<span class="' + seg.c + '">' + escapeHtml(seg.t) + '</span>' : escapeHtml(seg.t);
          segIndex++; charIndex = 0;
        }
        setTimeout(tick, 16 + Math.random() * 26);
      }
      tick();
    }

    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries, obs) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          typeLoop();
          obs.disconnect();
        });
      }, { threshold: 0.2 }).observe(container);
    } else {
      typeLoop();
    }
  }

  /* ---------- Interaction magnétique (CTA principaux) ---------- */

  function setupMagnetic(root) {
    if (reducedMotion || !window.matchMedia('(pointer: fine)').matches) return;
    var items = (root || document).querySelectorAll('[data-magnetic]:not([data-magnetized])');
    if (!items.length) return;

    items.forEach(function (el) {
      el.setAttribute('data-magnetized', '');
      var strength = parseFloat(el.dataset.magnetic) || 0.25;

      el.addEventListener('mousemove', function (e) {
        var rect = el.getBoundingClientRect();
        var x = (e.clientX - rect.left - rect.width / 2) * strength;
        var y = (e.clientY - rect.top - rect.height / 2) * strength;
        el.style.transform = 'translate(' + x.toFixed(1) + 'px, ' + y.toFixed(1) + 'px)';
      });

      el.addEventListener('mouseleave', function () {
        el.style.transform = '';
      });
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
    var links = document.querySelectorAll('.nav-link[href*="#"]');
    if (!sections.length || !('IntersectionObserver' in window)) return;

    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        links.forEach(function (link) {
          var hash = link.getAttribute('href').split('#')[1];
          link.classList.toggle('active', hash === entry.target.id);
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

  /* ---------- Init ---------- */

  document.addEventListener('DOMContentLoaded', function () {
    setupReveals(document);
    setupCounters(document);
    setupMagnetic(document);
    setupHeroParticles();
    setupAmbientVideos(document);
    setupCodeTypewriter(document);
    setupNav();
    setupFilters();
    setupModal();

    // Ré-applique le reveal / compteurs aux éléments injectés par HTMX (filtres projets)
    document.body.addEventListener('htmx:afterSettle', function (event) {
      setupReveals(event.detail.target);
      setupCounters(event.detail.target);
    });
  });
})();
