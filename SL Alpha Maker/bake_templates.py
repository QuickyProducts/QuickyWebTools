#!/usr/bin/env python3
"""
bake_templates.py — inline the body templates as base64 data URLs.

Why we need this
----------------
SL Alpha Maker is opened over file:// from disk. Chrome (and most
Chromium browsers) treat every local file as its own origin, so when
an <img> loads ./Robin Wood/foo.jpg and we drawImage it onto a canvas,
the canvas becomes "tainted" — toBlob() then throws a SecurityError
and the user can't download the alpha mask.

Inlining the templates as data: URLs sidesteps the origin check
(data URLs are same-origin with the document for canvas purposes).
The HTML grows by the templates' base64 size but stays a single
standalone file.

Usage
-----
    py bake_templates.py

…from inside the SL Alpha Maker folder. Re-run after replacing or
resizing a template. Idempotent: re-baking just refreshes the marker
block.
"""

from __future__ import annotations
import base64
import mimetypes
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent
HTML = ROOT / "sl_alpha_maker.html"

# Robin Wood's classic SL avatar templates (2005) — one Upper, one
# Lower. Most mesh bodies (Legacy, Reborn, Maitreya, …) use this same
# UV layout, so one alpha mask is enough for all of them.
SOURCES = {
    "upper": ROOT / "Robin Wood" / "SL-Avatar-Top-1024.jpg",
    "lower": ROOT / "Robin Wood" / "SL-Avatar-Bottom-1024.jpg",
}

BEGIN = "/* TEMPLATES:BEGIN */"
END   = "/* TEMPLATES:END */"


def data_url(path: Path) -> str:
    raw = path.read_bytes()
    mime, _ = mimetypes.guess_type(path.name)
    if mime is None:
        mime = "application/octet-stream"
    return f"data:{mime};base64," + base64.b64encode(raw).decode("ascii")


def build_block() -> str:
    lines = [
        BEGIN,
        "// Auto-baked by bake_templates.py - do not hand-edit. Re-run",
        "// the script to refresh after the source images change.",
        "const TEMPLATES = {",
    ]
    for side, path in SOURCES.items():
        if not path.exists():
            print(f"  MISSING: {path}", file=sys.stderr)
            sys.exit(1)
        url = data_url(path)
        lines.append(f"  {side}: '{url}',")
    lines.append("};")
    lines.append(END)
    return "\n".join(lines)


def main() -> int:
    text = HTML.read_text(encoding="utf-8")
    pat = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END), re.DOTALL)
    if not pat.search(text):
        print(f"ERROR: marker block ({BEGIN} … {END}) not found in {HTML.name}",
              file=sys.stderr)
        return 1

    block = build_block()
    new_text = pat.sub(lambda _m: block, text)
    HTML.write_text(new_text, encoding="utf-8")

    total_src = sum(p.stat().st_size for p in SOURCES.values())
    total_html = HTML.stat().st_size
    # Windows console defaults to cp1252 and chokes on fancy arrows.
    print(f"Baked {len(SOURCES)} templates ({total_src:,} source bytes -> {len(block):,} JS bytes)")
    print(f"  {HTML.name} is now {total_html:,} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
