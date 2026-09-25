#!/usr/bin/env python3
"""Personal-essay cover zoom GIF: full cover -> desk orange -> essay panel -> back out.

Rhythm (locked with Alyssa 2026-09-25): drag, pause, drag, pause, drag.

Usage:
  cover_zoom.py IMAGE OUT.gif --desk X,Y,W,H --panel X,Y,W,H
Boxes are in the image's own pixels and must be 16:10 (W/H = 1.6).
"""
import argparse, os, subprocess, tempfile
from PIL import Image

FPS = 20
OUT_SIZE = (800, 500)
# (from, to, seconds) — from == to means hold
TIMING = [("full", "full", 0.3), ("full", "desk", 0.9), ("desk", "desk", 0.5),
          ("desk", "panel", 1.1), ("panel", "panel", 0.7), ("panel", "full", 1.0)]

def ease(t): return t * t * (3 - 2 * t)

def box(s): return [float(v) for v in s.split(",")]

def main():
    p = argparse.ArgumentParser()
    p.add_argument("image"); p.add_argument("out")
    p.add_argument("--desk", required=True, type=box)
    p.add_argument("--panel", required=True, type=box)
    a = p.parse_args()

    src = Image.open(a.image).convert("RGB")
    W, H = src.size
    # full frame, trimmed to 16:10 around center if needed
    fw, fh = (W, W / 1.6) if W / H <= 1.6 else (H * 1.6, H)
    boxes = {"full": [(W - fw) / 2, (H - fh) / 2, fw, fh], "desk": a.desk, "panel": a.panel}

    with tempfile.TemporaryDirectory() as d:
        n = 0
        for f, t, sec in TIMING:
            A, B = boxes[f], boxes[t]
            for i in range(int(sec * FPS)):
                e = ease(i / int(sec * FPS))
                x, y, w, h = [A[j] + (B[j] - A[j]) * e for j in range(4)]
                src.resize(OUT_SIZE, Image.LANCZOS, box=(x, y, x + w, y + h)).save(f"{d}/{n:04d}.png")
                n += 1
        pal = f"{d}/pal.png"
        run = lambda *args: subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args], check=True)
        run("-framerate", str(FPS), "-i", f"{d}/%04d.png", "-vf", "palettegen=stats_mode=diff", pal)
        run("-framerate", str(FPS), "-i", f"{d}/%04d.png", "-i", pal,
            "-lavfi", "paletteuse=dither=sierra2_4a", "-loop", "0", a.out)
    print(f"{a.out}  {n} frames  {os.path.getsize(a.out)/1e6:.1f} MB")

if __name__ == "__main__":
    main()
