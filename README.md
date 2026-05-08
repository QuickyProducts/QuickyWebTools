# QuickyWebTools

A collection of browser-based utilities for Second Life® content creators.
Everything runs **locally in the browser** — no upload, no install, no
account.

**Live site:** https://quickyproducts.github.io/QuickyWebTools/

## Tools

| Badge | Tool | What it does |
| :---: | --- | --- |
| **AC** | [Animation Combiner](./SL%20Animation%20Combiner/sl_animation_combiner.html) | Merge a body BVH with a separate hands BVH into a single combined animation. |
| **AP** | [Animation Priority Changer](./SL%20Animation%20Priority%20Changer/sl_animation_priority_changer.html) | Rewrite the priority byte inside an SL internal-format `.anim` file. |
| **SS** | [Sprite Sheet Maker](./SL%20Sprite%20Sheet%20Maker/sl_sprite_sheet_maker.html) | Slice an animated GIF, video, or image sequence into a single sprite-sheet texture. |
| **TX** | [3D Text Creator](./SL%203D%20Text%20Creator/sl_3d_text_creator.html) | Type text, pick a font and depth, export a Collada (`.dae`) mesh ready to upload. |
| **HD** | [HUD Buttons Creator](./SL%20HUD%20Buttons%20Creator/sl_hud_buttons_creator.html) | Lay out a grid of HUD buttons; export a mesh + matching texture in one go. |

## Running locally

Each tool is a single self-contained HTML file with all assets inlined,
so you can use them straight from disk:

1. Clone or download this repo.
2. Open any `sl_*.html` file in a modern browser.

That's it — no build step, no server.

## Project layout

```
SL Animation Combiner/         tool folder, contains the HTML + a _meta.js stub
SL Animation Priority Changer/
SL Sprite Sheet Maker/
SL 3D Text Creator/
SL HUD Buttons Creator/
_shared/                       fonts + Three.js + nav theme + sync_inline.py
index.html                     landing page (GitHub Pages entry point)
```

The shared theme (`_shared/sl-nav.css`) and Three.js bundle
(`_shared/three/three_inline.js`) are inlined into each tool's HTML by
`_shared/sync_inline.py`. After editing any shared file, re-run that
script to propagate the change into every tool.

## Sister projects

- [QuickyHUD](https://github.com/QuickyProducts/QuickyHUD) — HUD scripts
- [QuickySitter](https://github.com/QuickyProducts/QuickySitter) — sit/pose system (AVsitter™-compatible)

## Trademarks

Second Life® is a trademark of Linden Research, Inc. QuickyWebTools is
not affiliated with or sponsored by Linden Research.
