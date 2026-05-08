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

CSS_PATH = SHARED / "sl-nav.css"
JS_PATH  = SHARED / "sl-nav.js"

CSS_TEXT = CSS_PATH.read_text(encoding="utf-8")
JS_TEXT  = JS_PATH.read_text(encoding="utf-8")

# When inlining a <script>, any literal </script> in the JS source
# (typically in doc comments) terminates the outer <script> tag from
# the HTML parser's perspective. Escape it so the parser sees one
# continuous script. Same trick for </style> inside CSS strings,
# though we don't currently have any.
JS_TEXT  = JS_TEXT.replace("</script>", "<\\/script>")
CSS_TEXT = CSS_TEXT.replace("</style>", "<\\/style>")

TOOLS = [
    "SL Animation Combiner/sl_animation_combiner.html",
    "SL Animation Priority Changer/sl_animation_priority_changer.html",
    "SL Sprite Sheet Maker/sl_sprite_sheet_maker.html",
    "SL 3D Text Creator/sl_3d_text_creator.html",
    "SL HUD Buttons Creator/sl_hud_buttons_creator.html",
]

# Markers wrap the inlined block so the script can find and replace it
# next time without re-introducing duplicates.
CSS_BEGIN = ("<!-- SHARED-CSS:BEGIN — auto-inlined from _shared/sl-nav.css "
             "by _shared/sync_inline.py. Do not hand-edit; edit the source "
             "and re-run the script. -->")
CSS_END   = "<!-- SHARED-CSS:END -->"
JS_BEGIN  = ("<!-- SHARED-JS:BEGIN — auto-inlined from _shared/sl-nav.js "
             "by _shared/sync_inline.py. Do not hand-edit; edit the source "
             "and re-run the script. -->")
JS_END    = "<!-- SHARED-JS:END -->"

# What the inlined snapshot looks like in each HTML head:
CSS_BLOCK = f"{CSS_BEGIN}\n<style>\n{CSS_TEXT}\n</style>\n{CSS_END}"
JS_BLOCK  = f"{JS_BEGIN}\n<script>\n{JS_TEXT}\n</script>\n{JS_END}"

# What the OLD non-standalone form looked like:
CSS_LINK_TAG = '<link rel="stylesheet" href="../_shared/sl-nav.css">'
JS_LINK_TAG  = '<script src="../_shared/sl-nav.js"></script>'

# Regex that matches an existing inlined snapshot (BEGIN…END pair).
CSS_INLINED_RE = re.compile(
    re.escape(CSS_BEGIN) + r".*?" + re.escape(CSS_END), re.DOTALL
)
JS_INLINED_RE = re.compile(
    re.escape(JS_BEGIN) + r".*?" + re.escape(JS_END), re.DOTALL
)


def inline(text: str, tool_name: str) -> tuple[str, bool, bool]:
    """Return (new_text, css_replaced, js_replaced)."""
    css_done = js_done = False

    # CSS — refresh existing snapshot, or replace the <link> tag the
    # first time we run on a tool.
    if CSS_INLINED_RE.search(text):
        text = CSS_INLINED_RE.sub(lambda _m: CSS_BLOCK, text)
        css_done = True
    elif CSS_LINK_TAG in text:
        text = text.replace(CSS_LINK_TAG, CSS_BLOCK)
        css_done = True
    else:
        print(f"  WARN: {tool_name}: no SHARED-CSS marker or <link> tag — "
              f"skipped CSS inlining", file=sys.stderr)

    # JS — same logic.
    if JS_INLINED_RE.search(text):
        text = JS_INLINED_RE.sub(lambda _m: JS_BLOCK, text)
        js_done = True
    elif JS_LINK_TAG in text:
        text = text.replace(JS_LINK_TAG, JS_BLOCK)
        js_done = True
    else:
        print(f"  WARN: {tool_name}: no SHARED-JS marker or <script src> "
              f"tag — skipped JS inlining", file=sys.stderr)

    return text, css_done, js_done


def main() -> int:
    print(f"Source CSS: {CSS_PATH} ({len(CSS_TEXT):,} bytes)")
    print(f"Source JS:  {JS_PATH} ({len(JS_TEXT):,} bytes)")
    print()

    for rel in TOOLS:
        path = ROOT / rel
        if not path.exists():
            print(f"  SKIP: {rel} (file not found)")
            continue
        before = path.read_text(encoding="utf-8")
        after, css_done, js_done = inline(before, rel)
        if before == after:
            print(f"  unchanged: {rel}")
        else:
            path.write_text(after, encoding="utf-8")
            tags = []
            if css_done: tags.append("CSS")
            if js_done:  tags.append("JS")
            print(f"  synced [{'+'.join(tags)}]: {rel}")

    print()
    print("Done. Each tool HTML now carries its own inlined copy of the "
          "shared CSS + JS, so it works standalone even if moved away "
          "from this folder.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
