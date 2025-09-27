"""Core functionality for audio snippet extraction."""

import csv
import os
import subprocess
from pathlib import Path
from shutil import which


class AudioSnippetError(Exception):
    """Base exception for audio snippet operations."""

    pass


def check_dependencies() -> None:
    """Check if required tools are available."""
    if not which("yt-dlp"):
        raise AudioSnippetError(
            "yt-dlp not found in PATH. Install it with: uv add yt-dlp"
        )
    if not which("ffmpeg"):
        raise AudioSnippetError(
            "ffmpeg not found in PATH. Install it and ensure it's on PATH."
        )


def _log_cmd(args: list[str]) -> None:
    """Pretty-print command for logging."""

    def _quote_arg(arg: str) -> str:
        # Simple quoting for display only
        if os.name == "nt":
            if any(c.isspace() or c in "()[]{}&|^=;!,`" for c in arg):
                return f'"{arg}"'
            return arg
        else:
            import shlex

            return shlex.quote(arg)

    print("[CMD] " + " ".join(_quote_arg(str(a)) for a in args))


def run_command(args: list[str], cwd: Path | None = None) -> None:
    """Run a command and exit on failure."""
    _log_cmd(args)
    proc = subprocess.run(args, cwd=cwd)
    if proc.returncode != 0:
        raise AudioSnippetError(f"Command failed with exit code {proc.returncode}")


def run_command_output(args: list[str]) -> str:
    """Run a command and return stdout, exit on failure."""
    _log_cmd(args)
    proc = subprocess.run(args, capture_output=True, text=True)
    if proc.returncode != 0:
        raise AudioSnippetError(
            f"Command failed with exit code {proc.returncode}: {proc.stderr.strip()}"
        )
    return proc.stdout.strip()


def run_with_cookie_fallback(
    args_list: list[str],
    cookie_browser: str | None,
    cookie_file: str | None,
    url: str,
) -> str:
    """Run yt-dlp command with cookie fallback on failure."""
    # Try cookie file first
    if cookie_file:
        try:
            return run_command_output(args_list + ["--cookies", cookie_file, url])
        except AudioSnippetError:
            print(
                "[ERROR] Failed with cookie file. Check that the file exists and is valid."
            )
            raise

    # No cookies at all
    if not cookie_browser:
        return run_command_output(args_list + [url])

    # Try with cookies from browser
    try:
        cookie_args = args_list + ["--cookies-from-browser", cookie_browser, url]
        return run_command_output(cookie_args)
    except AudioSnippetError:
        # Cookie extraction failed, suggest solutions and try without cookies
        print(f"[WARN] Cookie extraction from {cookie_browser} failed.")
        print("[WARN] This usually happens when the browser is running.")
        print(
            "[WARN] Try: 1) Close all browser windows, 2) Use --cookies file instead, or 3) Try without cookies."
        )
        print("[WARN] Attempting without cookies...")

        try:
            return run_command_output(args_list + [url])
        except AudioSnippetError:
            print(
                "[ERROR] Failed both with and without cookies. Video may be age-restricted and require authentication."
            )
            print("[HELP] Solutions:")
            print(f"[HELP] 1. Close ALL {cookie_browser} windows and try again")
            print(
                "[HELP] 2. Export cookies manually: https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp"
            )
            print(
                "[HELP] 3. Use a different browser (try --cookies-from-browser firefox)"
            )
            raise


def time_str(t: str) -> str:
    """Pass-through time string validation."""
    return str(t).strip()


def validate_csv_format(reader: csv.DictReader) -> None:
    """Validate CSV has required columns."""
    required = {"url", "start", "end"}
    if not required.issubset(set(reader.fieldnames or [])):
        raise AudioSnippetError(
            f"CSV must include columns: {', '.join(sorted(required))} (plus optional 'output'). All outputs will be in WAV format."
        )


def get_video_id(
    url: str, cookie_browser: str | None = None, cookie_file: str | None = None
) -> str:
    """Get YouTube video ID from URL."""
    get_id_args = ["yt-dlp", "--no-playlist", "--get-id"]
    return run_with_cookie_fallback(get_id_args, cookie_browser, cookie_file, url)


def download_audio(
    url: str,
    video_id: str,
    temp_dir: Path,
    cookie_browser: str | None = None,
    cookie_file: str | None = None,
) -> Path:
    """Download audio from YouTube URL."""
    temp_audio = temp_dir / f"{video_id}.m4a"

    if temp_audio.exists():
        print(f"[INFO] Using cached: {temp_audio}")
        return temp_audio

    dl_args = [
        "yt-dlp",
        "-x",
        "--audio-format",
        "m4a",
        "-o",
        str(temp_dir / "%(id)s.%(ext)s"),
        "--no-playlist",
    ]

    # Handle cookies for download
    try:
        if cookie_file:
            run_command(dl_args + ["--cookies", cookie_file, url])
        elif cookie_browser:
            run_command(dl_args + ["--cookies-from-browser", cookie_browser, url])
        else:
            run_command(dl_args + [url])
    except AudioSnippetError:
        if cookie_browser:
            print("[WARN] Download with cookies failed, trying without cookies...")
            run_command(dl_args + [url])
        else:
            raise

    return temp_audio


def cut_audio(
    input_file: Path, start: str, end: str, output_file: Path, precise: bool = False
) -> Path:
    """Cut audio segment using ffmpeg."""
    temp_cut = output_file.with_suffix(".cut.m4a")

    if precise:
        # Re-encode for frame-accurate cuts
        ff_args = [
            "ffmpeg",
            "-y",
            "-ss",
            start,
            "-to",
            end,
            "-i",
            str(input_file),
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            str(temp_cut),
        ]
    else:
        # Fast stream copy
        ff_args = [
            "ffmpeg",
            "-y",
            "-ss",
            start,
            "-to",
            end,
            "-i",
            str(input_file),
            "-c",
            "copy",
            str(temp_cut),
        ]

    run_command(ff_args)
    return temp_cut


def convert_format(input_file: Path, output_file: Path, format_type: str) -> None:
    """Convert audio to specified format."""
    if format_type == "m4a":
        # Already m4a; just rename
        if output_file.exists():
            output_file.unlink()
        input_file.rename(output_file)
    elif format_type == "mp3":
        run_command(
            ["ffmpeg", "-y", "-i", str(input_file), "-q:a", "2", str(output_file)]
        )
        input_file.unlink()
    elif format_type == "wav":
        run_command(["ffmpeg", "-y", "-i", str(input_file), str(output_file)])
        input_file.unlink()
    else:
        raise AudioSnippetError(f"Unsupported format: {format_type}")
