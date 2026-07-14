# Developer notes

Internal documentation for working on the Quicky Web Tools. Users
don't need anything from this file - see the root README instead.

## How the tools are built

Everything user-visible lives **inlined** inside each tool's HTML -
you can hand-edit any tool directly. The shared look + floating nav +
Three.js are maintained as sources in `_shared/` and baked into every
tool by a Python script, so each HTML stays a standalone single file
(works from disk, no server, no internet).

The Aurora Glass theme uses the operating system's native font stack
(Segoe UI / SF / system-ui), so no UI webfonts are embedded. The files
under `_shared/fonts/ui/` and `_build_ui_fonts.py` are retired
leftovers from the earlier synthwave theme and are no longer part of
the build.

## Folder layout

```
Tools for SL/
├── SL <Tool Name>/             one folder per tool
│   ├── sl_<tool_name>.html     the tool (single standalone file)
│   └── _meta.js                existence marker for the floating nav
├── _shared/
│   ├── sl-nav.css              Aurora Glass theme + floating nav styles
│   ├── sl-nav.js               nav bootstrap + tool registry + glow layer
│   ├── sync_inline.py          bakes the above (+ Three.js) into each tool
│   ├── fonts/
│   │   ├── *.ttf               picker fonts for the 3D Text Creator
│   │   ├── _build_fonts_inline.py  → write fonts_inline.js
│   │   ├── fonts_inline.js     built artefact, inlined by the 3D Text Creator
│   │   └── ui/                 (retired - UI now uses system fonts)
│   └── three/
│       ├── three.core.min.js   Three.js r184 ESM sources
│       ├── three.module.min.js
│       ├── OrbitControls.js
│       ├── RoomEnvironment.js
│       ├── _build_inline_bundle.py  → bake all four as one importmap loader
│       └── three_inline.js     built artefact, inlined by AP + 3D Text
└── index.html                  landing page (GitHub Pages entry point)
```

## Update workflow

After editing anything in `_shared/`:

```bash
# 1. If you touched any .ttf in _shared/fonts/ (picker fonts):
python "_shared/fonts/_build_fonts_inline.py"

# 2. If you touched any .js in _shared/three/:
python "_shared/three/_build_inline_bundle.py"

# 3. Always last - push the latest source into every tool:
python "_shared/sync_inline.py"
```

All scripts are idempotent - re-run as often as you like. The inlined
snapshots inside each tool are wrapped in marker comments
(`SHARED-CSS:BEGIN/END` etc.); never hand-edit between the markers.

## Adding a new tool

1. Create a folder next to the others, e.g. `SL Foo Maker/`.
2. Drop a `_meta.js` in it:
   ```js
   window.__SLT_AVAILABLE = window.__SLT_AVAILABLE || {};
   window.__SLT_AVAILABLE['foo-maker'] = { present: true };
   ```
3. In `_shared/sl-nav.js`, add a `REGISTRY` entry:
   ```js
   {
     id: 'foo-maker',
     name: 'Foo Maker',
     subtitle: 'one-line description',
     folder: 'SL Foo Maker',
     file: 'sl_foo_maker.html',
     badge: 'FM',
   },
   ```
4. In `_shared/sync_inline.py`, add the new HTML to `TOOLS`
   (`three: True` if it uses Three.js, `False` otherwise).
5. In the tool's HTML head, add
   ```html
   <link rel="stylesheet" href="../_shared/sl-nav.css">
   <script>window.SLT_CURRENT = "foo-maker";</script>
   ```
   and directly after `<body>`:
   ```html
   <script src="../_shared/sl-nav.js"></script>
   ```
   Use `<body class="slt-themed">` so the Aurora Glass theme picks it
   up. (A tool may also skip `slt-themed` and keep fully custom
   styling - the Music Slicer does this - and still gets the nav.)
6. Add a card for it on `index.html` (landing page).
7. Run `python "_shared/sync_inline.py"`.

## The floating nav is modular

Each tool probes its sibling folders for `_meta.js` at runtime - a
deleted tool folder disappears from every other tool's nav menu
automatically, no configuration needed. This works on `file://` too.
