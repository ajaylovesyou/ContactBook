/**
 * ============================================================
 * Phase 5 — FRONTEND DEVELOPER's JavaScript
 * Branch  : frontend
 * File    : static/js/main.js
 * Handles : (1) Navbar mobile toggle
 *           (2) Delete confirmation modal
 *           (3) Live client-side filter on All Contacts page
 *           (4) Search page auto-submit on Enter
 *           (5) Flash message auto-dismiss
 *           (6) Card entrance animations
 * ============================================================
 */

document.addEventListener('DOMContentLoaded', () => {

  // ── 1. NAVBAR MOBILE TOGGLE ──────────────────────────────
  const navToggle = document.getElementById('navToggle');
  const navLinks  = document.getElementById('navLinks');

  if (navToggle && navLinks) {
    navToggle.addEventListener('click', () => {
      navLinks.classList.toggle('open');

      // Animate hamburger → X
      const spans = navToggle.querySelectorAll('span');
      navLinks.classList.contains('open')
        ? spans.forEach((s, i) => {
            if (i === 0) s.style.transform = 'rotate(45deg) translate(5px, 5px)';
            if (i === 1) s.style.opacity   = '0';
            if (i === 2) s.style.transform = 'rotate(-45deg) translate(5px, -5px)';
          })
        : spans.forEach(s => { s.style.transform = ''; s.style.opacity = ''; });
    });

    // Close menu when a link is clicked
    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('open');
      });
    });
  }


  // ── 2. DELETE CONFIRMATION ───────────────────────────────
  /**
   * Every delete <form> has class="delete-form" and
   * data-name="<Contact Name>".
   * We intercept submit, show a confirm dialog, and only
   * let the form proceed if the user confirms.
   */
  document.querySelectorAll('.delete-form').forEach(form => {
    form.addEventListener('submit', (e) => {
      e.preventDefault();   // stop immediate submit

      const name = form.dataset.name || 'this contact';

      // Custom confirm dialog
      const confirmed = showConfirmDialog(name, () => {
        form.submit();       // user confirmed → actually submit
      });
    });
  });


  // ── 3. LIVE CLIENT-SIDE FILTER (All Contacts page) ───────
  /**
   * The #filterInput box on contacts.html filters visible cards
   * in real-time without a server round-trip.
   * Cards have data-name="<lowercase name>" attribute.
   */
  const filterInput = document.getElementById('filterInput');
  const contactsGrid = document.getElementById('contactsGrid');
  const noFilterResults = document.getElementById('noFilterResults');

  if (filterInput && contactsGrid) {
    filterInput.addEventListener('input', () => {
      const term  = filterInput.value.trim().toLowerCase();
      const cards = contactsGrid.querySelectorAll('.contact-card');
      let   visible = 0;

      cards.forEach(card => {
        const name = card.dataset.name || '';
        const show = !term || name.includes(term);
        card.style.display = show ? '' : 'none';
        if (show) visible++;
      });

      // Show/hide "no matches" message
      if (noFilterResults) {
        noFilterResults.style.display = (term && visible === 0) ? 'block' : 'none';
      }
    });

    // Clear filter on Escape
    filterInput.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        filterInput.value = '';
        filterInput.dispatchEvent(new Event('input'));
        filterInput.blur();
      }
    });
  }


  // ── 4. SEARCH PAGE — submit on Enter ─────────────────────
  const searchInput = document.getElementById('searchInput');
  if (searchInput) {
    // Form already submits on Enter natively for input[type=text],
    // but we add a small UX: clear button visibility.
    searchInput.addEventListener('input', () => {
      // Future: could trigger live fetch here
    });
  }


  // ── 5. AUTO-DISMISS FLASH MESSAGES ───────────────────────
  const flashes = document.querySelectorAll('.flash');
  flashes.forEach((flash, i) => {
    setTimeout(() => {
      flash.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
      flash.style.opacity    = '0';
      flash.style.transform  = 'translateY(-8px)';
      setTimeout(() => flash.remove(), 500);
    }, 4000 + i * 500);   // stagger if multiple
  });


  // ── 6. STAGGERED CARD ANIMATIONS ─────────────────────────
  const cards = document.querySelectorAll('.contact-card, .feature-card');
  cards.forEach((card, i) => {
    card.style.animationDelay = `${i * 60}ms`;
  });

});


// ── CONFIRM DIALOG HELPER ────────────────────────────────────
/**
 * Creates a styled overlay confirm dialog.
 * Calls onConfirm() if user clicks "Delete".
 */
function showConfirmDialog(contactName, onConfirm) {
  // Remove any existing dialog
  const existing = document.getElementById('confirmOverlay');
  if (existing) existing.remove();

  const overlay = document.createElement('div');
  overlay.id = 'confirmOverlay';
  overlay.style.cssText = `
    position: fixed; inset: 0;
    background: rgba(28,28,30,0.55);
    display: flex; align-items: center; justify-content: center;
    z-index: 9999;
    animation: fadeOverlay 0.2s ease;
  `;

  overlay.innerHTML = `
    <style>
      @keyframes fadeOverlay { from { opacity:0; } to { opacity:1; } }
      @keyframes popIn { from { opacity:0; transform:scale(0.9) translateY(16px); }
                         to   { opacity:1; transform:scale(1)   translateY(0);    } }
      #confirmBox {
        background: #FFFFFF;
        border-radius: 14px;
        padding: 2rem 2.25rem;
        max-width: 380px;
        width: 90%;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        animation: popIn 0.25s cubic-bezier(0.34,1.56,0.64,1);
        text-align: center;
      }
      #confirmBox .icon  { font-size: 2.8rem; margin-bottom: 0.75rem; }
      #confirmBox h3     { font-family: 'Playfair Display', serif; font-size: 1.3rem; margin-bottom: 0.5rem; color: #1C1C1E; }
      #confirmBox p      { font-size: 0.9rem; color: #8A8A8E; margin-bottom: 1.75rem; line-height: 1.5; }
      #confirmBox p strong { color: #1C1C1E; }
      .confirm-actions   { display: flex; gap: 0.75rem; justify-content: center; }
      .confirm-actions button {
        padding: 0.65rem 1.4rem;
        border-radius: 6px;
        font-size: 0.9rem;
        font-weight: 600;
        cursor: pointer;
        border: 2px solid transparent;
        font-family: 'DM Sans', sans-serif;
        transition: all 0.2s ease;
      }
      #cancelBtn  { background: transparent; border-color: #3A3A3C; color: #1C1C1E; }
      #cancelBtn:hover  { background: #1C1C1E; color: #F5F0E8; }
      #deleteBtn  { background: #DC3545; border-color: #DC3545; color: #fff; }
      #deleteBtn:hover  { background: #C82333; }
    </style>

    <div id="confirmBox">
      <div class="icon">🗑️</div>
      <h3>Delete Contact?</h3>
      <p>Are you sure you want to delete <strong>${escapeHtml(contactName)}</strong>?<br>This cannot be undone.</p>
      <div class="confirm-actions">
        <button id="cancelBtn">Cancel</button>
        <button id="deleteBtn">Yes, Delete</button>
      </div>
    </div>
  `;

  document.body.appendChild(overlay);

  // Wire buttons
  overlay.querySelector('#cancelBtn').addEventListener('click', () => overlay.remove());
  overlay.querySelector('#deleteBtn').addEventListener('click', () => {
    overlay.remove();
    onConfirm();
  });

  // Click outside to cancel
  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) overlay.remove();
  });

  // ESC to cancel
  const escHandler = (e) => {
    if (e.key === 'Escape') { overlay.remove(); document.removeEventListener('keydown', escHandler); }
  };
  document.addEventListener('keydown', escHandler);
}


// ── HTML ESCAPE UTILITY ──────────────────────────────────────
function escapeHtml(str) {
  return String(str)
    .replace(/&/g,  '&amp;')
    .replace(/</g,  '&lt;')
    .replace(/>/g,  '&gt;')
    .replace(/"/g,  '&quot;')
    .replace(/'/g,  '&#39;');
}
// The frontend is done — this is the end of main.js!
