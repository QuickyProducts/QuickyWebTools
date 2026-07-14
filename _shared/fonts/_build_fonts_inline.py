#!/usr/bin/env python3
"""
Build fonts_inline.js - base64-encodes every .ttf in this folder
(NOT the ui/ subfolder) and writes them as Object.assign(FONT_DATA, …)
so the SL 3D Text Creator can offer them in its picker.

The companion file _build_ui_fonts.py handles the synthwave UI fonts
in fonts/ui/ - those go straight into sl-nav.css as @font-face rules.

USAGE
-----
    python "_shared/fonts/_build_fonts_inline.py"

Re-run after adding/removing .ttf files in this folder.
"""
from __future__ import annotations
import base64
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

HEADER = """\
/* Extra fonts for SL 3D Text Creator. Each entry is a base64-encoded TTF
   file. Decoded and parsed by opentype.js the same way as the inline
   Pacifico font. Built from the .ttf files in this folder by
   _build_fonts_inline.py.
   All fonts here are SIL Open Font License (free + redistributable).

   Note: the Pacifico FONT_DATA is declared as `const` in the inline script
   just before this one. We use Object.assign on the object directly -
   const binds the reference, not the contents, so mutating works. */
Object.assign(FONT_DATA, {
"""

FOOTER = "});\n"


def main() -> int:
    ttfs = sorted(HERE.glob("*.ttf"))
    if not ttfs:
        print("  ERROR: no .ttf files found in this folder", file=sys.stderr)
        return 1

    entries = []
    for ttf in ttfs:
        b64 = base64.b64encode(ttf.read_bytes()).decode("ascii")
        entries.append(f'  "{ttf.stem}": "{b64}"')

    out_path = HERE / "fonts_inline.js"
    body = ",\n".join(entries) + "\n"
    out_path.write_text(HEADER + body + FOOTER, encoding="utf-8")
    size = out_path.stat().st_size
    print(f"  Wrote fonts_inline.js ({size:,} bytes, {len(ttfs)} fonts)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
