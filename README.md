# SL Tools — Aurora Edition

A small constellation of single-file, browser-based utilities for
Second Life creators. Each tool is a self-contained `.html` you can
double-click to open — no install, no server, no internet required.
The "Aurora Glass" UI (deep indigo, drifting aurora blobs, frosted
glass panels, animated gradient headlines, clean system fonts) is
shared between every tool, and a floating nav pill in the top-right
corner lets you flip between them.

```
Tools for SL/
├── SL Animation Combiner/         body + hand .anim → combo .anim
├── SL Animation Priority Changer/ set priority on one or many .anims
├── SL Sprite Sheet Maker/         GIFs → optimised PNG sprite sheets
├── SL 3D Text Creator/            text → Collada .dae mesh (3D depth)
├── SL HUD Buttons Creator/        button grid → low-poly mesh for HUDs
├── SL Alpha Maker/                paint the body alpha mask on a template
├── SL Music Slicer/               songs → ≤30s WAV clips + in-world player
└── _shared/                       build sources + sync pipeline (dev only)
```


## Use it

Double-click any of the tool `.html` files. That's it.

Every tool has the **same** floating nav pill — click the `[badge ▾]`
in the top-right corner to see the other tools and switch between
them. The list is built modularly: if you delete a tool's folder it
disappears from every other tool's menu automatically.

Tools work just as well copied somewhere else on disk (e.g. emailed
as a single file). The shared theme, fonts, Three.js, OpenCV, etc.
are all baked into each HTML — no `_shared/` or network needed at
runtime.


## The tools

### SL Animation Combiner
Two `.anim` files → one. Ideal for sticking a hand pose onto a body
dance: the hand keyframes are aligned to the loop window of the body
animation so the cycle stays clean. Parses + writes the LindenLab
.anim binary format in JavaScript.

### SL Animation Priority Changer
Load any number of `.anim` files, change their `base_priority` (and
all per-joint priorities), preview the rig in a 3D viewer, export
again. Higher priority wins when multiple animations fight over the
same joints. Bit-perfect — only the priority fields are touched.

### SL Sprite Sheet Maker
Drop one or more GIFs in, get a single PNG sprite sheet out.
- Auto-crops or aspect-locks each frame
- Quantises to ≤ 256 colours per cell to keep the PNG small enough for
  SL's 1024×1024 texture budget
- Customisable background (transparent, solid, or per-pixel pick)

### SL 3D Text Creator
Type a word, pick a font, get a Collada `.dae` mesh with real 3D
depth ready for SL upload. Built-in fonts (Pacifico, Audiowide,
BebasNeue, Anton, BlackOpsOne, PressStart2P, Righteous, RussoOne)
plus custom TTF/OTF upload. Live three.js preview, triangle-count
read-out, optional decoration shapes (hearts, stars, dots…).

### SL HUD Buttons Creator
Lay out HUD buttons in a row, column, or arbitrary M×N grid; pick a
shape (rect / rounded rect / pill / circle / polygon / arrow / star /
heart / plus), set per-button colours and labels, choose how SL's
face slots are spent, export an optimised `.dae` mesh.

### SL Alpha Maker
Paint over the parts you want to hide on a body template (Upper or
Lower), download the resulting alpha mask `.png` to wear on your
avatar. Uses the Robin Wood UV templates baked in as data URLs.

### SL Music Slicer
Song-length music playback in SL despite the 30-second sound-clip
limit: drop songs in (mp3 / wav / flac / ogg / m4a), trim on the
waveform, and export loudness-normalised ≤30s mono WAV clips with a
predictable naming scheme that an in-world player script can schedule
gaplessly (the player itself is not part of this repository). Titles
auto-fill from embedded metadata tags. See the folder's own README
for the workflow and the clip naming spec.


## Develop

Everything user-visible lives **inlined** inside the tool HTMLs — you
can hand-edit any tool directly. But the look + nav + Three.js are
pulled from sources in `_shared/`, then baked into each tool by a
Python script.

The Aurora Glass theme uses the operating system's native font stack
(Segoe UI / SF / system-ui), so **no UI webfonts are embedded** —
that keeps every tool ~380 KB lighter than the old synthwave builds.
The files under `_shared/fonts/ui/` and `_build_ui_fonts.py` are
retired leftovers from that era and are no longer part of the build.

### Folder layout under `_shared/`

```
_shared/
├── sl-nav.css                  Aurora Glass theme + floating nav styles
├── sl-nav.js                   nav bootstrap + tool registry + glow layer
├── sync_inline.py              bakes the above (+ Three.js) into each tool
├── fonts/
│   ├── *.ttf                   picker fonts for the 3D Text Creator
│   ├── _build_fonts_inline.py  → write fonts_inline.js (base64 picker fonts)
│   ├── fonts_inline.js         built artefact, inlined by the 3D Text Creator
│   └── ui/                     (retired — UI now uses system fonts)
└── three/
    ├── three.core.min.js       Three.js r184 ESM sources
    ├── three.module.min.js
    ├── OrbitControls.js
    ├── RoomEnvironment.js
    ├── _build_inline_bundle.py → bake all four as one importmap loader
    └── three_inline.js         built artefact, inlined by AP + 3D Text
```

### Update workflow

After editing anything in `_shared/`:

```bash
# 1. If you touched any .ttf in _shared/fonts/ (picker fonts):
python "_shared/fonts/_build_fonts_inline.py"

# 2. If you touched any .js in _shared/three/:
python "_shared/three/_build_inline_bundle.py"

# 3. Always last — push the latest source into every tool:
python "_shared/sync_inline.py"
```

All scripts are idempotent — re-run as often as you like.

### Adding a new tool

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
5. In the tool's HTML head, BEFORE the SHARED-CSS marker block, set
   ```html
   <script>window.SLT_CURRENT = "foo-maker";</script>
   ```
   and use `<body class="slt-themed">` so the Aurora Glass theme
   picks it up. (A tool may also skip `slt-themed` and keep fully
   custom styling — the Music Slicer does this — and still gets the
   floating nav.)
6. Run `python "_shared/sync_inline.py"`.


## Credits

The tools bundle several MIT-, ISC- or OFL-licensed libraries and
fonts, plus the Robin Wood SL avatar UV templates. The bundled,
base64-decoded source code is unmodified. Full attribution and
licence texts are in [`THIRD-PARTY-NOTICES.md`](THIRD-PARTY-NOTICES.md).

- **Three.js** r184 (MIT) — mrdoob & contributors
- **opentype.js** (MIT) — font parsing in the 3D Text Creator
- **earcut** (ISC) — polygon triangulation in the 3D Text Creator
- **gifuct-js** (MIT) — GIF decoding in the Sprite Sheet Maker
- **Picker fonts** in the 3D Text Creator (SIL Open Font License):
  Pacifico, Audiowide, BebasNeue, Anton, BlackOpsOne, PressStart2P,
  Righteous, RussoOne
- **Body UV templates** in SL Alpha Maker: Robin Wood (2005), used
  under her free-redistribution terms; credited inline in the tool's
  footer

The UI itself uses the operating system's native fonts — no UI
webfonts are embedded anymore. The Music Slicer bundles no
third-party code at all (own WAV/ZIP encoders and tag readers).


## Licence

Application code in this repository — UI, parsers, builders, build
scripts and styles written by Ya — is licensed under the **PolyForm
Noncommercial License 1.0.0**. See [`LICENSE`](LICENSE) for the full
text.

Plain-language summary (not part of the licence):

- You **may** use, copy, modify and redistribute the tools for any
  **noncommercial** purpose (personal hobby use, learning, charitable
  / educational use, etc.).
- You **may not** use them commercially — no selling the tools,
  bundling them in a commercial product, offering them as a paid
  service, or using them in a business.
- If you distribute copies (or modified versions), include the
  `LICENSE` file and the `Required Notice: Copyright © 2026 Ya` line.
- All rights not explicitly granted are reserved.

Bundled third-party libraries and fonts keep their own permissive
licences and are unaffected by this. See `THIRD-PARTY-NOTICES.md`.
