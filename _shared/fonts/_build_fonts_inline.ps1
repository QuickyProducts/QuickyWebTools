param(
  [string]$dir = "D:\Second Life\Tools for SL\_shared\fonts"
)

# Build fonts_inline.js by base64-encoding all .ttf files in this folder
# and merging them into the page's FONT_DATA constant.

$entries = @()
foreach ($f in Get-ChildItem $dir -Filter *.ttf | Sort-Object Name) {
  $b64 = [Convert]::ToBase64String([IO.File]::ReadAllBytes($f.FullName))
  $name = $f.BaseName
  $entries += '  "' + $name + '": "' + $b64 + '"'
}

$header = @'
/* Extra fonts for SL 3D Text Creator. Each entry is a base64-encoded TTF
   file. Decoded and parsed by opentype.js the same way as the inline
   Pacifico font. Built from the .ttf files in this folder by
   _build_fonts_inline.ps1.
   All fonts here are SIL Open Font License (free + redistributable).

   Note: the Pacifico FONT_DATA is declared as `const` in the inline script
   just before this one. We use Object.assign on the object directly —
   const binds the reference, not the contents, so mutating works. */
Object.assign(FONT_DATA, {
'@

$footer = @'
});
'@

$body = ($entries -join ",`n")
$content = $header + "`n" + $body + "`n" + $footer + "`n"
[IO.File]::WriteAllText("$dir\fonts_inline.js", $content, [Text.UTF8Encoding]::new($false))
$size = (Get-Item "$dir\fonts_inline.js").Length
Write-Host ("Wrote fonts_inline.js ({0:N0} bytes, {1} fonts)" -f $size, $entries.Count)
