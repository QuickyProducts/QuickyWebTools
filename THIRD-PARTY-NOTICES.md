# Third-Party Notices

The SL Tools bundle several open-source libraries, fonts, and image
assets directly inside each tool's HTML (as base64 / inlined `<script>`
blocks) so the tools can run offline as standalone files.

Every item listed below is included **unmodified** under its original
licence. None of the bundled material was authored by Ya. The licence
texts are reproduced in full so each standalone tool HTML satisfies
the attribution + permission-notice requirements of MIT, ISC, and
SIL OFL.

The tools' own application code (UI, file parsers, builders, styles
written by Ya) is licensed separately under the **PolyForm
Noncommercial License 1.0.0** — see the `LICENSE` file at the repo
root for the full text.

---

## 1. JavaScript libraries

### Three.js — MIT

**Used in:** `SL Animation Priority Changer`, `SL 3D Text Creator`
**Version bundled:** r184
**Source:** https://github.com/mrdoob/three.js
**Inlined as:** base64 Blob URLs + an importmap (`three_inline.js`)

```
The MIT License

Copyright © 2010-2026 three.js authors

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### earcut — ISC

**Used in:** `SL 3D Text Creator`
**Source:** https://github.com/mapbox/earcut
**Inlined as:** UMD script block

```
ISC License

Copyright (c) 2016, Mapbox

Permission to use, copy, modify, and/or distribute this software for
any purpose with or without fee is hereby granted, provided that the
above copyright notice and this permission notice appear in all
copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL
WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE
AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL
DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR
PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.
```

### opentype.js — MIT

**Used in:** `SL 3D Text Creator`
**Source:** https://github.com/opentypejs/opentype.js
**Inlined as:** UMD script block (minified)

```
The MIT License (MIT)

Copyright © Frederik De Bleser and contributors.

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### gifuct-js — MIT

**Used in:** `SL Sprite Sheet Maker`
**Source:** https://github.com/matt-way/gifuct-js
**Inlined as:** UMD script block

```
The MIT License (MIT)

Copyright (c) 2015 Matt Way

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 2. Fonts — SIL Open Font License v1.1

*(The tool UI itself uses the operating system's native font stack —
no UI webfonts are embedded. Retired copies of the former UI fonts
(Audiowide, Orbitron, Share Tech Mono, VT323 — all SIL OFL 1.1) may
still sit unused in `_shared/fonts/ui/`.)*

### 3D-Text-Creator picker fonts

Embedded as base64 TTF entries inside the page's `FONT_DATA` object
(merged in by `fonts_inline.js`).

| Font            | Copyright                              | Reserved Font Name |
| --------------- | -------------------------------------- | ------------------ |
| Pacifico        | © 2011 Vernon Adams                    | Pacifico           |
| Audiowide       | © 2011 Astigmatic (AOETI)              | Audiowide          |
| Anton           | © 2011 Vernon Adams                    | Anton              |
| Bebas Neue      | © Dharma Type                          | Bebas Neue         |
| Black Ops One   | © 2011 JM Solé                         | Black Ops One      |
| Press Start 2P  | © 2012 CodeMan38                       | Press Start 2P     |
| Righteous       | © 2011 Astigmatic (AOETI)              | Righteous          |
| Russo One       | © 2011 Jovanny Lemonad                 | Russo One          |

### Full SIL OFL v1.1 text

```
Copyright (c) <date>, <copyright holder>, with Reserved Font Name <Reserved Font Name>.

This Font Software is licensed under the SIL Open Font License,
Version 1.1. This license is copied below, and is also available with
a FAQ at: https://openfontlicense.org

-----------------------------------------------------------
SIL OPEN FONT LICENSE Version 1.1 - 26 February 2007
-----------------------------------------------------------

PREAMBLE
The goals of the Open Font License (OFL) are to stimulate worldwide
development of collaborative font projects, to support the font
creation efforts of academic and linguistic communities, and to
provide a free and open framework in which fonts may be shared and
improved in partnership with others.

The OFL allows the licensed fonts to be used, studied, modified and
redistributed freely as long as they are not sold by themselves. The
fonts, including any derivative works, can be bundled, embedded,
redistributed and/or sold with any software provided that any reserved
names are not used by derivative works. The fonts and derivatives,
however, cannot be released under any other type of license. The
requirement for fonts to remain under this license does not apply to
any document created using the fonts or their derivatives.

DEFINITIONS
"Font Software" refers to the set of files released by the Copyright
Holder(s) under this license and clearly marked as such. This may
include source files, build scripts and documentation.

"Reserved Font Name" refers to any names specified as such after the
copyright statement(s).

"Original Version" refers to the collection of Font Software
components as distributed by the Copyright Holder(s).

"Modified Version" refers to any derivative made by adding to,
deleting, or substituting -- in part or in whole -- any of the
components of the Original Version, by changing formats or by porting
the Font Software to a new environment.

"Author" refers to any designer, engineer, programmer, technical
writer or other person who contributed to the Font Software.

PERMISSION & CONDITIONS
Permission is hereby granted, free of charge, to any person obtaining
a copy of the Font Software, to use, study, copy, merge, embed,
modify, redistribute, and sell modified and unmodified copies of the
Font Software, subject to the following conditions:

1) Neither the Font Software nor any of its individual components, in
Original or Modified Versions, may be sold by itself.

2) Original or Modified Versions of the Font Software may be bundled,
redistributed and/or sold with any software, provided that each copy
contains the above copyright notice and this license. These can be
included either as stand-alone text files, human-readable headers or
in the appropriate machine-readable metadata fields within text or
binary files as long as those fields can be easily viewed by the user.

3) No Modified Version of the Font Software may use the Reserved Font
Name(s) unless explicit written permission is granted by the
corresponding Copyright Holder. This restriction only applies to the
primary font name as presented to the users.

4) The name(s) of the Copyright Holder(s) or the Author(s) of the
Font Software shall not be used to promote, endorse or advertise any
Modified Version, except to acknowledge the contribution(s) of the
Copyright Holder(s) and the Author(s) or with their explicit written
permission.

5) The Font Software, modified or unmodified, in part or in whole,
must be distributed entirely under this license, and must not be
distributed under any other license. The requirement for fonts to
remain under this license does not apply to any document created
using the Font Software.

TERMINATION
This license becomes null and void if any of the above conditions are
not met.

DISCLAIMER
THE FONT SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO ANY WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT
OF COPYRIGHT, PATENT, TRADEMARK, OR OTHER RIGHT. IN NO EVENT SHALL
THE COPYRIGHT HOLDER BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, INCLUDING ANY GENERAL, SPECIAL, INDIRECT, INCIDENTAL, OR
CONSEQUENTIAL DAMAGES, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF THE USE OR INABILITY TO USE THE FONT
SOFTWARE OR FROM OTHER DEALINGS IN THE FONT SOFTWARE.
```

---

## 3. Image assets

### Robin Wood UV templates

**Used in:** `SL Alpha Maker`
**Files:** `SL Alpha Maker/Robin Wood/SL-Avatar-Top-1024.jpg`,
            `SL Alpha Maker/Robin Wood/SL-Avatar-Bottom-1024.jpg`
**Source:** Robin Wood, 2005 — original SL avatar UV templates released
            free for community use.

The Robin Wood templates are widely redistributed in the Second Life
creator community under Robin Wood's explicit "free to use, modify,
and redistribute, but you may not sell the templates themselves"
terms. They are bundled here unmodified and credited inline in the
tool's footer.

---

## 4. Summary

| What | Where it lives | Licence | Allows redistribute? |
| ---- | -------------- | ------- | -------------------- |
| Three.js r184 | `_shared/three/`, inlined into AP + 3DText | MIT | yes |
| earcut | inlined into 3DText | ISC | yes |
| opentype.js | inlined into 3DText | MIT | yes |
| gifuct-js | inlined into Sprite Sheet Maker | MIT | yes |
| Picker fonts (Pacifico + 7 others) | `_shared/fonts/`, base64 in fonts_inline.js | SIL OFL 1.1 | yes (bundled) |
| Robin Wood UV templates | `SL Alpha Maker/Robin Wood/` | Author-granted (free use, no resale of the templates themselves) | yes |
| Retired UI fonts (unused since the Aurora redesign) | `_shared/fonts/ui/` | SIL OFL 1.1 | yes |
| Application code (UI, parsers, builders, styles; incl. Music Slicer) | each tool's HTML + `_shared/` | PolyForm Noncommercial 1.0.0 — see `LICENSE` | for noncommercial use |
