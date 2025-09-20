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
import shlex  # still used for pretty logging on non-Windows

def which(cmd):
    from shutil import which as _which
    return _which(cmd) is not None

def die(msg, code=1):
    print(f"[ERROR] {msg}", file=sys.stderr)
    sys.exit(code)

def _log_cmd(args):
    def _q(a):
        # Pretty-print only; we are NOT passing through a shell
        if os.name == 'nt':
            # simple rule: quote with double quotes if space or special chars
            if any(c.isspace() for c in a) or any(c in '()[]{}&|^=;!,`' for c in a):
                return f'"{a}"'
            return a
        else:
            return shlex.quote(a)
    print("[CMD] " + " ".join(_q(str(a)) for a in args))

def run(args, cwd=None):
    if isinstance(args, str):  # backward safety
        # fall back to shell execution (legacy) but warn
        print("[WARN] run() received string; prefer list of args.")
        print(f"[CMD] {args}")
        proc = subprocess.run(args, shell=True, cwd=cwd)
    else:
        _log_cmd(args)
        proc = subprocess.run(args, cwd=cwd)
    if proc.returncode != 0:
        die(f"Command failed with exit code {proc.returncode}")

def run_get_output(args):
    # returns stdout as str
    if isinstance(args, str):
        print("[WARN] run_get_output() received string; prefer list of args.")
        print(f"[CMD] {args}")
        proc = subprocess.run(args, shell=True, capture_output=True, text=True)
    else:
        _log_cmd(args)
        proc = subprocess.run(args, capture_output=True, text=True)
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

def add_cookie_args(args_list, cookie_browser):
    """Add cookie arguments to yt-dlp command with error handling"""
    if not cookie_browser:
        return args_list
    
    # Try cookies-from-browser first
    return args_list + ['--cookies-from-browser', cookie_browser]

def run_with_cookie_fallback(args_list, cookie_browser, cookie_file, url):
    """Run yt-dlp command with cookie fallback on failure"""
    # Determine cookie method
    if cookie_file:
        try:
            return run_get_output(args_list + ['--cookies', cookie_file, url])
        except SystemExit:
            print("[ERROR] Failed with cookie file. Check that the file exists and is valid.")
            raise
    
    if not cookie_browser:
        return run_get_output(args_list + [url])
    
    # Try with cookies from browser
    try:
        cookie_args = args_list + ['--cookies-from-browser', cookie_browser, url]
        return run_get_output(cookie_args)
    except SystemExit:
        # Cookie extraction failed, suggest solutions and try without cookies
        print(f"[WARN] Cookie extraction from {cookie_browser} failed.")
        print("[WARN] This usually happens when the browser is running.")
        print("[WARN] Try: 1) Close all browser windows, 2) Use --cookies file instead, or 3) Try without cookies.")
        print("[WARN] Attempting without cookies...")
        
        try:
            return run_get_output(args_list + [url])
        except SystemExit:
            print("[ERROR] Failed both with and without cookies. Video may be age-restricted and require authentication.")
            print("[HELP] Solutions:")
            print(f"[HELP] 1. Close ALL {cookie_browser} windows and try again")
            print("[HELP] 2. Export cookies manually: https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp")
            print("[HELP] 3. Use a different browser (try --cookies-from-browser firefox)")
            raise

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, help="Path to CSV with jobs")
    parser.add_argument("--format", default="m4a", choices=["m4a", "mp3", "wav"], help="Default output format")
    parser.add_argument("--precise", action="store_true", help="Re-encode for precise cuts (useful if copy cuts are off)")
    parser.add_argument("--outdir", default="snippets", help="Output directory")
    parser.add_argument("--tempdir", default="downloads", help="Temp download dir")
    parser.add_argument("--cookies-from-browser", help="Browser to extract cookies from (chrome, firefox, safari, etc.) for age-restricted videos")
    parser.add_argument("--cookies", help="Path to cookies.txt file for age-restricted videos")
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
            # Use fallback function to handle cookie extraction errors
            get_id_args = ['yt-dlp', '--no-playlist', '--get-id']
            vid = run_with_cookie_fallback(get_id_args, getattr(args, 'cookies_from_browser', None), getattr(args, 'cookies', None), url)
            
            # 2) Download best audio as M4A into tempdir
            temp_audio = os.path.join(args.tempdir, f"{vid}.m4a")
            if not os.path.exists(temp_audio):
                dl_args = [
                    'yt-dlp', '-x', '--audio-format', 'm4a',
                    '-o', os.path.join(args.tempdir, '%(id)s.%(ext)s'),
                    '--no-playlist'
                ]
                # Handle cookies for download
                try:
                    if getattr(args, 'cookies', None):
                        cookie_dl_args = dl_args + ['--cookies', args.cookies, url]
                        run(cookie_dl_args)
                    elif getattr(args, 'cookies_from_browser', None):
                        cookie_dl_args = dl_args + ['--cookies-from-browser', args.cookies_from_browser, url]
                        run(cookie_dl_args)
                    else:
                        run(dl_args + [url])
                except SystemExit:
                    if getattr(args, 'cookies_from_browser', None):
                        print("[WARN] Download with cookies failed, trying without cookies...")
                        run(dl_args + [url])
                    else:
                        raise
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
                ff_cut = [
                    'ffmpeg', '-y', '-ss', start, '-to', end, '-i', temp_audio,
                    '-c:a', 'aac', '-b:a', '192k', cut_tmp
                ]
            else:
                ff_cut = [
                    'ffmpeg', '-y', '-ss', start, '-to', end, '-i', temp_audio,
                    '-c', 'copy', cut_tmp
                ]
            run(ff_cut)

            # 5) Convert to requested format if needed
            final_path = f"{out_path_noext}.{fmt}"
            if fmt == "m4a":
                # Already m4a; just rename
                if os.path.exists(final_path):
                    os.remove(final_path)
                os.replace(cut_tmp, final_path)
            elif fmt == "mp3":
                run(['ffmpeg', '-y', '-i', cut_tmp, '-q:a', '2', final_path])
                os.remove(cut_tmp)
            elif fmt == "wav":
                run(['ffmpeg', '-y', '-i', cut_tmp, final_path])
                os.remove(cut_tmp)

            print(f"[OK] Wrote {final_path}")

    print("[DONE] All jobs processed.")

if __name__ == "__main__":
    main()
