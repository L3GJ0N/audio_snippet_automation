"""Command line interface for audio snippet automation."""

import csv
import json
import sys
from pathlib import Path

import click

from .core import (
    AudioSnippetError,
    check_dependencies,
    convert_format,
    cut_audio,
    download_audio,
    get_video_id,
    time_str,
    validate_csv_format,
)


def generate_soundboard_config_file(
    snippet_files: list[dict], layout: tuple[int, int], config_path: Path
) -> None:
    """Generate a soundboard configuration file from created snippets."""
    rows, cols = layout
    max_buttons = rows * cols

    # Limit to grid size
    if len(snippet_files) > max_buttons:
        print(
            f"[WARN] Too many snippets ({len(snippet_files)}) for {rows}x{cols} grid. Using first {max_buttons}."
        )
        snippet_files = snippet_files[:max_buttons]

    # Create configuration
    config = {"layout": {"rows": rows, "cols": cols}, "buttons": []}

    # Auto-arrange buttons in grid
    for i, snippet in enumerate(snippet_files):
        row = (i // cols) + 1
        col = (i % cols) + 1

        button = {
            "file": str(snippet["path"].absolute()),
            "row": row,
            "col": col,
            "label": snippet["label"],
        }
        config["buttons"].append(button)

    # Write configuration
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

    print(f"[INFO] Generated soundboard config: {config_path}")
    print(f"[INFO] Layout: {rows}x{cols} with {len(snippet_files)} buttons")


def process_csv_row(
    row: dict, row_num: int, args: dict, snippet_files: list[dict] = None
) -> None:
    """Process a single CSV row."""
    url = (row.get("url") or "").strip()
    start = time_str(row.get("start") or "")
    end = time_str(row.get("end") or "")
    out_base = (row.get("output") or "").strip()
    fmt = (row.get("format") or "").strip().lower() or args["format"]

    # Override format if soundboard-ready flag is set
    if args["soundboard_ready"]:
        fmt = "wav"
        print(f"[INFO] Soundboard mode: Using WAV format for {out_base or 'snippet'}")

    if not url or not start or not end:
        print(f"[WARN] Row {row_num} missing url/start/end. Skipping.")
        return

    # Get video ID
    vid = get_video_id(url, args["cookies_from_browser"], args["cookies"])

    # Download audio
    temp_audio = download_audio(
        url, vid, args["tempdir"], args["cookies_from_browser"], args["cookies"]
    )

    # Determine output name
    if not out_base:
        out_base = vid

    final_path = args["outdir"] / f"{out_base}.{fmt}"
    print(f"[INFO] Processing: {url} -> {final_path}")

    # Cut audio
    cut_tmp = cut_audio(temp_audio, start, end, final_path, args["precise"])

    # Convert to final format
    convert_format(cut_tmp, final_path, fmt)

    print(f"[OK] Wrote {final_path}")

    # Track snippet for soundboard config generation
    if snippet_files is not None:
        # Create a nice label from the output name
        label = out_base.replace("_", " ").replace("-", " ").title()
        # Limit label length for UI
        if len(label) > 25:
            label = label[:22] + "..."

        snippet_files.append({"path": final_path, "label": label, "output": out_base})


@click.command()
@click.version_option(version="0.2.0", prog_name="asa")
@click.option(
    "--csv",
    "csv_file",
    required=True,
    type=click.Path(exists=True, path_type=Path),
    help="Path to CSV file with jobs",
)
@click.option(
    "--format",
    "output_format",
    default="m4a",
    type=click.Choice(["m4a", "mp3", "wav"]),
    help="Default output format",
)
@click.option(
    "--precise",
    is_flag=True,
    help="Re-encode for precise cuts (useful if copy cuts are off)",
)
@click.option(
    "--outdir",
    default="snippets",
    type=click.Path(path_type=Path),
    help="Output directory",
)
@click.option(
    "--tempdir",
    default="downloads",
    type=click.Path(path_type=Path),
    help="Temp download dir",
)
@click.option(
    "--cookies-from-browser",
    help="Browser to extract cookies from (chrome, firefox, safari, etc.) for age-restricted videos",
)
@click.option(
    "--cookies",
    type=click.Path(exists=True, path_type=Path),
    help="Path to cookies.txt file for age-restricted videos",
)
@click.option(
    "--soundboard-ready",
    is_flag=True,
    help="Convert all outputs to WAV format and generate soundboard config (overrides --format)",
)
@click.option(
    "--generate-soundboard-config",
    type=click.Path(path_type=Path),
    help="Generate a soundboard JSON configuration file for the created snippets",
)
@click.option(
    "--soundboard-layout",
    nargs=2,
    type=int,
    default=[4, 6],
    help="Grid layout for soundboard config (rows cols, default: 4 6)",
)
def main(
    csv_file: Path,
    output_format: str,
    precise: bool,
    outdir: Path,
    tempdir: Path,
    cookies_from_browser: str,
    cookies: Path,
    soundboard_ready: bool,
    generate_soundboard_config: Path,
    soundboard_layout: tuple[int, int],
) -> None:
    """Create multiple precisely trimmed audio snippets from YouTube URLs using a single CSV file."""
    try:
        # Check dependencies
        check_dependencies()

        # Create directories
        outdir.mkdir(exist_ok=True)
        tempdir.mkdir(exist_ok=True)

        # Convert parameters to dict for compatibility with existing functions
        args = {
            "csv": csv_file,
            "format": output_format,
            "precise": precise,
            "outdir": outdir,
            "tempdir": tempdir,
            "cookies_from_browser": cookies_from_browser,
            "cookies": cookies,
            "soundboard_ready": soundboard_ready,
            "generate_soundboard_config": generate_soundboard_config,
            "soundboard_layout": soundboard_layout,
        }

        # Initialize snippet tracking for soundboard config
        snippet_files = []
        should_generate_config = soundboard_ready or generate_soundboard_config

        # Process CSV
        with open(csv_file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            validate_csv_format(reader)

            for i, row in enumerate(reader, 1):
                try:
                    process_csv_row(
                        row, i, args, snippet_files if should_generate_config else None
                    )
                except AudioSnippetError as e:
                    print(f"[ERROR] Row {i}: {e}")
                    continue
                except KeyboardInterrupt:
                    print("\n[INFO] Interrupted by user")
                    sys.exit(130)

        print("[DONE] All jobs processed.")

        # Generate soundboard configuration if requested
        if should_generate_config and snippet_files:
            config_path = generate_soundboard_config or (outdir / "soundboard.json")
            layout = tuple(soundboard_layout)
            generate_soundboard_config_file(snippet_files, layout, config_path)

            if soundboard_ready:
                print(
                    f"[INFO] Soundboard ready! Launch with: asa-soundboard --config {config_path}"
                )

    except AudioSnippetError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"[ERROR] CSV file not found: {csv_file}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[INFO] Interrupted by user")
        sys.exit(130)


if __name__ == "__main__":
    main()
