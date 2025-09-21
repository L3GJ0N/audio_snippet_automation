# Audio Snippet Automation## Batch YouTube Audio Snippet Extractor



[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)Create multiple precisely trimmed audio snippets from YouTube ## Troubleshooting

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

| Problem | Cause | Fix |

Create multiple precisely trimmed audio snippets from YouTube URLs using a single CSV file.|---------|-------|-----|

| URL reported "not a valid URL" | Quotes were passed literally (older version) | Use updated script (argument list, no shell quoting) |

## Features| `yt-dlp` not found | Not installed / PATH issue | `pip install yt-dlp` ; check `yt-dlp --version` |

| `ffmpeg` not found | Not installed / PATH issue | Install via Scoop/Choco or add to PATH |

- 🎵 **Batch processing** - Process multiple videos at once| Empty output file | Cut range too short or outside duration | Verify start/end within video length |

- 📊 **CSV-driven** - Simple spreadsheet interface| Slight time inaccuracy | Container keyframe boundaries | Use `--precise` |

- 🎯 **Precise cutting** - Frame-accurate timestamps| "Sign in to confirm your age" | Age-restricted video | Add `--cookies-from-browser chrome` (or firefox, safari, etc.) |

- 🔄 **Smart caching** - Reuse downloads between runs| "Could not copy Chrome cookie database" | Browser is running / cookie locked | **Close ALL browser windows** and try again, or try `firefox` instead |

- 🌐 **Format support** - Output as M4A, MP3, or WAV

- 🔐 **Age-restricted videos** - Cookie support for restricted content### Cookie Issues (Age-restricted videos)

- 🐍 **Modern Python** - Built with modern tooling and best practices

**Problem**: `Could not copy Chrome cookie database` or similar errors.

## Quick Start

**Solutions** (try in order):

### Prerequisites1. **Close ALL browser windows** completely and try again

2. Try a different browser: `--cookies-from-browser firefox`

- **Python 3.9+**3. Export cookies manually:

- **uv** package manager ([installation guide](https://docs.astral.sh/uv/getting-started/installation/))   - Install browser extension like "Get cookies.txt"

- **ffmpeg** ([installation guide](https://ffmpeg.org/download.html))   - Export cookies for youtube.com to `cookies.txt`

   - Use: `python batch_audio_snippets.py --csv snippets.csv --cookies cookies.txt`

### Installation4. Use incognito/private mode approach (won't work for age-restricted)



```bash**Why this happens**: Browsers lock their cookie databases while running. The script can't read them when the browser is open.g a single CSV file.

# Clone the repository

git clone https://github.com/L3GJ0N/audio_snippet_automation.git### Why use this?

cd audio_snippet_automation- Batch workflow (no copying timestamps manually one-by-one)

- Supports multiple output formats (m4a, mp3, wav)

# Install with uv (recommended)- Optional frame-accurate cutting (`--precise`)

uv sync- Re-uses cached downloads if you re-run



# Or install in development mode---

uv pip install -e .## Quick Start (Windows 10/11)

```

```powershell

### Usage# 1. (Optional) Create and activate a virtual environment

python -m venv .venv

```bash./.venv/Scripts/Activate.ps1

# Using uv

uv run audio-snippet-automation --csv examples/snippets.csv# 2. Install required tools

pip install --upgrade yt-dlp

# Or if installed globally

audio-snippet-automation --csv examples/snippets.csv# 3. Install ffmpeg (choose ONE method)

# a) Scoop (recommended):

# Short alias#   Install Scoop if you don't have it:  Set-ExecutionPolicy RemoteSigned -Scope CurrentUser; iwr get.scoop.sh -useb | iex

asa --csv examples/snippets.csv#   Then:

```scoop install ffmpeg

# b) Chocolatey:

## CSV Format#   choco install ffmpeg

# c) Manual: Download static build from https://www.gyan.dev/ffmpeg/ and add its /bin folder to PATH.

Create a CSV file with the following columns:

# 4. Verify tools

| Column  | Required | Description |yt-dlp --version

|---------|----------|-------------|ffmpeg -version

| `url`   | ✅ | YouTube URL (any format) |

| `start` | ✅ | Start time: `SS(.ms)` or `HH:MM:SS(.ms)` |# 5. Run using the provided CSV

| `end`   | ✅ | End time (same format as start) |python batch_audio_snippets.py --csv snippets.csv --format m4a --outdir snippets --tempdir downloads

| `output`| ❌ | Custom filename (without extension) |```

| `format`| ❌ | Override format (`m4a`, `mp3`, `wav`) |

After running, trimmed files appear in `snippets/`. Source downloads (cached) are stored in `downloads/`.

### Example CSV

---

```csv## CSV Format

url,start,end,output,formatFile must have a header row. Columns:

https://www.youtube.com/watch?v=dQw4w9WgXcQ,00:00:05,00:00:12,rick-intro,m4a

https://youtu.be/dQw4w9WgXcQ,5,12,rick-chorus,mp3| Column  | Required | Description |

```|---------|----------|-------------|

| url     | yes      | Full YouTube link (any normal watch or youtu.be URL) |

## Command Options| start   | yes      | Start time: `SS(.ms)` or `HH:MM:SS(.ms)` |

| end     | yes      | End time (same formats). Must be > start |

```bash| output  | no       | Base filename (without extension). If blank, video ID is used |

audio-snippet-automation --help| format  | no       | Override format for that row (`m4a`, `mp3`, `wav`) |

```

Example (`snippets.csv`) currently in this repo:

| Option | Description | Default |```

|--------|-------------|---------|url,start,end,output,format

| `--csv PATH` | CSV file with jobs | Required |https://www.youtube.com/watch?v=42N62Z5E7-s,00:00:01,00:00:03,avengers_assemble,m4a

| `--format {m4a,mp3,wav}` | Default output format | `m4a` |https://www.youtube.com/watch?v=42N62Z5E7-s,00:00:03,00:00:05,thanos-like_to_lose,m4a

| `--precise` | Frame-accurate cuts (slower) | Fast copy |```

| `--outdir DIR` | Output directory | `snippets` |

| `--tempdir DIR` | Cache directory | `downloads` |> Tip: You can copy a watch URL and tweak timestamps by scrubbing in the YouTube player and using the "Copy debug info" time or just manual entry.

| `--cookies-from-browser BROWSER` | Browser cookies for age-restricted videos | None |

| `--cookies PATH` | Cookie file for age-restricted videos | None |---

## Command Reference

### Examples

| Option | Purpose |

```bash|--------|---------|

# Basic usage| `--csv PATH` | (Required) Path to CSV file |

uv run asa --csv my-clips.csv| `--format m4a|mp3|wav` | Default output format when a row omits the `format` column |

| `--precise` | Re-encode for frame-accurate cuts (slower, quality maintained) |

# Custom output format and directories| `--outdir DIR` | Where final snippets are written (default `snippets`) |

uv run asa --csv clips.csv --format mp3 --outdir my-snippets| `--tempdir DIR` | Where source downloads are cached (default `downloads`) |

| `--cookies-from-browser BROWSER` | Extract cookies from browser for age-restricted videos (chrome, firefox, safari, etc.) |

# Precise cuts (re-encode for accuracy)

uv run asa --csv clips.csv --precise### Example (matches repo data)

```powershell

# Age-restricted videos (browser cookies)python batch_audio_snippets.py --csv .\snippets.csv --format m4a --outdir .\snippets --tempdir .\downloads

uv run asa --csv clips.csv --cookies-from-browser chrome```



# Age-restricted videos (cookie file)### Producing MP3 instead

uv run asa --csv clips.csv --cookies cookies.txt```powershell

```python batch_audio_snippets.py --csv .\snippets.csv --format mp3

```

## Development

### Frame-accurate cuts (use if edges are off)

### Setup Development Environment```powershell

python batch_audio_snippets.py --csv .\snippets.csv --precise

```bash```

# Clone and setup

git clone https://github.com/L3GJ0N/audio_snippet_automation.git### Age-restricted videos (requires browser cookies)

cd audio_snippet_automation```powershell

python batch_audio_snippets.py --csv .\snippets.csv --cookies-from-browser chrome

# Install with dev dependencies```

uv sync --extra dev

---

# Install pre-commit hooks## How It Works

uv run pre-commit install1. Reads each CSV row

```2. Fetches the video ID (`yt-dlp --get-id`)

3. Downloads best audio (cached in `downloads/`)

### Running Tests4. Cuts with `ffmpeg` (fast stream copy or precise re-encode)

5. Converts / renames to desired format

```bash

# Run all testsRe-running with the same CSV is fast because existing downloads are reused.

uv run pytest

---

# Run with coverage## Troubleshooting

uv run pytest --cov

| Problem | Cause | Fix |

# Run specific test|---------|-------|-----|

uv run pytest tests/test_core.py::test_time_str| URL reported “not a valid URL” | Quotes were passed literally (older version) | Use updated script (argument list, no shell quoting) |

```| `yt-dlp` not found | Not installed / PATH issue | `pip install yt-dlp` ; check `yt-dlp --version` |

| `ffmpeg` not found | Not installed / PATH issue | Install via Scoop/Choco or add to PATH |

### Code Quality| Empty output file | Cut range too short or outside duration | Verify start/end within video length |

| Slight time inaccuracy | Container keyframe boundaries | Use `--precise` |

```bash

# Format codeLog lines beginning with `[CMD]` show the exact tool invocations.

uv run black .

---

# Lint code## FAQ

uv run ruff check .**Q: Will it download playlists?**  No, `--no-playlist` is enforced.



# Type checking (if mypy is added)**Q: Can I mix formats per row?**  Yes—add the `format` column value.

uv run mypy src/

```**Q: How do I get milliseconds?**  Use `HH:MM:SS.mmm` (e.g., `00:01:12.350`).



## Troubleshooting**Q: Can I keep original full audio?**  It’s cached already in `downloads/` as M4A.



| Problem | Solution |---

|---------|----------|## Development Notes

| `yt-dlp not found` | Install with `uv add yt-dlp` or system package manager |Python standard library only. No external dependencies besides `yt-dlp` & `ffmpeg` executables.

| `ffmpeg not found` | Install ffmpeg and add to PATH |

| Cookie database error | Close browser completely, try different browser, or use cookie file |### Pre-commit Hooks (Black formatting)

| Permission errors | Check file permissions, run with appropriate user rights |This repo can automatically format code before each commit using [pre-commit] and Black.



### Age-Restricted VideosSetup (once):

```powershell

When encountering "Sign in to confirm your age" errors:pip install -r requirements-dev.txt

pre-commit install

1. **Close browser completely** and retry with `--cookies-from-browser chrome````

2. **Try different browser**: `--cookies-from-browser firefox`

3. **Export cookies manually**:Run hooks on all files manually:

   - Install browser extension like "Get cookies.txt LOCALLY"```powershell

   - Export YouTube cookies to `cookies.txt`pre-commit run --all-files

   - Use `--cookies cookies.txt````



## Project StructureUpdate hook versions later:

```powershell

```pre-commit autoupdate

audio_snippet_automation/git add .pre-commit-config.yaml

├── src/```

│   └── audio_snippet_automation/

│       ├── __init__.pyIf a commit is blocked, fix/accept Black changes, then:

│       ├── cli.py           # Command-line interface```powershell

│       └── core.py          # Core functionalitygit add .

├── tests/git commit -m "Your message"

│   ├── __init__.py```

│   └── test_core.py

├── examples/

│   └── snippets.csv         # Example CSV file
├── docs/                    # Documentation
├── pyproject.toml          # Project configuration
├── README.md
└── .gitignore
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Run the test suite
6. Submit a pull request

## Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube downloader
- [FFmpeg](https://ffmpeg.org/) - Audio/video processing
- [uv](https://github.com/astral-sh/uv) - Modern Python package manager
