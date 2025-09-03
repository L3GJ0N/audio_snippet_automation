## Batch YouTube Audio Snippet Extractor

Create multiple precisely trimmed audio snippets from YouTube URLs using a single CSV file.

### Why use this?
- Batch workflow (no copying timestamps manually one-by-one)
- Supports multiple output formats (m4a, mp3, wav)
- Optional frame-accurate cutting (`--precise`)
- Re-uses cached downloads if you re-run

---
## Quick Start (Windows 10/11)

```powershell
# 1. (Optional) Create and activate a virtual environment
python -m venv .venv
./.venv/Scripts/Activate.ps1

# 2. Install required tools
pip install --upgrade yt-dlp

# 3. Install ffmpeg (choose ONE method)
# a) Scoop (recommended):
#   Install Scoop if you don't have it:  Set-ExecutionPolicy RemoteSigned -Scope CurrentUser; iwr get.scoop.sh -useb | iex
#   Then:
scoop install ffmpeg
# b) Chocolatey:
#   choco install ffmpeg
# c) Manual: Download static build from https://www.gyan.dev/ffmpeg/ and add its /bin folder to PATH.

# 4. Verify tools
yt-dlp --version
ffmpeg -version

# 5. Run using the provided CSV
python batch_audio_snippets.py --csv snippets.csv --format m4a --outdir snippets --tempdir downloads
```

After running, trimmed files appear in `snippets/`. Source downloads (cached) are stored in `downloads/`.

---
## CSV Format
File must have a header row. Columns:

| Column  | Required | Description |
|---------|----------|-------------|
| url     | yes      | Full YouTube link (any normal watch or youtu.be URL) |
| start   | yes      | Start time: `SS(.ms)` or `HH:MM:SS(.ms)` |
| end     | yes      | End time (same formats). Must be > start |
| output  | no       | Base filename (without extension). If blank, video ID is used |
| format  | no       | Override format for that row (`m4a`, `mp3`, `wav`) |

Example (`snippets.csv`) currently in this repo:
```
url,start,end,output,format
https://www.youtube.com/watch?v=42N62Z5E7-s,00:00:01,00:00:03,avengers_assemble,m4a
https://www.youtube.com/watch?v=42N62Z5E7-s,00:00:03,00:00:05,thanos-like_to_lose,m4a
```

> Tip: You can copy a watch URL and tweak timestamps by scrubbing in the YouTube player and using the "Copy debug info" time or just manual entry.

---
## Command Reference

| Option | Purpose |
|--------|---------|
| `--csv PATH` | (Required) Path to CSV file |
| `--format m4a|mp3|wav` | Default output format when a row omits the `format` column |
| `--precise` | Re-encode for frame-accurate cuts (slower, quality maintained) |
| `--outdir DIR` | Where final snippets are written (default `snippets`) |
| `--tempdir DIR` | Where source downloads are cached (default `downloads`) |

### Example (matches repo data)
```powershell
python batch_audio_snippets.py --csv .\snippets.csv --format m4a --outdir .\snippets --tempdir .\downloads
```

### Producing MP3 instead
```powershell
python batch_audio_snippets.py --csv .\snippets.csv --format mp3
```

### Frame-accurate cuts (use if edges are off)
```powershell
python batch_audio_snippets.py --csv .\snippets.csv --precise
```

---
## How It Works
1. Reads each CSV row
2. Fetches the video ID (`yt-dlp --get-id`)
3. Downloads best audio (cached in `downloads/`)
4. Cuts with `ffmpeg` (fast stream copy or precise re-encode)
5. Converts / renames to desired format

Re-running with the same CSV is fast because existing downloads are reused.

---
## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| URL reported “not a valid URL” | Quotes were passed literally (older version) | Use updated script (argument list, no shell quoting) |
| `yt-dlp` not found | Not installed / PATH issue | `pip install yt-dlp` ; check `yt-dlp --version` |
| `ffmpeg` not found | Not installed / PATH issue | Install via Scoop/Choco or add to PATH |
| Empty output file | Cut range too short or outside duration | Verify start/end within video length |
| Slight time inaccuracy | Container keyframe boundaries | Use `--precise` |

Log lines beginning with `[CMD]` show the exact tool invocations.

---
## FAQ
**Q: Will it download playlists?**  No, `--no-playlist` is enforced.

**Q: Can I mix formats per row?**  Yes—add the `format` column value.

**Q: How do I get milliseconds?**  Use `HH:MM:SS.mmm` (e.g., `00:01:12.350`).

**Q: Can I keep original full audio?**  It’s cached already in `downloads/` as M4A.

---
## Development Notes
Python standard library only. No external dependencies besides `yt-dlp` & `ffmpeg` executables.

