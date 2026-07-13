#!/usr/bin/env python3
"""
Build _shared/three/three_inline.js — a single self-contained loader
that decodes base64-embedded Three.js sources, creates Blob URLs, and
injects an importmap so any page can `import "three"` etc. without a
local web server. Works on file:// and http://.

Source files (all in this folder):
    three.core.min.js
    three.module.min.js
    OrbitControls.js
    RoomEnvironment.js

USAGE
-----
    python "_shared/three/_build_inline_bundle.py"

Re-run after replacing any of the source files (e.g. when bumping
Three.js to a newer release).
"""
from __future__ import annotations
import base64
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

FILES = {
    "B64_CORE":  "three.core.min.js",
    "B64_MOD":   "three.module.min.js",
    "B64_ORBIT": "OrbitControls.js",
    "B64_ROOM":  "RoomEnvironment.js",
}

TEMPLATE = """\
/* Three.js inline-loader bundle.
   Decodes base64-embedded Three.js sources, creates Blob URLs, and
   injects an importmap so the page can `import "three"` etc. without
   needing a local web server. Works on file:// and http://.

   Built from sibling files (three.core.min.js, three.module.min.js,
   OrbitControls.js, RoomEnvironment.js) by _build_inline_bundle.py.
*/
(function () {{
  var B64_CORE  = "{B64_CORE}";
  var B64_MOD   = "{B64_MOD}";
  var B64_ORBIT = "{B64_ORBIT}";
  var B64_ROOM  = "{B64_ROOM}";

  function b64ToText(b64) {{
    var bin = atob(b64);
    var bytes = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
    return new TextDecoder("utf-8").decode(bytes);
  }}
  function makeBlob(text) {{
    return URL.createObjectURL(new Blob([text], {{ type: "application/javascript" }}));
  }}

  var coreText = b64ToText(B64_CORE);
  var coreUrl  = makeBlob(coreText);

  // three.module.min.js imports the core via "./three.core.min.js" — rewrite
  // both occurrences to the blob URL of the inlined core so the module file
  // resolves correctly when loaded as a blob.
  var modText = b64ToText(B64_MOD)
    .replace(/['"]\\.\\/three\\.core\\.min\\.js['"]/g, JSON.stringify(coreUrl));
  var moduleUrl = makeBlob(modText);

  // OrbitControls + RoomEnvironment use bare `from "three"` — these resolve
  // via the importmap below.
  var orbitUrl = makeBlob(b64ToText(B64_ORBIT));
  var roomUrl  = makeBlob(b64ToText(B64_ROOM));

  var map = document.createElement("script");
  map.type = "importmap";
  map.textContent = JSON.stringify({{
    imports: {{
      "three":       moduleUrl,
      "three/orbit": orbitUrl,
      "three/room":  roomUrl
    }}
  }});
  document.head.appendChild(map);
  window.__SLT_THREE_INLINE_READY = true;
}})();
"""


def main() -> int:
    subs = {}
    for placeholder, filename in FILES.items():
        path = HERE / filename
        if not path.exists():
            print(f"  ERROR: missing {path}", file=sys.stderr)
            return 1
        subs[placeholder] = base64.b64encode(path.read_bytes()).decode("ascii")

    out = TEMPLATE.format(**subs)
    out_path = HERE / "three_inline.js"
    out_path.write_text(out, encoding="utf-8")
    size = out_path.stat().st_size
    print(f"  Wrote three_inline.js ({size:,} bytes)")
    print("  Now run _shared/sync_inline.py to push the updated bundle "
          "into every tool that uses Three.js.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
