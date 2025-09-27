# Audio Snippet Automation

Create multiple precisely trimmed audio snippets from YouTube URLs and automatically generate beautiful soundboards with a simple CSV file.

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## What Does This Do?

This tool provides a **complete soundboard workflow** - from YouTube videos to interactive web soundboards. Instead of manually downloading, cutting, and organizing audio files, you can:

1. **Create a CSV file** with YouTube URLs, start times, end times, and meaningful names
2. **Run one command** to download and cut all snippets automatically
3. **Auto-generate soundboards** with aesthetically optimized button layouts
4. **Launch interactive web interface** to play your sounds instantly

Perfect for creating sound effects, voice clips, music samples, DJ soundboards, or any interactive audio collection from YouTube videos.

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
- `output`: Filename for the audio snippet (optional)

All audio snippets are saved in **WAV format** for optimal soundboard compatibility.

**Example CSV:**
```csv
url,start,end,output
https://www.youtube.com/watch?v=J_vOzkxKfzk,00:00:14,00:00:17,thanos-like_to_lose
https://www.youtube.com/watch?v=PWSx0bBiNIs,00:00:04.230,00:00:07,you_cant_handle_truth
```

## Installation

### Prerequisites
You need these installed on your system:

1. **Python 3.12 or newer** - [Download here](https://www.python.org/downloads/)
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

**Note:** All audio files are automatically saved in **WAV format** for soundboard compatibility.

### Example CSV File

```csv
url,start,end,output
https://www.youtube.com/watch?v=J_vOzkxKfzk,00:00:14,00:00:17,thanos-like_to_lose
https://www.youtube.com/watch?v=PWSx0bBiNIs,00:00:04.230,00:00:07,you_cant_handle_truth
https://www.youtube.com/watch?v=31Voz1H40zI,00:01:22.110,00:01:23.800,i_am_the_danger
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

## 🎚️ MemeDeck Live

Once you've created your audio snippets, use the included **MemeDeck Live** deck to play them instantly with a customizable button grid!

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

### Launchpad-Inspired Interface

The browser soundboard now ships with a **Launchpad-style deck** complete with neon pads, a brushed-metal frame, and glowing play feedback. Each pad receives a color from a curated palette, and active pads pulse with an LED halo so you can see what is playing at a glance—perfect for live DJ work or streaming overlays.

#### Customizing the look

- 🎨 **Pad colors** – Update the `accentPalette` array in `src/audio_snippet_automation/static/js/soundboard.js` to change or expand the set of pad hues.
- 🧱 **Board styling** – Tweak the CSS variables at the top of `src/audio_snippet_automation/templates/soundboard.html` to adjust gradients, shadows, or typography.
- 🪪 **Labels** – Button labels are rendered directly on each pad; edit your soundboard JSON labels or tweak the `.pad-meta` rules to adjust typography or styling.
- 🚨 **Status banner** – The floating status pill mirrors the pad colors; adjust the `.status-indicator` rules in the template if you want a different placement or tone.

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

## 🚀 Automated Soundboard Generation

**NEW!** Skip the manual JSON configuration and automatically generate beautiful soundboards from your audio snippets!

### Quick Start

```bash
# Generate soundboard from your snippets folder
asa-generate-soundboard snippets/

# Preview the layout before generating
asa-generate-soundboard snippets/ --preview

# Generate with custom output file
asa-generate-soundboard snippets/ --output my_soundboard.json
```

### Complete Workflow Example

Here's the complete workflow from CSV creation to soundboard launch:

#### 1. Create Your Snippet List (snippets.csv)
```csv
url,start,end,output,format
https://www.youtube.com/watch?v=J_vOzkxKfzk,00:00:14,00:00:17,thanos-like_to_lose,m4a
https://www.youtube.com/watch?v=PWSx0bBiNIs,00:00:04.230,00:00:07,you_cant_handle_truth,m4a
https://www.youtube.com/watch?v=31Voz1H40zI,00:01:22.110,00:01:23.800,i_am_the_danger,m4a
https://www.youtube.com/watch?v=Wu67wq8ypwQ,00:00:03.500,00:00:08.200,simply_the_best,m4a
```

💡 **Pro Tip**: Use meaningful names in the `output` column - these become your button labels!

#### 2. Generate Audio Snippets
```bash
# Download and cut all your snippets
asa --csv snippets.csv --output-dir ./my_sounds
```

#### 3. Generate Soundboard Configuration
```bash
# Auto-generate optimal grid layout
asa-generate-soundboard ./my_sounds --output soundboard.json

# Preview the layout first
asa-generate-soundboard ./my_sounds --preview
```

#### 4. Launch Your Soundboard
```bash
# Start the web interface
asa-soundboard --config soundboard.json
```

### Intelligent Grid Algorithm

The generator uses an **aesthetic-optimized algorithm** that creates visually appealing layouts:

- ✅ **rows ≥ cols** - Slightly taller than wide (more natural)
- ✅ **rows - cols ≤ 2** - Prevents overly tall/narrow grids
- ✅ **Minimal empty slots** - Reduces wasted space
- ✅ **Optimal visual balance** - Creates near-square layouts when possible

**Examples:**
- 28 files → **6×5 grid** (30 slots, 2 empty) - Much better than 7×4!
- 12 files → **4×3 grid** (12 slots, 0 empty) - Perfect fit
- 20 files → **5×4 grid** (20 slots, 0 empty) - Balanced layout

### Generator Features

- 🎯 **Smart Layout** - Automatically calculates optimal grid dimensions
- 📁 **Auto-Discovery** - Finds all supported audio files in directory
- 🏷️ **Clean Labels** - Converts filenames to readable button labels
- 👀 **Preview Mode** - See layout before generating configuration
- ⚡ **Format Support** - Works with M4A, MP3, WAV, OGG files
- 🎨 **Aesthetic Focus** - Creates visually balanced button grids

### Usage Options

```bash
# Basic generation
asa-generate-soundboard <directory>

# Preview layout without creating file
asa-generate-soundboard <directory> --preview

# Custom output filename
asa-generate-soundboard <directory> --output my_board.json

# Show detailed information
asa-generate-soundboard <directory> --verbose
```

### Why Use Meaningful CSV Names?

When creating your snippets CSV, use descriptive `output` names because they become your soundboard button labels:

❌ **Bad:**
```csv
url,start,end,output,format
https://youtube.com/...,00:00:14,00:00:17,clip1,m4a
https://youtube.com/...,00:00:04,00:00:07,audio2,m4a
```

✅ **Good:**
```csv
url,start,end,output,format
https://youtube.com/...,00:00:14,00:00:17,thanos_inevitable,m4a
https://youtube.com/...,00:00:04,00:00:07,you_cant_handle_truth,m4a
```

The generator automatically converts filenames like `you_cant_handle_truth.m4a` into clean labels like **"You Cant Handle Truth"** for your soundboard buttons!

## 📋 Command Reference

### Snippet Generation Commands

```bash
# Basic snippet generation from CSV
asa --csv snippets.csv

# With output directory and format
asa --csv snippets.csv --output-dir ./sounds --format mp3

# With cookies for age-restricted videos
asa --csv snippets.csv --cookies-from-browser chrome

# Precise cutting (slower but more accurate)
asa --csv snippets.csv --precise
```

### Soundboard Generator Commands

```bash
# Generate optimal soundboard layout
asa-generate-soundboard <directory>

# Preview layout without creating file
asa-generate-soundboard <directory> --preview

# Custom output filename
asa-generate-soundboard <directory> --output board.json

# Show detailed information
asa-generate-soundboard <directory> --verbose
```

### Soundboard Player Commands

```bash
# Launch soundboard from config
asa-soundboard --config soundboard.json

# Create example configuration
asa-soundboard --create-example my_board.json

# Custom host and port
asa-soundboard --config board.json --host 0.0.0.0 --port 8080

# Don't auto-open browser
asa-soundboard --config board.json --no-browser

# Debug mode
asa-soundboard --config board.json --debug --verbose
```

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
│       ├── snippet_cli.py      # Audio snippet automation CLI
│       ├── soundboard_cli.py   # MemeDeck Live CLI
│       ├── soundboard.py       # Soundboard backend
│       ├── core.py             # Core audio processing logic
│       └── templates/          # Web interface templates
├── tests/
│   ├── __init__.py
│   └── test_core.py
├── examples/
│   ├── snippets.csv            # Example CSV file
│   └── soundboard.json         # Example soundboard config
├── docs/                       # Documentation
├── pyproject.toml             # Project configuration
├── README.MD
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
