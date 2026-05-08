param(
  [string]$shared = "D:\Second Life\Tools for SL\_shared\three"
)

$core  = [Convert]::ToBase64String([IO.File]::ReadAllBytes("$shared\three.core.min.js"))
$mod   = [Convert]::ToBase64String([IO.File]::ReadAllBytes("$shared\three.module.min.js"))
$orbit = [Convert]::ToBase64String([IO.File]::ReadAllBytes("$shared\OrbitControls.js"))
$room  = [Convert]::ToBase64String([IO.File]::ReadAllBytes("$shared\RoomEnvironment.js"))

$template = @'
/* Three.js inline-loader bundle.
   Decodes base64-embedded Three.js sources, creates Blob URLs, and
   injects an importmap so the page can `import "three"` etc. without
   needing a local web server. Works on file:// and http://.

   Built from sibling files (three.core.min.js, three.module.min.js,
   OrbitControls.js, RoomEnvironment.js) by _build_inline_bundle.ps1.
*/
(function () {
  var B64_CORE  = "__CORE__";
  var B64_MOD   = "__MOD__";
  var B64_ORBIT = "__ORBIT__";
  var B64_ROOM  = "__ROOM__";

  function b64ToText(b64) {
    var bin = atob(b64);
    var bytes = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
    return new TextDecoder("utf-8").decode(bytes);
  }
  function makeBlob(text) {
    return URL.createObjectURL(new Blob([text], { type: "application/javascript" }));
  }

  var coreText = b64ToText(B64_CORE);
  var coreUrl  = makeBlob(coreText);

  // three.module.min.js imports the core via "./three.core.min.js" — rewrite
  // both occurrences to the blob URL of the inlined core so the module file
  // resolves correctly when loaded as a blob.
  var modText = b64ToText(B64_MOD)
    .replace(/['"]\.\/three\.core\.min\.js['"]/g, JSON.stringify(coreUrl));
  var moduleUrl = makeBlob(modText);

  // OrbitControls + RoomEnvironment use bare `from "three"` — these resolve
  // via the importmap below.
  var orbitUrl = makeBlob(b64ToText(B64_ORBIT));
  var roomUrl  = makeBlob(b64ToText(B64_ROOM));

  var map = document.createElement("script");
  map.type = "importmap";
  map.textContent = JSON.stringify({
    imports: {
      "three": moduleUrl,
      "three/orbit": orbitUrl,
      "three/room": roomUrl
    }
  });
  document.head.appendChild(map);
  window.__SLT_THREE_INLINE_READY = true;
})();
'@

$content = $template `
  -replace '__CORE__',  $core `
  -replace '__MOD__',   $mod `
  -replace '__ORBIT__', $orbit `
  -replace '__ROOM__',  $room

[IO.File]::WriteAllText("$shared\three_inline.js", $content, [Text.UTF8Encoding]::new($false))
$size = (Get-Item "$shared\three_inline.js").Length
Write-Host ("Wrote three_inline.js ({0:N0} bytes)" -f $size)
