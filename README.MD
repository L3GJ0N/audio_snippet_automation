# Audio Snippet Automation# Audio Snippet Automation## Batch YouTube Audio Snippet Extractor



[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)Create multiple precisely trimmed audio snippets from YouTube ## Troubleshooting

Create multiple precisely trimmed audio snippets from YouTube URLs using a single CSV file.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

| Problem | Cause | Fix |

- 🎵 **Batch processing** - Process multiple videos at once

- 📊 **CSV-driven** - Simple spreadsheet interfaceCreate multiple precisely trimmed audio snippets from YouTube URLs using a single CSV file.|---------|-------|-----|

- 🎯 **Precise cutting** - Frame-accurate timestamps

- 🔄 **Smart caching** - Reuse downloads between runs| URL reported "not a valid URL" | Quotes were passed literally (older version) | Use updated script (argument list, no shell quoting) |

- 🌐 **Format support** - Output as M4A, MP3, or WAV

- 🔐 **Age-restricted videos** - Cookie support for restricted content## Features| `yt-dlp` not found | Not installed / PATH issue | `pip install yt-dlp` ; check `yt-dlp --version` |

- 🐍 **Modern Python** - Built with modern tooling and best practices

| `ffmpeg` not found | Not installed / PATH issue | Install via Scoop/Choco or add to PATH |

## Quick Start

- 🎵 **Batch processing** - Process multiple videos at once| Empty output file | Cut range too short or outside duration | Verify start/end within video length |

### Prerequisites

- 📊 **CSV-driven** - Simple spreadsheet interface| Slight time inaccuracy | Container keyframe boundaries | Use `--precise` |

- **Python 3.9+**

- **uv** package manager ([installation guide](https://docs.astral.sh/uv/getting-started/installation/))- 🎯 **Precise cutting** - Frame-accurate timestamps| "Sign in to confirm your age" | Age-restricted video | Add `--cookies-from-browser chrome` (or firefox, safari, etc.) |

- **ffmpeg** ([installation guide](https://ffmpeg.org/download.html))

- 🔄 **Smart caching** - Reuse downloads between runs| "Could not copy Chrome cookie database" | Browser is running / cookie locked | **Close ALL browser windows** and try again, or try `firefox` instead |

### Installation

- 🌐 **Format support** - Output as M4A, MP3, or WAV

```bash

# Clone the repository- 🔐 **Age-restricted videos** - Cookie support for restricted content### Cookie Issues (Age-restricted videos)

git clone https://github.com/L3GJ0N/audio_snippet_automation.git

cd audio_snippet_automation- 🐍 **Modern Python** - Built with modern tooling and best practices



# Install with uv (recommended)**Problem**: `Could not copy Chrome cookie database` or similar errors.

uv sync

## Quick Start

# Or install in development mode

uv pip install -e .**Solutions** (try in order):

```

### Prerequisites1. **Close ALL browser windows** completely and try again

### Usage

2. Try a different browser: `--cookies-from-browser firefox`

```bash

# Using uv- **Python 3.9+**3. Export cookies manually:

uv run audio-snippet-automation --csv examples/snippets.csv

- **uv** package manager ([installation guide](https://docs.astral.sh/uv/getting-started/installation/))   - Install browser extension like "Get cookies.txt"

# Or if installed globally

audio-snippet-automation --csv examples/snippets.csv- **ffmpeg** ([installation guide](https://ffmpeg.org/download.html))   - Export cookies for youtube.com to `cookies.txt`



# Short alias   - Use: `python batch_audio_snippets.py --csv snippets.csv --cookies cookies.txt`

asa --csv examples/snippets.csv

```### Installation4. Use incognito/private mode approach (won't work for age-restricted)



## CSV Format



Create a CSV file with the following columns:```bash**Why this happens**: Browsers lock their cookie databases while running. The script can't read them when the browser is open.g a single CSV file.



| Column  | Required | Description |# Clone the repository

|---------|----------|-------------|

| `url`   | ✅ | YouTube URL (any format) |git clone https://github.com/L3GJ0N/audio_snippet_automation.git### Why use this?

| `start` | ✅ | Start time: `SS(.ms)` or `HH:MM:SS(.ms)` |

| `end`   | ✅ | End time (same format as start) |cd audio_snippet_automation- Batch workflow (no copying timestamps manually one-by-one)

| `output`| ❌ | Custom filename (without extension) |

| `format`| ❌ | Override format (`m4a`, `mp3`, `wav`) |- Supports multiple output formats (m4a, mp3, wav)



### Example CSV# Install with uv (recommended)- Optional frame-accurate cutting (`--precise`)



```csvuv sync- Re-uses cached downloads if you re-run

url,start,end,output,format

https://www.youtube.com/watch?v=dQw4w9WgXcQ,00:00:05,00:00:12,rick-intro,m4a

https://youtu.be/dQw4w9WgXcQ,5,12,rick-chorus,mp3

```# Or install in development mode---



## Command Optionsuv pip install -e .## Quick Start (Windows 10/11)



```bash```

audio-snippet-automation --help

``````powershell



| Option | Description | Default |### Usage# 1. (Optional) Create and activate a virtual environment

|--------|-------------|---------|

| `--csv PATH` | CSV file with jobs | Required |python -m venv .venv

| `--format {m4a,mp3,wav}` | Default output format | `m4a` |

| `--precise` | Frame-accurate cuts (slower) | Fast copy |```bash./.venv/Scripts/Activate.ps1

| `--outdir DIR` | Output directory | `snippets` |

| `--tempdir DIR` | Cache directory | `downloads` |# Using uv

| `--cookies-from-browser BROWSER` | Browser cookies for age-restricted videos | None |

| `--cookies PATH` | Cookie file for age-restricted videos | None |uv run audio-snippet-automation --csv examples/snippets.csv# 2. Install required tools



### Examplespip install --upgrade yt-dlp



```bash# Or if installed globally

# Basic usage

uv run asa --csv my-clips.csvaudio-snippet-automation --csv examples/snippets.csv# 3. Install ffmpeg (choose ONE method)



# Custom output format and directories# a) Scoop (recommended):

uv run asa --csv clips.csv --format mp3 --outdir my-snippets

# Short alias#   Install Scoop if you don't have it:  Set-ExecutionPolicy RemoteSigned -Scope CurrentUser; iwr get.scoop.sh -useb | iex

# Precise cuts (re-encode for accuracy)

uv run asa --csv clips.csv --preciseasa --csv examples/snippets.csv#   Then:



# Age-restricted videos (browser cookies)```scoop install ffmpeg

uv run asa --csv clips.csv --cookies-from-browser chrome

# b) Chocolatey:

# Age-restricted videos (cookie file)

uv run asa --csv clips.csv --cookies cookies.txt## CSV Format#   choco install ffmpeg

```

# c) Manual: Download static build from https://www.gyan.dev/ffmpeg/ and add its /bin folder to PATH.

## How It Works

Create a CSV file with the following columns:

1. Reads each CSV row

2. Fetches the video ID (`yt-dlp --get-id`)# 4. Verify tools

3. Downloads best audio (cached in `downloads/`)

4. Cuts with `ffmpeg` (fast stream copy or precise re-encode)| Column  | Required | Description |yt-dlp --version

5. Converts / renames to desired format

|---------|----------|-------------|ffmpeg -version

Re-running with the same CSV is fast because existing downloads are reused.

| `url`   | ✅ | YouTube URL (any format) |

## Development

| `start` | ✅ | Start time: `SS(.ms)` or `HH:MM:SS(.ms)` |# 5. Run using the provided CSV

### Setup Development Environment

| `end`   | ✅ | End time (same format as start) |python batch_audio_snippets.py --csv snippets.csv --format m4a --outdir snippets --tempdir downloads

```bash

# Clone and setup| `output`| ❌ | Custom filename (without extension) |```

git clone https://github.com/L3GJ0N/audio_snippet_automation.git

cd audio_snippet_automation| `format`| ❌ | Override format (`m4a`, `mp3`, `wav`) |



# Install with dev dependenciesAfter running, trimmed files appear in `snippets/`. Source downloads (cached) are stored in `downloads/`.

uv sync --extra dev

### Example CSV

# Install pre-commit hooks

uv run pre-commit install---

```

```csv## CSV Format

### Running Tests

url,start,end,output,formatFile must have a header row. Columns:

```bash

# Run all testshttps://www.youtube.com/watch?v=dQw4w9WgXcQ,00:00:05,00:00:12,rick-intro,m4a

uv run pytest

https://youtu.be/dQw4w9WgXcQ,5,12,rick-chorus,mp3| Column  | Required | Description |

# Run with coverage

uv run pytest --cov```|---------|----------|-------------|



# Run specific test| url     | yes      | Full YouTube link (any normal watch or youtu.be URL) |

uv run pytest tests/test_core.py::test_time_str

```## Command Options| start   | yes      | Start time: `SS(.ms)` or `HH:MM:SS(.ms)` |



### Code Quality| end     | yes      | End time (same formats). Must be > start |



```bash```bash| output  | no       | Base filename (without extension). If blank, video ID is used |

# Format code

uv run black .audio-snippet-automation --help| format  | no       | Override format for that row (`m4a`, `mp3`, `wav`) |



# Lint code```

uv run ruff check .

Example (`snippets.csv`) currently in this repo:

# Type checking (if mypy is added)

uv run mypy src/| Option | Description | Default |```

```

|--------|-------------|---------|url,start,end,output,format

## Troubleshooting

| `--csv PATH` | CSV file with jobs | Required |https://www.youtube.com/watch?v=42N62Z5E7-s,00:00:01,00:00:03,avengers_assemble,m4a

| Problem | Solution |

|---------|----------|| `--format {m4a,mp3,wav}` | Default output format | `m4a` |https://www.youtube.com/watch?v=42N62Z5E7-s,00:00:03,00:00:05,thanos-like_to_lose,m4a

| `yt-dlp not found` | Install with `uv add yt-dlp` or system package manager |

| `ffmpeg not found` | Install ffmpeg and add to PATH || `--precise` | Frame-accurate cuts (slower) | Fast copy |```

| Cookie database error | Close browser completely, try different browser, or use cookie file |

| Permission errors | Check file permissions, run with appropriate user rights || `--outdir DIR` | Output directory | `snippets` |



### Age-Restricted Videos| `--tempdir DIR` | Cache directory | `downloads` |> Tip: You can copy a watch URL and tweak timestamps by scrubbing in the YouTube player and using the "Copy debug info" time or just manual entry.



When encountering "Sign in to confirm your age" errors:| `--cookies-from-browser BROWSER` | Browser cookies for age-restricted videos | None |



1. **Close browser completely** and retry with `--cookies-from-browser chrome`| `--cookies PATH` | Cookie file for age-restricted videos | None |---

2. **Try different browser**: `--cookies-from-browser firefox`

3. **Export cookies manually**:## Command Reference

   - Install browser extension like "Get cookies.txt LOCALLY"

   - Export YouTube cookies to `cookies.txt`### Examples

   - Use `--cookies cookies.txt`

| Option | Purpose |

## Project Structure

```bash|--------|---------|

```

audio_snippet_automation/# Basic usage| `--csv PATH` | (Required) Path to CSV file |

├── src/

│   └── audio_snippet_automation/uv run asa --csv my-clips.csv| `--format m4a|mp3|wav` | Default output format when a row omits the `format` column |

│       ├── __init__.py

│       ├── cli.py           # Command-line interface| `--precise` | Re-encode for frame-accurate cuts (slower, quality maintained) |

│       └── core.py          # Core functionality

├── tests/# Custom output format and directories| `--outdir DIR` | Where final snippets are written (default `snippets`) |

│   ├── __init__.py

│   └── test_core.pyuv run asa --csv clips.csv --format mp3 --outdir my-snippets| `--tempdir DIR` | Where source downloads are cached (default `downloads`) |

├── examples/

│   └── snippets.csv         # Example CSV file| `--cookies-from-browser BROWSER` | Extract cookies from browser for age-restricted videos (chrome, firefox, safari, etc.) |

├── docs/                    # Documentation

├── pyproject.toml          # Project configuration# Precise cuts (re-encode for accuracy)

├── README.md

└── .gitignoreuv run asa --csv clips.csv --precise### Example (matches repo data)

```

```powershell

## License

# Age-restricted videos (browser cookies)python batch_audio_snippets.py --csv .\snippets.csv --format m4a --outdir .\snippets --tempdir .\downloads

This project is licensed under the MIT License. See the LICENSE file for details.

uv run asa --csv clips.csv --cookies-from-browser chrome```

## Contributing



1. Fork the repository

2. Create a feature branch# Age-restricted videos (cookie file)### Producing MP3 instead

3. Make your changes

4. Add tests if applicableuv run asa --csv clips.csv --cookies cookies.txt```powershell

5. Run the test suite

6. Submit a pull request```python batch_audio_snippets.py --csv .\snippets.csv --format mp3



## Acknowledgments```



- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube downloader## Development

- [FFmpeg](https://ffmpeg.org/) - Audio/video processing

- [uv](https://github.com/astral-sh/uv) - Modern Python package manager### Frame-accurate cuts (use if edges are off)

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
