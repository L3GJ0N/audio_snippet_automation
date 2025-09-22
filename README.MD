# Audio Snippet Automation

Create multiple precisely trimmed audio snippets from YouTube URLs using a simple CSV file.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## What Does This Do?

This tool automates the process of creating audio snippets from YouTube videos. Instead of manually downloading videos and cutting them one by one, you can:

1. **Create a CSV file** with YouTube URLs, start times, end times, and output names
2. **Run one command** to process all entries automatically
3. **Get perfectly trimmed audio files** ready to use

Perfect for creating sound effects, voice clips, music samples, or any audio content from YouTube videos.

## ⚠️ Legal Notice & Responsible Use

**This tool is for educational and personal use only.** Users are solely responsible for:

- ✅ **Complying with YouTube's Terms of Service** - Review YouTube's current ToS before use
- ✅ **Respecting copyright laws** - Ensure you have rights to use the content you download
- ✅ **Obtaining proper permissions** - Get authorization for copyrighted material when required
- ✅ **Following local laws** - Copyright laws vary by jurisdiction
- ✅ **Using only authorized content** - Content you own, have licensed, or is in the public domain

**Examples of appropriate use:**
- Your own uploaded videos
- Creative Commons or public domain content
- Educational content where fair use applies (varies by jurisdiction)
- Content you have explicit permission to use

**The developers provide this tool "as-is" and are not responsible for any misuse, copyright violations, or legal issues arising from its use.** By using this software, you acknowledge that you understand these responsibilities and agree to use it legally and ethically.

## How It Works

The tool reads a CSV file where each row defines:
- `url`: YouTube video URL
- `start`: When to start cutting (e.g., `00:01:23.500`)
- `end`: When to stop cutting (e.g., `00:01:30.000`)
- `output`: Filename for the audio snippet
- `format`: Audio format (m4a, mp3, wav)

**Example CSV:**
```csv
url,start,end,output,format
https://www.youtube.com/watch?v=J_vOzkxKfzk,00:00:14,00:00:17,thanos-like_to_lose,m4a
https://www.youtube.com/watch?v=PWSx0bBiNIs,00:00:04.230,00:00:07,you_cant_handle_truth,m4a
```

## Installation

### Prerequisites
You need these installed on your system:

1. **Python 3.9 or newer** - [Download here](https://www.python.org/downloads/)
2. **uv package manager** - [Installation guide](https://docs.astral.sh/uv/getting-started/installation/)
3. **ffmpeg** - [Download here](https://ffmpeg.org/download.html)

### Install the Tool

```bash
# Clone the repository
git clone https://github.com/L3GJ0N/audio_snippet_automation.git
cd audio_snippet_automation

# Install with uv (recommended)
uv sync

# Or install with pip
pip install -e .
```

### Verify Installation

```bash
# Check if the tool is installed
asa --help

# Or use the full command name
audio-snippet-automation --help

# Verify dependencies
yt-dlp --version
ffmpeg -version
```

## Usage

### Basic Usage

```bash
# Process a CSV file
asa --csv examples/snippets.csv

# Or use the full command name
audio-snippet-automation --csv examples/snippets.csv

# If using uv in development
uv run audio-snippet-automation --csv examples/snippets.csv
```

### CSV Format

Create a CSV file with these columns:

| Column   | Required | Description                              | Example                    |
|----------|----------|------------------------------------------|----------------------------|
| `url`    | ✅        | YouTube URL (any format)                | `https://youtu.be/abc123`  |
| `start`  | ✅        | Start time: `SS(.ms)` or `HH:MM:SS(.ms)` | `00:01:23.500`             |
| `end`    | ✅        | End time (same format as start)         | `00:01:30.000`             |
| `output` | ❌        | Custom filename (without extension)     | `my_audio_clip`            |
| `format` | ❌        | Override format (`m4a`, `mp3`, `wav`)    | `mp3`                      |

### Example CSV File

```csv
url,start,end,output,format
https://www.youtube.com/watch?v=J_vOzkxKfzk,00:00:14,00:00:17,thanos-like_to_lose,m4a
https://www.youtube.com/watch?v=PWSx0bBiNIs,00:00:04.230,00:00:07,you_cant_handle_truth,m4a
https://www.youtube.com/watch?v=31Voz1H40zI,00:01:22.110,00:01:23.800,i_am_the_danger,m4a
```

### Advanced Options

```bash
# Use cookies for age-restricted videos
asa --csv snippets.csv --cookies-from-browser chrome

# Or use Firefox cookies
asa --csv snippets.csv --cookies-from-browser firefox

# Use external cookie file
asa --csv snippets.csv --cookies cookies.txt

# Specify output directory
asa --csv snippets.csv --output-dir ./my_snippets

# Use different audio format (default: m4a)
asa --csv snippets.csv --format mp3

# Enable precise cutting (slower but more accurate)
asa --csv snippets.csv --precise
```

## Time Format Guide

You can specify times in multiple formats:

- **Seconds only**: `45` or `45.5`
- **Minutes and seconds**: `01:23` or `01:23.5`
- **Hours, minutes, seconds**: `00:01:23` or `00:01:23.500`

**Examples:**
- `15` = 15 seconds
- `01:30` = 1 minute 30 seconds
- `00:02:45.250` = 2 minutes 45.25 seconds

## Features

- 🎵 **Batch processing** - Process multiple videos at once
- 📊 **CSV-driven** - Simple spreadsheet interface
- 🎯 **Precise cutting** - Frame-accurate timestamps with `--precise`
- 🔄 **Smart caching** - Reuse downloads between runs
- 🌐 **Format support** - Output as M4A, MP3, or WAV
- 🔐 **Age-restricted videos** - Cookie support for restricted content
- 🐍 **Modern Python** - Built with modern tooling and best practices

## 🎚️ Virtual DJ Soundboard

Once you've created your audio snippets, use the included **Virtual DJ Soundboard** to play them instantly with a customizable button grid!

### Quick Start

```bash
# Create example soundboard configuration
asa-soundboard --create-example my_soundboard.json

# Edit the JSON file to point to your audio files
# Then launch the soundboard
asa-soundboard --config my_soundboard.json
```

### Soundboard Features

- 🎛️ **Customizable Grid** - Define any NxM button layout
- 🌐 **Web Interface** - Cross-platform browser-based UI
- 🎵 **Simultaneous Playbook** - Play multiple sounds at once
- ⚡ **Instant Response** - Low-latency audio playback
- 🎨 **Visual Feedback** - Button animations and status indicators
- ⌨️ **Keyboard Shortcuts** - Space/Escape to stop all sounds
- 🎚️ **Audio Formats** - Supports WAV, MP3, and OGG files

**Note**: M4A files need to be converted to supported formats. Use:
```bash
ffmpeg -i input.m4a output.wav
```

### Configuration Format

Create a JSON file with your button layout:

```json
{
  "layout": {
    "rows": 4,
    "cols": 6
  },
  "buttons": [
    {
      "file": "path/to/your/snippet.m4a",
      "row": 1,
      "col": 1,
      "label": "Button Label"
    }
  ]
}
```

### Soundboard Usage

```bash
# Basic usage
asa-soundboard --config soundboard.json

# Custom host/port
asa-soundboard --config sounds.json --host 0.0.0.0 --port 8080

# Don't auto-open browser
asa-soundboard --config sounds.json --no-browser

# Enable debug mode
asa-soundboard --config sounds.json --debug --verbose
```

The soundboard will open in your browser with a beautiful grid interface where you can click buttons to play your audio snippets instantly!

## Troubleshooting

### Common Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| `yt-dlp not found` | Not installed or not in PATH | Install with `pip install yt-dlp` |
| `ffmpeg not found` | Not installed or not in PATH | [Install ffmpeg](https://ffmpeg.org/download.html) |
| "Sign in to confirm your age" | Age-restricted video | Use `--cookies-from-browser chrome` |
| Empty output file | Invalid time range | Check start/end times are within video duration |
| "Could not copy cookie database" | Browser is running | Close ALL browser windows and try again |

### Cookie Issues (Age-restricted videos)

**Problem**: `Could not copy Chrome cookie database` or similar errors.

**Solutions** (try in order):
1. **Close ALL browser windows** completely and try again
2. Try a different browser: `--cookies-from-browser firefox`
3. Export cookies manually:
   - Install browser extension like "Get cookies.txt"
   - Export cookies for youtube.com to `cookies.txt`
   - Use: `asa --csv snippets.csv --cookies cookies.txt`

**Why this happens**: Browsers lock their cookie databases while running. The script can't read them when the browser is open.

### Getting Help

```bash
# Show all available options
asa --help

# Check version
asa --version
```

## Project Structure

```
audio_snippet_automation/
├── src/
│   └── audio_snippet_automation/
│       ├── __init__.py
│       ├── cli.py              # Command-line interface
│       └── core.py             # Core audio processing logic
├── tests/
│   ├── __init__.py
│   └── test_core.py
├── examples/
│   └── snippets.csv            # Example CSV file
├── docs/                       # Documentation
├── pyproject.toml             # Project configuration
├── README.md
└── .gitignore
```

## Development

### Setting Up Development Environment

```bash
# Clone and enter the repository
git clone https://github.com/L3GJ0N/audio_snippet_automation.git
cd audio_snippet_automation

# Install with development dependencies
uv sync --extra dev

# Install pre-commit hooks
uv run pre-commit install

# Run tests
uv run pytest

# Run with coverage
uv run pytest --cov=audio_snippet_automation
```

### Code Quality

This project uses modern Python tooling:

- **uv** - Fast Python package manager
- **black** - Code formatting
- **ruff** - Linting and import sorting
- **pre-commit** - Git hooks for code quality
- **pytest** - Testing framework

```bash
# Format code
uv run black .

# Lint code
uv run ruff check .

# Run all pre-commit hooks
uv run pre-commit run --all-files
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Run the test suite: `uv run pytest`
6. Ensure code quality: `uv run pre-commit run --all-files`
7. Submit a pull request

## Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube downloader
- [FFmpeg](https://ffmpeg.org/) - Audio/video processing
- [uv](https://github.com/astral-sh/uv) - Modern Python package manager
