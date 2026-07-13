#!/usr/bin/env python3
"""
sync_inline.py — keep every SL tool standalone

Each tool's HTML used to load its theme via:
    <link rel="stylesheet" href="../_shared/sl-nav.css">
    <script src="../_shared/sl-nav.js"></script>
…which broke the look the moment the tool was moved away from the
parent folder.

This script bakes the current contents of _shared/sl-nav.css and
_shared/sl-nav.js directly into every tool's <head>. After running,
each tool HTML is a self-contained file: copy it anywhere on disk, open
in a browser, and it still looks and behaves identically.

The inlined block is wrapped in BEGIN/END markers, so this script is
idempotent — re-run after editing the shared files and the snapshot
inside each tool gets refreshed.

USAGE
-----
    python "_shared/sync_inline.py"

…from the parent directory, or just:

    python sync_inline.py

…from inside _shared/.
"""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
SHARED = ROOT / "_shared"

CSS_PATH       = SHARED / "sl-nav.css"
JS_PATH        = SHARED / "sl-nav.js"
THREE_INLINE   = SHARED / "three" / "three_inline.js"     # ES-module loader
PICKER_FONTS   = SHARED / "fonts" / "fonts_inline.js"     # 3D Text picker fonts


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


# Inlined script bodies live inside <script>…</script>. Any literal
# </script> in the source code (typically in JSDoc strings) ends the
# outer tag from the HTML parser's perspective, so we escape it.
def _escape_script(s: str) -> str:
    return s.replace("</script>", "<\\/script>")


CSS_TEXT             = _read(CSS_PATH).replace("</style>", "<\\/style>")
JS_TEXT              = _escape_script(_read(JS_PATH))
THREE_INLINE_TEXT    = _escape_script(_read(THREE_INLINE))  if THREE_INLINE.exists()  else None
PICKER_FONTS_TEXT    = _escape_script(_read(PICKER_FONTS))  if PICKER_FONTS.exists()  else None

# Per-tool config:
#   three          False/True → bake _shared/three/three_inline.js + bridge
#   picker_fonts   False/True → bake _shared/fonts/fonts_inline.js
#                               (only the 3D Text Creator's font picker
#                                needs this — Anton, BebasNeue, etc.)
TOOLS = [
    {"path": "SL Animation Combiner/sl_animation_combiner.html",                  "three": False, "picker_fonts": False},
    {"path": "SL Animation Priority Changer/sl_animation_priority_changer.html",  "three": True,  "picker_fonts": False},
    {"path": "SL Sprite Sheet Maker/sl_sprite_sheet_maker.html",                  "three": False, "picker_fonts": False},
    {"path": "SL 3D Text Creator/sl_3d_text_creator.html",                        "three": True,  "picker_fonts": True},
    {"path": "SL HUD Buttons Creator/sl_hud_buttons_creator.html",                "three": False, "picker_fonts": False},
    {"path": "SL Alpha Maker/sl_alpha_maker.html",                                "three": False, "picker_fonts": False},
    {"path": "SL Music Slicer/sl_music_slicer.html",                              "three": False, "picker_fonts": False},
]

# ----- Markers wrap each inlined block so the script can find &
# replace it next time without producing duplicates. -----------
CSS_BEGIN   = ("<!-- SHARED-CSS:BEGIN — auto-inlined from _shared/sl-nav.css "
               "by _shared/sync_inline.py. Do not hand-edit; edit the source "
               "and re-run the script. -->")
CSS_END     = "<!-- SHARED-CSS:END -->"
JS_BEGIN    = ("<!-- SHARED-JS:BEGIN — auto-inlined from _shared/sl-nav.js "
               "by _shared/sync_inline.py. Do not hand-edit; edit the source "
               "and re-run the script. -->")
JS_END      = "<!-- SHARED-JS:END -->"
THREE_BEGIN = ("<!-- SHARED-THREE:BEGIN — auto-inlined from _shared/three/ "
               "by _shared/sync_inline.py. Do not hand-edit; edit the source "
               "and re-run the script. -->")
THREE_END   = "<!-- SHARED-THREE:END -->"
PICKER_BEGIN = ("<!-- SHARED-PICKER-FONTS:BEGIN — auto-inlined from "
                "_shared/fonts/fonts_inline.js by _shared/sync_inline.py. "
                "Do not hand-edit; edit the source and re-run the script. -->")
PICKER_END   = "<!-- SHARED-PICKER-FONTS:END -->"

# Inlined snapshots:
CSS_BLOCK = f"{CSS_BEGIN}\n<style>\n{CSS_TEXT}\n</style>\n{CSS_END}"
JS_BLOCK  = f"{JS_BEGIN}\n<script>\n{JS_TEXT}\n</script>\n{JS_END}"

def three_block() -> str:
    if THREE_INLINE_TEXT is None:
        raise FileNotFoundError("_shared/three/three_inline.js missing — "
                                "run _shared/three/_build_inline_bundle.py first")
    return (
        f"{THREE_BEGIN}\n"
        f'<script>/* Three.js ES-module loader (base64-decoded into Blob URLs '
        f'+ importmap, no network needed). */\n'
        f"{THREE_INLINE_TEXT}\n"
        f"</script>\n"
        f'<script type="module">\n'
        f'  /* Bridge: expose Three.js as window.THREE for any pre-module\n'
        f'     code paths that read it off the global, then signal readiness\n'
        f'     so deferred init can run. */\n'
        f'  import * as THREE from "three";\n'
        f'  window.THREE = THREE;\n'
        f'  window.dispatchEvent(new Event("three-ready"));\n'
        f'</script>\n'
        f"{THREE_END}"
    )

def picker_block() -> str:
    if PICKER_FONTS_TEXT is None:
        raise FileNotFoundError("_shared/fonts/fonts_inline.js missing — "
                                "run _shared/fonts/_build_fonts_inline.py first")
    return (
        f"{PICKER_BEGIN}\n"
        f"<script>/* SL 3D Text Creator picker fonts — base64 TTFs merged "
        f"into FONT_DATA via Object.assign. All SIL OFL v1.1. */\n"
        f"{PICKER_FONTS_TEXT}\n"
        f"</script>\n"
        f"{PICKER_END}"
    )

# What the OLD non-standalone forms looked like:
CSS_LINK_TAG       = '<link rel="stylesheet" href="../_shared/sl-nav.css">'
JS_LINK_TAG        = '<script src="../_shared/sl-nav.js"></script>'
THREE_INLINE_TAG   = '<script src="../_shared/three/three_inline.js"></script>'
PICKER_FONTS_TAG   = '<script src="../_shared/fonts/fonts_inline.js"></script>'

# Regexes that match existing inlined snapshots (BEGIN…END pairs).
CSS_INLINED_RE    = re.compile(re.escape(CSS_BEGIN)    + r".*?" + re.escape(CSS_END),    re.DOTALL)
JS_INLINED_RE     = re.compile(re.escape(JS_BEGIN)     + r".*?" + re.escape(JS_END),     re.DOTALL)
THREE_INLINED_RE  = re.compile(re.escape(THREE_BEGIN)  + r".*?" + re.escape(THREE_END),  re.DOTALL)
PICKER_INLINED_RE = re.compile(re.escape(PICKER_BEGIN) + r".*?" + re.escape(PICKER_END), re.DOTALL)


def inline_one(text: str, tool: dict) -> tuple[str, list[str]]:
    """Return (new_text, list of bundles refreshed)."""
    refreshed: list[str] = []
    name = tool["path"]

    # ----- shared CSS -----
    if CSS_INLINED_RE.search(text):
        text = CSS_INLINED_RE.sub(lambda _m: CSS_BLOCK, text); refreshed.append("CSS")
    elif CSS_LINK_TAG in text:
        text = text.replace(CSS_LINK_TAG, CSS_BLOCK);          refreshed.append("CSS")
    else:
        print(f"  WARN: {name}: no SHARED-CSS marker or <link> tag — "
              f"skipped CSS", file=sys.stderr)

    # ----- shared JS (the floating-nav bootstrap) -----
    if JS_INLINED_RE.search(text):
        text = JS_INLINED_RE.sub(lambda _m: JS_BLOCK, text);   refreshed.append("JS")
    elif JS_LINK_TAG in text:
        text = text.replace(JS_LINK_TAG, JS_BLOCK);            refreshed.append("JS")
    else:
        print(f"  WARN: {name}: no SHARED-JS marker or <script src> tag — "
              f"skipped JS", file=sys.stderr)

    # ----- Three.js (only for tools that use it) -----
    if tool["three"]:
        block = three_block()
        if THREE_INLINED_RE.search(text):
            text = THREE_INLINED_RE.sub(lambda _m: block, text)
            refreshed.append("THREE")
        elif THREE_INLINE_TAG in text:
            text = text.replace(THREE_INLINE_TAG, block)
            refreshed.append("THREE")
        else:
            print(f"  WARN: {name}: tool needs Three.js but no SHARED-THREE "
                  f"marker or ../_shared/three/three_inline.js <script> "
                  f"found", file=sys.stderr)

    # ----- Picker fonts (only the 3D Text Creator needs them) -----
    if tool.get("picker_fonts"):
        block = picker_block()
        if PICKER_INLINED_RE.search(text):
            text = PICKER_INLINED_RE.sub(lambda _m: block, text)
            refreshed.append("PICKER")
        elif PICKER_FONTS_TAG in text:
            text = text.replace(PICKER_FONTS_TAG, block)
            refreshed.append("PICKER")
        else:
            print(f"  WARN: {name}: tool needs picker fonts but no "
                  f"SHARED-PICKER-FONTS marker or fonts_inline.js <script> "
                  f"found", file=sys.stderr)

    return text, refreshed


def main() -> int:
    print(f"Source CSS:    {CSS_PATH} ({len(CSS_TEXT):,} bytes)")
    print(f"Source JS:     {JS_PATH} ({len(JS_TEXT):,} bytes)")
    if THREE_INLINE_TEXT is not None:
        print(f"Three.js:      {THREE_INLINE} ({len(THREE_INLINE_TEXT):,} bytes)")
    if PICKER_FONTS_TEXT is not None:
        print(f"Picker fonts:  {PICKER_FONTS} ({len(PICKER_FONTS_TEXT):,} bytes)")
    print()

    for tool in TOOLS:
        rel = tool["path"]
        path = ROOT / rel
        if not path.exists():
            print(f"  SKIP: {rel} (file not found)")
            continue
        before = path.read_text(encoding="utf-8")
        after, refreshed = inline_one(before, tool)
        if before == after:
            print(f"  unchanged: {rel}")
        else:
            path.write_text(after, encoding="utf-8")
            tag = "+".join(refreshed) if refreshed else "noop"
            print(f"  synced [{tag}]: {rel}")

    print()
    print("Done. Each tool HTML now carries its own inlined copies of the "
          "shared CSS + JS (and Three.js where needed). Standalone — no "
          "_shared/ folder or internet required.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
