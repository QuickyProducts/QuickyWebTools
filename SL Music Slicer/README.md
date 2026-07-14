# SL Music Slicer

Song-length music playback in Second Life despite the 30-second sound-clip limit: this browser tool slices songs into perfectly named ≤30s WAV clips. A companion in-world LSD-backed player script (not part of this repository) streams them back gaplessly - the clip naming spec below is the contract between the two.

> **Music rights:** this is a tool, not a music source. Only slice and
> upload audio you have the rights to use (your own work, licensed
> tracks, royalty-free music). Uploading copyrighted music to Second
> Life without permission violates the SL Terms of Service and the
> rights holder's copyright.

## Files

- **sl_music_slicer.html** (single standalone file) - local browser tool (open it directly). No dependencies, works offline.

## Workflow

1. Drop songs (mp3/wav/flac/ogg/m4a) into the slicer. The title fills itself from the file's **embedded metadata tags** as `Artist - Songtitle` (ID3v1/v2, Vorbis comments, iTunes atoms, WAV INFO - read locally, no internet); files without tags fall back to the cleaned filename. Edit freely - a title you typed is never overwritten by late-arriving tags. It becomes the display name in SL.
2. Trim: click the wave to place the playhead, hit **✂ Cut**, then choose *delete front part* or *delete back part* (for junk before/after the song). Fine-tuning: drag the green/red handles or `[` / `]` keys. Click a clip number to hear across that boundary.
3. Export → ZIP download (per song, or **Export ALL** for one big ZIP). Inside, every song has **its own folder named after its title** with its clips (16-bit / 44.1 kHz WAV, SL-upload-ready). Unzip it wherever you like. Tick **"No folders in ZIP"** under the Export-ALL button to put all clips at the top level instead - handy for bulk-uploading everything in a single go (clip names stay unique because they start with the song title).
4. In the SL viewer: **bulk upload** the .wav files from a song's folder (L$10 each).
5. Drag the uploaded sound clips into your player prim. (The companion
   MusicPlayer script that consumes these clips is not part of this
   repository - any player that understands the naming spec below works.)

## Clip naming spec (the contract between tool and player)

```
<Title>~NN-TT~D[.D].wav      e.g.  Haddaway - What Is Love (Extended)~03-08~30.wav
                                   Haddaway - What Is Love (Extended)~08-08~9.7.wav
```

- `NN` = part number, `TT` = total parts (2-digit, so ≤99 parts ≈ 49 min max), then **this clip's duration in seconds** (full clips are exactly `30`; the last clip carries its real length, 1 decimal) - the script schedules its timer from this, so the short last clip never leaves dead air.
- The scanner tolerates the older, longer form `<Title> ~NN-TT~DD.DD` too (it splits on `~` and trims) - already-uploaded clips keep working.
- Title may not contain `~ \ / : * ? " < > | [ ]` (tool strips them). Full clip name ≤63 bytes → title ≤52 bytes: the input caps typing, and export auto-shortens anything still over with an ℹ note in the log - never a hard error.
- Zero-padded numbers make prim inventory (alphabetical) return parts in order, so a player can group consecutive same-title items reliably.

## Slicer details

- Slicing is fixed and predictable: full 30s clips + one shorter last clip, no settings. Trimmed length + clip count show top-left inside the waveform (amber when the tail lands under 3s). If SL ever rejects a 30.00s clip, change `maxLen: 30` in sl_music_slicer.html to 29.9.
- **Auto-mastering, zero settings**: export is always **mono** (SL downmixes uploads anyway - half the file size, identical in-world) and every song is loudness-normalized to the same loud-but-clean level: gated-RMS measurement → gain toward −10.5 dB → 2ms-lookahead brickwall limiter at −0.26 dB ceiling (max ~6 dB of peak taming for very dynamic sources; quiet tracks get boosted, hot masters get pulled down - the whole playlist ends up equally loud, never distorted). The export log reports the applied gain per song. Preview plays through the same gain + a limiter so you hear roughly the export loudness. Sources are resampled to 44.1 kHz automatically.
- De-click boundary fades and song fade in/out still exist as internal constants (`declick`, `fadeIn`, `fadeOut` per song, default 0) - no UI.

## Troubleshooting

- **Upload rejects a 30.00s clip**: change `maxLen: 30` to `29.9` in sl_music_slicer.html (song object defaults) and re-export.
- **Tiny click/blip exactly at clip boundaries in-world**: viewer-side artifact - re-export with a 3-5ms de-click fade (`declick` constant in sl_music_slicer.html).
