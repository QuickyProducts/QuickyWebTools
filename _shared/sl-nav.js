/* =====================================================================
   SL Tools :: Navigation bootstrapper
   - Detects which sibling tools exist (modular: missing folder = hidden)
   - Renders a synthwave nav bar at the top
   - Adds the sun + grid + scanlines background layers

   How it works
   ------------
   Each tool folder contains a tiny `_meta.js` that registers its own
   metadata into window.__SLT_AVAILABLE. We try to load that file via
   <script> tags. file:// allows local <script> loads, and onerror fires
   reliably when the file is missing — so removing a tool folder makes
   it disappear from the nav automatically.

   Adding a new tool:
   - Add an entry below in REGISTRY
   - Drop the folder with its main HTML and a `_meta.js`

   Each tool's HTML opts in by including:
     <link rel="stylesheet" href="../_shared/sl-nav.css">
     <script>window.SLT_CURRENT = "anim-combiner";</script>
     <script src="../_shared/sl-nav.js"></script>
   ===================================================================== */
(function () {
  'use strict';

  // Ordered registry of all tools known to this navigation system.
  // Each `folder` is the directory name that sits next to this tool.
  // `file` is the main HTML in that folder.
  const REGISTRY = [
    {
      id: 'anim-combiner',
      name: 'Animation Combiner',
      subtitle: 'body + hands → combo',
      folder: 'SL Animation Combiner',
      file: 'sl_animation_combiner.html',
      badge: 'AC',
    },
    {
      id: 'anim-priority',
      name: 'Animation Priority Changer',
      subtitle: 'set priority on .anim files',
      folder: 'SL Animation Priority Changer',
      file: 'sl_animation_priority_changer.html',
      badge: 'AP',
    },
    {
      id: 'sprite-sheet',
      name: 'Sprite Sheet Maker',
      subtitle: 'gif → sprite sheet',
      folder: 'SL Sprite Sheet Maker',
      file: 'sl_sprite_sheet_maker.html',
      badge: 'SS',
    },
    {
      id: 'sl-text',
      name: '3D Text Creator',
      subtitle: 'text → 3D mesh',
      folder: 'SL 3D Text Creator',
      file: 'sl_3d_text_creator.html',
      badge: 'TX',
    },
    {
      id: 'sl-hud',
      name: 'HUD Buttons Creator',
      subtitle: 'buttons grid → mesh',
      folder: 'SL HUD Buttons Creator',
      file: 'sl_hud_buttons_creator.html',
      badge: 'HD',
    },
  ];

  window.__SLT_AVAILABLE = window.__SLT_AVAILABLE || {};

  // ---------------------------------------------------------------------
  // The body theme + sun + grid + scanlines are now applied entirely
  // via CSS. Each themed tool sets <body class="slt-themed"> in its
  // HTML and pre-renders <div class="slt-scanlines"></div> so there's
  // no flash of unstyled content. This script's only job is to render
  // the navigation bar after probing for sibling tools.
  // ---------------------------------------------------------------------

  // ---------------------------------------------------------------------
  // Step 2: detect which sibling tools exist
  //   For each tool that isn't the current one, try to load its
  //   `_meta.js` via a dynamic <script> tag. onerror fires when the
  //   file (or folder) is missing.
  // ---------------------------------------------------------------------
  function detectTool(tool) {
    return new Promise((resolve) => {
      // current tool always "available"
      if (tool.id === window.SLT_CURRENT) {
        window.__SLT_AVAILABLE[tool.id] = { ...tool, current: true };
        return resolve(true);
      }
      const s = document.createElement('script');
      s.async = true;
      s.src = '../' + encodeURI(tool.folder) + '/_meta.js';
      let settled = false;
      const finish = (ok) => {
        if (settled) return;
        settled = true;
        s.parentNode && s.parentNode.removeChild(s);
        resolve(ok);
      };
      s.onload = () => finish(true);
      s.onerror = () => finish(false);
      // safety timeout in case the browser silently stalls
      setTimeout(() => finish(false), 2500);
      document.head.appendChild(s);
    });
  }

  async function detectAll() {
    const results = await Promise.all(
      REGISTRY.map((t) => detectTool(t).then((ok) => ({ tool: t, ok })))
    );
    return results.filter((r) => r.ok).map((r) => r.tool);
  }

  // ---------------------------------------------------------------------
  // Step 3: render the floating nav (collapsible dropdown menu)
  //
  //   <nav class="slt-nav" data-open="false">
  //     <button class="slt-nav-handle">★ SL TOOLS ★ [TX] ▾</button>
  //     <div class="slt-nav-panel"><ul>…</ul></div>
  //   </nav>
  //
  //   The handle is the always-visible pill in the top-right corner.
  //   Clicking it expands the panel below; clicking outside or pressing
  //   Escape collapses it. Open/closed state is persisted in
  //   localStorage so it stays the way the user prefers across pages.
  // ---------------------------------------------------------------------
  const STATE_KEY = 'slt-nav-open';

  function renderNav(tools) {
    const current = tools.find((t) => t.id === window.SLT_CURRENT);
    const currentBadge = current ? current.badge : '★';

    const nav = document.createElement('nav');
    nav.className = 'slt-nav';
    nav.setAttribute('aria-label', 'SL Tools');
    nav.setAttribute('data-open', 'false');

    // Handle (always visible)
    const handle = document.createElement('button');
    handle.type = 'button';
    handle.className = 'slt-nav-handle';
    handle.setAttribute('aria-expanded', 'false');
    handle.setAttribute('aria-controls', 'slt-nav-panel');
    handle.innerHTML =
      '<span class="slt-nav-current">' + currentBadge + '</span>' +
      '<span class="slt-nav-chevron" aria-hidden="true">▾</span>';
    handle.title = 'SL Tools — click to switch';
    nav.appendChild(handle);

    // Collapsible panel (the actual menu)
    const panel = document.createElement('div');
    panel.className = 'slt-nav-panel';
    panel.id = 'slt-nav-panel';

    // Brand header inside the panel
    const header = document.createElement('div');
    header.className = 'slt-nav-panel-header';
    header.innerHTML =
      '<span class="slt-nav-handle-brand">★ SL TOOLS ★</span>' +
      '<small class="slt-nav-panel-tagline">NEON ROUTINE</small>';
    panel.appendChild(header);

    const list = document.createElement('ul');
    list.className = 'slt-nav-list';

    for (const tool of tools) {
      const li = document.createElement('li');
      const a = document.createElement('a');
      a.className = 'slt-nav-btn';
      if (tool.id === window.SLT_CURRENT) {
        a.classList.add('current');
        a.setAttribute('aria-current', 'page');
        a.href = '#';
        a.addEventListener('click', (e) => e.preventDefault());
      } else {
        a.href = '../' + encodeURI(tool.folder) + '/' + encodeURI(tool.file);
        // smooth fade-out before navigating
        a.addEventListener('click', smoothNavigate);
      }
      a.title = tool.name + ' — ' + tool.subtitle;
      a.innerHTML =
        '<span class="slt-nav-badge">' + tool.badge + '</span>' +
        '<span class="slt-nav-name">' + tool.name +
          '<small>' + tool.subtitle + '</small></span>';
      li.appendChild(a);
      list.appendChild(li);
    }

    panel.appendChild(list);
    nav.appendChild(panel);

    document.body.insertBefore(nav, document.body.firstChild);

    // Toggle behavior
    function setOpen(open) {
      nav.setAttribute('data-open', open ? 'true' : 'false');
      handle.setAttribute('aria-expanded', open ? 'true' : 'false');
      try { localStorage.setItem(STATE_KEY, open ? '1' : '0'); } catch (e) {}
    }
    handle.addEventListener('click', (e) => {
      e.stopPropagation();
      setOpen(nav.getAttribute('data-open') !== 'true');
    });
    document.addEventListener('click', (e) => {
      if (!nav.contains(e.target)) setOpen(false);
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') setOpen(false);
    });

    // Restore previous state
    try {
      if (localStorage.getItem(STATE_KEY) === '1') setOpen(true);
    } catch (e) {}
  }

  // ---------------------------------------------------------------------
  // Smooth page transition: fade the current page out before navigating.
  // The destination page fades back in via CSS animation on body load.
  // ---------------------------------------------------------------------
  function smoothNavigate(e) {
    // Allow ctrl/cmd/middle-click to open in a new tab without hijack
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.button === 1) return;
    e.preventDefault();
    const href = e.currentTarget.href;
    document.documentElement.classList.add('slt-leaving');
    setTimeout(() => { window.location.href = href; }, 180);
  }

  // ---------------------------------------------------------------------
  // Bootstrap once the DOM is ready
  // ---------------------------------------------------------------------
  function boot() {
    detectAll().then(renderNav).catch((err) => {
      console.warn('[SL Tools nav] detection failed:', err);
      // fallback: still show current tool only
      const current = REGISTRY.find((t) => t.id === window.SLT_CURRENT);
      if (current) renderNav([current]);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot, { once: true });
  } else {
    boot();
  }
})();
