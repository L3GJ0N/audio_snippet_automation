"""Command line interface for audio snippet automation."""

import argparse
import csv
import json
import sys
from pathlib import Path

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


def create_parser() -> argparse.ArgumentParser:
    """Create the command line argument parser."""
    parser = argparse.ArgumentParser(
        prog="audio-snippet-automation",
        description="Create multiple precisely trimmed audio snippets from YouTube URLs using a single CSV file.",
    )
    parser.add_argument(
        "--csv", required=True, type=Path, help="Path to CSV file with jobs"
    )
    parser.add_argument(
        "--format",
        default="m4a",
        choices=["m4a", "mp3", "wav"],
        help="Default output format",
    )
    parser.add_argument(
        "--precise",
        action="store_true",
        help="Re-encode for precise cuts (useful if copy cuts are off)",
    )
    parser.add_argument(
        "--outdir", default="snippets", type=Path, help="Output directory"
    )
    parser.add_argument(
        "--tempdir", default="downloads", type=Path, help="Temp download dir"
    )
    parser.add_argument(
        "--cookies-from-browser",
        help="Browser to extract cookies from (chrome, firefox, safari, etc.) for age-restricted videos",
    )
    parser.add_argument(
        "--cookies",
        type=Path,
        help="Path to cookies.txt file for age-restricted videos",
    )
    parser.add_argument(
        "--soundboard-ready",
        action="store_true",
        help="Convert all outputs to WAV format and generate soundboard config (overrides --format)",
    )
    parser.add_argument(
        "--generate-soundboard-config",
        type=Path,
        help="Generate a soundboard JSON configuration file for the created snippets",
    )
    parser.add_argument(
        "--soundboard-layout",
        nargs=2,
        type=int,
        metavar=("ROWS", "COLS"),
        default=[4, 6],
        help="Grid layout for soundboard config (rows cols, default: 4 6)",
    )
    return parser


def generate_soundboard_config(
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
    row: dict, row_num: int, args: argparse.Namespace, snippet_files: list[dict] = None
) -> None:
    """Process a single CSV row."""
    url = (row.get("url") or "").strip()
    start = time_str(row.get("start") or "")
    end = time_str(row.get("end") or "")
    out_base = (row.get("output") or "").strip()
    fmt = (row.get("format") or "").strip().lower() or args.format

    # Override format if soundboard-ready flag is set
    if args.soundboard_ready:
        fmt = "wav"
        print(f"[INFO] Soundboard mode: Using WAV format for {out_base or 'snippet'}")

    if not url or not start or not end:
        print(f"[WARN] Row {row_num} missing url/start/end. Skipping.")
        return

    # Get video ID
    vid = get_video_id(url, args.cookies_from_browser, args.cookies)

    # Download audio
    temp_audio = download_audio(
        url, vid, args.tempdir, args.cookies_from_browser, args.cookies
    )

    # Determine output name
    if not out_base:
        out_base = vid

    final_path = args.outdir / f"{out_base}.{fmt}"
    print(f"[INFO] Processing: {url} -> {final_path}")

    # Cut audio
    cut_tmp = cut_audio(temp_audio, start, end, final_path, args.precise)

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


def main() -> None:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()

    try:
        # Check dependencies
        check_dependencies()

        # Create directories
        args.outdir.mkdir(exist_ok=True)
        args.tempdir.mkdir(exist_ok=True)

        # Initialize snippet tracking for soundboard config
        snippet_files = []
        should_generate_config = (
            args.soundboard_ready or args.generate_soundboard_config
        )

        # Process CSV
        with open(args.csv, newline="", encoding="utf-8") as f:
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
            config_path = args.generate_soundboard_config or (
                args.outdir / "soundboard.json"
            )
            layout = tuple(args.soundboard_layout)
            generate_soundboard_config(snippet_files, layout, config_path)

            if args.soundboard_ready:
                print(
                    f"[INFO] Soundboard ready! Launch with: asa-soundboard --config {config_path}"
                )

    except AudioSnippetError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"[ERROR] CSV file not found: {args.csv}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[INFO] Interrupted by user")
        sys.exit(130)


if __name__ == "__main__":
    main()
