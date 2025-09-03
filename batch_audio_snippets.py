#!/usr/bin/env python3
"""
Batch downloader + snipper for YouTube audio.

Requirements:
  - yt-dlp  (https://github.com/yt-dlp/yt-dlp)
  - ffmpeg  (https://ffmpeg.org/)
Install on macOS:  brew install yt-dlp ffmpeg
Install on Linux:  sudo apt-get install ffmpeg && pip install yt-dlp
Install on Windows:
  - Install ffmpeg and add it to PATH
  - pip install yt-dlp

Usage:
  1) Put your jobs in snippets.csv (see columns below).
  2) Run:  python batch_audio_snippets.py --csv snippets.csv
     Optional flags:
       --format m4a|mp3|wav     (default: m4a)
       --precise                (re-encode for frame-accurate cuts; slower)
       --outdir PATH            (default: ./snippets)
       --tempdir PATH           (default: ./downloads)

CSV columns (header required):
  url,start,end,output,format
  - url:     YouTube link
  - start:   HH:MM:SS(.ms) or seconds (e.g., 90.5)
  - end:     HH:MM:SS(.ms) or seconds
  - output:  (optional) filename without extension
  - format:  (optional) m4a|mp3|wav (overrides --format per-row)

Examples:
  url,start,end,output,format
  https://www.youtube.com/watch?v=dQw4w9WgXcQ,00:00:05,00:00:12,rick-intro,m4a
  https://youtu.be/dQw4w9WgXcQ,5,12,,mp3
"""
import csv
import os
import subprocess
import sys
import argparse
import shlex

def which(cmd):
    from shutil import which as _which
    return _which(cmd) is not None

def die(msg, code=1):
    print(f"[ERROR] {msg}", file=sys.stderr)
    sys.exit(code)

def run(cmd, cwd=None):
    print(f"[CMD] {cmd}")
    proc = subprocess.run(cmd, shell=True, cwd=cwd)
    if proc.returncode != 0:
        die(f"Command failed with exit code {proc.returncode}")

def run_get_output(cmd):
    # returns stdout as str
    print(f"[CMD] {cmd}")
    proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if proc.returncode != 0:
        die(f"Command failed with exit code {proc.returncode}: {proc.stderr.strip()}")
    return proc.stdout.strip()

def ensure_tools():
    if not which("yt-dlp"):
        die("yt-dlp not found in PATH. Install it (e.g., 'pip install yt-dlp').")
    if not which("ffmpeg"):
        die("ffmpeg not found in PATH. Install it and ensure it's on PATH.")

def time_str(t):
    # pass-through; allow "SS.sss" or "HH:MM:SS(.sss)"
    return str(t).strip()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, help="Path to CSV with jobs")
    parser.add_argument("--format", default="m4a", choices=["m4a", "mp3", "wav"], help="Default output format")
    parser.add_argument("--precise", action="store_true", help="Re-encode for precise cuts (useful if copy cuts are off)")
    parser.add_argument("--outdir", default="snippets", help="Output directory")
    parser.add_argument("--tempdir", default="downloads", help="Temp download dir")
    args = parser.parse_args()

    ensure_tools()
    os.makedirs(args.outdir, exist_ok=True)
    os.makedirs(args.tempdir, exist_ok=True)

    with open(args.csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required = {"url", "start", "end"}
        if not required.issubset(set(reader.fieldnames or [])):
            die(f"CSV must include columns: {', '.join(sorted(required))} (plus optional 'output', 'format')")

        for i, row in enumerate(reader, 1):
            url = (row.get("url") or "").strip()
            start = time_str(row.get("start") or "")
            end = time_str(row.get("end") or "")
            out_base = (row.get("output") or "").strip()
            fmt = (row.get("format") or "").strip().lower() or args.format

            if not url or not start or not end:
                print(f"[WARN] Row {i} missing url/start/end. Skipping.")
                continue

            # 1) Get video ID to create stable temp filename
            vid = run_get_output(f'yt-dlp --no-playlist --get-id {shlex.quote(url)}')
            # 2) Download best audio as M4A into tempdir
            temp_audio = os.path.join(args.tempdir, f"{vid}.m4a")
            dl_cmd = (
                f'yt-dlp -x --audio-format m4a '
                f'-o {shlex.quote(os.path.join(args.tempdir, "%(id)s.%(ext)s"))} '
                f'--no-playlist {shlex.quote(url)}'
            )
            if not os.path.exists(temp_audio):
                run(dl_cmd)
            else:
                print(f"[INFO] Using cached: {temp_audio}")

            # 3) Determine output name
            if not out_base:
                out_base = vid

            # 4) Cut the desired range
            # Fast (stream copy) vs precise (re-encode)
            out_path_noext = os.path.join(args.outdir, out_base)
            cut_tmp = out_path_noext + ".cut.m4a"
            if args.precise:
                # re-encode to AAC for accurate cut
                ff_cut = (
                    f'ffmpeg -y -ss {start} -to {end} -i {shlex.quote(temp_audio)} '
                    f'-c:a aac -b:a 192k {shlex.quote(cut_tmp)}'
                )
            else:
                # fast stream copy (may cut a few ms off depending on container)
                ff_cut = (
                    f'ffmpeg -y -ss {start} -to {end} -i {shlex.quote(temp_audio)} '
                    f'-c copy {shlex.quote(cut_tmp)}'
                )
            run(ff_cut)

            # 5) Convert to requested format if needed
            final_path = f"{out_path_noext}.{fmt}"
            if fmt == "m4a":
                # Already m4a; just rename
                if os.path.exists(final_path):
                    os.remove(final_path)
                os.replace(cut_tmp, final_path)
            elif fmt == "mp3":
                run(f'ffmpeg -y -i {shlex.quote(cut_tmp)} -q:a 2 {shlex.quote(final_path)}')
                os.remove(cut_tmp)
            elif fmt == "wav":
                run(f'ffmpeg -y -i {shlex.quote(cut_tmp)} {shlex.quote(final_path)}')
                os.remove(cut_tmp)

            print(f"[OK] Wrote {final_path}")

    print("[DONE] All jobs processed.")

if __name__ == "__main__":
    main()
