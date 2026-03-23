/* ================================================================
   MEDIC ADRENALINE — Portfolio JavaScript
   Features:
   - Dark/Light mode toggle (persists via localStorage)
   - Hero canvas particle network animation
   - Typewriter / typing effect for hero tagline
   - Sticky navbar with active-section highlighting
   - Mobile hamburger menu
   - Scroll-triggered reveal animations
   - Animated skill progress bars (triggered on scroll)
   - Contact form submission handler
   ================================================================ */


/* ── 1. DOM REFERENCES ─────────────────────────────────────────── */
const html         = document.documentElement;
const navbar       = document.getElementById('navbar');
const themeToggle  = document.getElementById('themeToggle');
const themeIcon    = document.getElementById('themeIcon');
const hamburger    = document.getElementById('hamburger');
const mobileMenu   = document.getElementById('mobileMenu');
const navLinks     = document.querySelectorAll('.nav-link');
const sections     = document.querySelectorAll('section[id]');
const revealEls    = document.querySelectorAll('.reveal');
const skillItems   = document.querySelectorAll('.skill-item');
const contactForm  = document.getElementById('contactForm');
const formSuccess  = document.getElementById('formSuccess');
const canvas       = document.getElementById('heroCanvas');


/* ── 2. DARK / LIGHT MODE TOGGLE ──────────────────────────────── */

/**
 * Apply a theme to the <html> element and persist it.
 * @param {'dark'|'light'} theme
 */
function applyTheme(theme) {
  html.setAttribute('data-theme', theme);
  localStorage.setItem('theme', theme);

  // Swap icon: moon for dark mode, sun for light mode
  themeIcon.className = theme === 'dark'
    ? 'fa-solid fa-moon'
    : 'fa-solid fa-sun';
}

// Init: load saved preference (or default to dark)
applyTheme(localStorage.getItem('theme') || 'dark');

// Toggle on button click
themeToggle.addEventListener('click', () => {
  const next = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
  applyTheme(next);
});


/* ── 3. HAMBURGER / MOBILE MENU ───────────────────────────────── */
hamburger.addEventListener('click', () => {
  const isOpen = hamburger.classList.toggle('open');
  mobileMenu.classList.toggle('open', isOpen);
  hamburger.setAttribute('aria-expanded', isOpen);
});

// Close mobile menu when a link is tapped
document.querySelectorAll('.mob-link').forEach(link => {
  link.addEventListener('click', () => {
    hamburger.classList.remove('open');
    mobileMenu.classList.remove('open');
  });
});


/* ── 4. STICKY NAVBAR + ACTIVE SECTION HIGHLIGHT ─────────────── */

/**
 * On scroll:
 *  • Add `.scrolled` class to navbar once user scrolls past 60px
 *  • Highlight the nav link whose corresponding section is in view
 */
function onScroll() {
  // Scrolled class for blur background
  navbar.classList.toggle('scrolled', window.scrollY > 60);

  // Active section detection
  let current = '';
  sections.forEach(sec => {
    const top = sec.offsetTop - 120;      // offset for nav height
    if (window.scrollY >= top) current = sec.id;
  });

  navLinks.forEach(link => {
    link.classList.toggle(
      'active',
      link.getAttribute('href') === `#${current}`
    );
  });
}

window.addEventListener('scroll', onScroll, { passive: true });
onScroll(); // run once on load


/* ── 5. SCROLL-TRIGGERED REVEAL ANIMATIONS ────────────────────── */

/**
 * IntersectionObserver adds `.visible` to elements as they enter
 * the viewport, triggering CSS fade-up transitions.
 */
const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        // Stagger siblings within the same parent grid/flex
        const siblings = entry.target.parentElement.querySelectorAll('.reveal');
        let delay = 0;
        siblings.forEach((sib, idx) => {
          if (sib === entry.target) delay = idx * 80;
        });
        setTimeout(() => entry.target.classList.add('visible'), delay);
        revealObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.12 }
);

revealEls.forEach(el => revealObserver.observe(el));


/* ── 6. ANIMATED SKILL PROGRESS BARS ─────────────────────────── */

/**
 * When a skill card enters view, animate each bar to its target width.
 * The width is read from the parent `.skill-item`'s `data-level` attribute.
 */
const skillObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const card = entry.target;
        card.querySelectorAll('.skill-item').forEach((item, i) => {
          const level = item.getAttribute('data-level') || '0';
          const fill  = item.querySelector('.skill-fill');
          setTimeout(() => {
            fill.style.width = `${level}%`;
          }, i * 120 + 200); // stagger each bar
        });
        skillObserver.unobserve(card);
      }
    });
  },
  { threshold: 0.3 }
);

document.querySelectorAll('.skill-card').forEach(card => skillObserver.observe(card));


/* ── 7. HERO TYPING EFFECT ────────────────────────────────────── */

const typingEl    = document.getElementById('typingText');
const typingWords = [
  'Medical Student',
  'Python Developer',
  'AI Enthusiast',
  'Web Developer',
  'Bot Builder',
  'Problem Solver',
];

let wordIndex = 0;
let charIndex = 0;
let isDeleting = false;

/**
 * Recursive typewriter function:
 *  - Types each word character by character
 *  - Pauses at end of word, then deletes
 *  - Cycles through the words list
 */
function typeWriter() {
  const word = typingWords[wordIndex];

  if (!isDeleting) {
    // Add next character
    typingEl.textContent = word.slice(0, charIndex + 1);
    charIndex++;

    if (charIndex === word.length) {
      // Finished typing — pause, then start deleting
      setTimeout(() => { isDeleting = true; typeWriter(); }, 1600);
      return;
    }
  } else {
    // Remove last character
    typingEl.textContent = word.slice(0, charIndex - 1);
    charIndex--;

    if (charIndex === 0) {
      // Finished deleting — move to next word
      isDeleting = false;
      wordIndex = (wordIndex + 1) % typingWords.length;
    }
  }

  const speed = isDeleting ? 55 : 90;
  setTimeout(typeWriter, speed);
}

// Start typing after hero animation completes
setTimeout(typeWriter, 1200);


/* ── 8. HERO CANVAS — PARTICLE NETWORK ───────────────────────── */

/**
 * Minimal particle network that draws dots connected by lines
 * when close enough. Renders on the hero section's <canvas>.
 */
(function initCanvas() {
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  let W, H, particles;
  const COUNT     = 70;
  const MAX_DIST  = 140;
  const SPEED     = 0.4;

  // Resize handler — fills the canvas to window size
  function resize() {
    W = canvas.width  = canvas.offsetWidth;
    H = canvas.height = canvas.offsetHeight;
  }

  // Create particles with random position and velocity
  function createParticles() {
    particles = Array.from({ length: COUNT }, () => ({
      x:  Math.random() * W,
      y:  Math.random() * H,
      vx: (Math.random() - 0.5) * SPEED,
      vy: (Math.random() - 0.5) * SPEED,
      r:  Math.random() * 2 + 1,
    }));
  }

  // Get the current theme accent color
  function getAccent() {
    return getComputedStyle(html).getPropertyValue('--accent').trim() || '#00e5ff';
  }

  // Main draw loop
  function draw() {
    ctx.clearRect(0, 0, W, H);

    const accent = getAccent();

    // Move + bounce particles
    particles.forEach(p => {
      p.x += p.vx;
      p.y += p.vy;
      if (p.x < 0 || p.x > W) p.vx *= -1;
      if (p.y < 0 || p.y > H) p.vy *= -1;

      // Draw dot
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = accent;
      ctx.globalAlpha = 0.6;
      ctx.fill();
    });

    // Draw connecting lines
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx   = particles[i].x - particles[j].x;
        const dy   = particles[i].y - particles[j].y;
        const dist = Math.hypot(dx, dy);

        if (dist < MAX_DIST) {
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = accent;
          ctx.globalAlpha = (1 - dist / MAX_DIST) * 0.3;
          ctx.lineWidth   = 0.8;
          ctx.stroke();
        }
      }
    }

    ctx.globalAlpha = 1;
    requestAnimationFrame(draw);
  }

  // Pause animation when tab is hidden (performance)
  document.addEventListener('visibilitychange', () => {
    if (!document.hidden) requestAnimationFrame(draw);
  });

  // Init
  resize();
  createParticles();
  requestAnimationFrame(draw);

  const ro = new ResizeObserver(() => { resize(); createParticles(); });
  ro.observe(canvas.parentElement);
})();


/* ── 9. CONTACT FORM ──────────────────────────────────────────── */

/**
 * Prevent default submission, show a success message.
 * In production: replace with a real backend call or Formspree/EmailJS.
 */
if (contactForm) {
  contactForm.addEventListener('submit', (e) => {
    e.preventDefault();

    const btn = contactForm.querySelector('button[type="submit"]');
    btn.textContent = 'Sending…';
    btn.disabled    = true;

    // Simulate network delay
    setTimeout(() => {
      contactForm.reset();
      btn.innerHTML = 'Send Message <i class="fa-solid fa-paper-plane"></i>';
      btn.disabled  = false;
      formSuccess.classList.add('show');

      setTimeout(() => formSuccess.classList.remove('show'), 5000);
    }, 1200);
  });
}
/* ── 10. SMOOTH SCROLL FOR ALL ANCHOR LINKS ───────────────────── */

/**
 * Intercept every <a href="#..."> click and smoothly scroll to the target,
 * accounting for the fixed navbar height.
 */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', (e) => {
    const targetId = anchor.getAttribute('href').slice(1);
    const target   = document.getElementById(targetId);
    if (!target) return;

    e.preventDefault();
    const navH   = navbar.offsetHeight;
    const top    = target.getBoundingClientRect().top + window.scrollY - navH;
    window.scrollTo({ top, behavior: 'smooth' });
  });
});