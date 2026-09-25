---
name: cover-zoom
description: Make the animated zoom GIF for Alyssa's "Step up Step together" personal-essay covers (full cover → desk orange → essay panel → back out). Trigger phrases — "cover zoom", "make the zoom gif", "animate this cover".
---

# Cover zoom

Every personal-essay cover shares a template: script header, desk orange + title sign on the left, essay-specific panel on the right. The GIF starts on the full cover (the series signal), follows the desk orange's gaze right, and lands on the panel (the essay's distinctive moment).

## Steps

1. Read the image (note the display scale in the Read result — box coords must be in **original** pixels).
2. Pick two 16:10 boxes (W/H = 1.6):
   - **desk**: desk orange + monitor, whole desk incl. wheels, a bit of sign bottom OK.
   - **panel**: the right panel's key moment. Nothing cut off — keep full characters (feet included) and the whole speech bubble.
3. Run:
   ```
   python3 ~/src/ai-builder-toolkit/tools/cover-zoom/cover_zoom.py IMAGE ~/Downloads/<slug>-zoom.gif --desk X,Y,W,H --panel X,Y,W,H
   ```
4. Spot-check the desk and panel frames if unsure, then `open -a Safari` the GIF.

## Locked decisions

- Rhythm: drag, pause, drag, pause, drag. Holds: full 0.3s, desk 0.5s, panel 0.7s. Don't lengthen the panel pause — nobody needs to read the bubble; long holds look like the GIF ended.
- 800×500, 20fps, ~6 MB. Timing lives in `TIMING` in `tools/cover-zoom/cover_zoom.py`.

Reference boxes ("child of immigrants", 2400×1500): desk `24,708,1200,750`, panel `972,270,1296,810`.
