#!/usr/bin/env python3
"""
Soundboard JSON Generator

Automatically generates a soundboard configuration JSON file from a folder of audio files.
Creates an optimal grid layout and maps audio files to buttons.
"""

import json
import math
from pathlib import Path

import click


def calculate_optimal_grid(num_files: int) -> tuple[int, int]:
    """
    Calculate the optimal grid dimensions for the given number of files.

    Prioritizes more rows over columns (taller rather than wider layout).
    If the number doesn't fit perfectly, uses the next larger grid.

    Args:
        num_files: Number of audio files to arrange

    Returns:
        Tuple of (rows, cols) for the grid layout

    Examples:
        6 files -> (3, 2)  # 3 rows, 2 cols
        9 files -> (3, 3)  # 3 rows, 3 cols
        28 files -> (7, 4) # 7 rows, 4 cols (28 total slots)
    """
    if num_files == 0:
        return (1, 1)
    if num_files == 1:
        return (1, 1)

    # Find factors of num_files and factors that create minimal empty slots
    best_rows, best_cols = num_files, 1  # Fallback: single column
    min_empty_slots = float("inf")

    # Try different column counts from 1 to sqrt(num_files) + some buffer
    max_cols = min(num_files, int(math.sqrt(num_files)) + 3)

    for cols in range(1, max_cols + 1):
        rows = math.ceil(num_files / cols)
        total_slots = rows * cols
        empty_slots = total_slots - num_files

        # Prefer arrangements with:
        # 1. Fewer empty slots
        # 2. More rows than columns (rows >= cols)
        # 3. More reasonable aspect ratios (not too tall/wide)
        if (
            empty_slots < min_empty_slots and rows >= cols and rows / cols <= 3
        ):  # Don't make it more than 3x taller than wide
            best_rows, best_cols = rows, cols
            min_empty_slots = empty_slots

    return (best_rows, best_cols)


def find_audio_files(
    folder_path: Path, extensions: list[str] | None = None
) -> list[Path]:
    """
    Find all audio files in the given folder.

    Args:
        folder_path: Path to the folder containing audio files
        extensions: List of file extensions to include (default: common audio formats)

    Returns:
        List of Path objects for found audio files, sorted by name
    """
    if extensions is None:
        extensions = [".wav", ".mp3", ".m4a", ".ogg", ".flac"]

    audio_files = set()  # Use set to avoid duplicates

    for ext in extensions:
        audio_files.update(folder_path.glob(f"*{ext}"))
        audio_files.update(folder_path.glob(f"*{ext.upper()}"))

    # Sort by filename for consistent ordering
    return sorted(audio_files, key=lambda p: p.name.lower())


def create_button_label(file_path: Path) -> str:
    """
    Create a human-readable label from the filename.

    Removes extension and replaces underscores/hyphens with spaces.
    Capitalizes each word for better readability.

    Args:
        file_path: Path to the audio file

    Returns:
        Formatted label string
    """
    # Remove extension
    name = file_path.stem

    # Replace common separators with spaces
    name = name.replace("_", " ").replace("-", " ")

    # Capitalize each word
    return " ".join(word.capitalize() for word in name.split())


def generate_soundboard_config(
    audio_folder: Path, use_relative_paths: bool = True
) -> dict:
    """
    Generate a complete soundboard configuration from a folder of audio files.

    Args:
        audio_folder: Path to folder containing audio files
        use_relative_paths: If True, use relative paths; if False, use absolute paths

    Returns:
        Dictionary containing the soundboard configuration
    """
    # Find all audio files
    audio_files = find_audio_files(audio_folder)

    if not audio_files:
        raise ValueError(f"No audio files found in {audio_folder}")

    # Calculate optimal grid layout
    rows, cols = calculate_optimal_grid(len(audio_files))

    # Create button configurations
    buttons = []
    file_index = 0

    for row in range(1, rows + 1):
        for col in range(1, cols + 1):
            if file_index >= len(audio_files):
                # No more files, leave remaining slots empty
                break

            file_path = audio_files[file_index]

            # Determine path format
            if use_relative_paths:
                # Use relative path from current directory
                try:
                    display_path = file_path.relative_to(Path.cwd())
                except ValueError:
                    # If file is not relative to cwd, use absolute path
                    display_path = file_path
            else:
                display_path = file_path.absolute()

            button_config = {
                "file": str(display_path).replace(
                    "\\", "/"
                ),  # Use forward slashes for cross-platform
                "row": row,
                "col": col,
                "label": create_button_label(file_path),
            }

            buttons.append(button_config)
            file_index += 1

    # Create the complete configuration
    config = {"layout": {"rows": rows, "cols": cols}, "buttons": buttons}

    return config


@click.command()
@click.argument(
    "audio_folder", type=click.Path(exists=True, file_okay=False, path_type=Path)
)
@click.option(
    "--output",
    "-o",
    type=click.Path(path_type=Path),
    help="Output JSON file path (default: soundboard.json in audio folder)",
)
@click.option(
    "--absolute-paths",
    "-a",
    is_flag=True,
    help="Use absolute file paths instead of relative paths",
)
@click.option(
    "--extensions",
    "-e",
    multiple=True,
    help="Additional file extensions to include (e.g., -e .aac -e .wma)",
)
@click.option(
    "--preview",
    "-p",
    is_flag=True,
    help="Preview the configuration without writing to file",
)
def main(
    audio_folder: Path,
    output: Path,
    absolute_paths: bool,
    extensions: tuple,
    preview: bool,
):
    """
    Generate a soundboard JSON configuration from a folder of audio files.

    AUDIO_FOLDER: Path to the folder containing audio files

    Examples:

        # Generate soundboard.json from WAV files in ./sounds/
        python generate_soundboard.py ./sounds/

        # Use absolute paths and custom output location
        python generate_soundboard.py ./sounds/ -o my_soundboard.json --absolute-paths

        # Include additional file types and preview
        python generate_soundboard.py ./sounds/ -e .aac -e .wma --preview
    """
    try:
        # Prepare extensions list
        default_extensions = [".wav", ".mp3", ".m4a", ".ogg", ".flac"]
        if extensions:
            all_extensions = default_extensions + list(extensions)
        else:
            all_extensions = default_extensions

        # Find audio files
        audio_files = find_audio_files(audio_folder, all_extensions)

        if not audio_files:
            click.echo(f"❌ No audio files found in {audio_folder}")
            click.echo(f"   Supported extensions: {', '.join(all_extensions)}")
            return

        # Generate configuration
        config = generate_soundboard_config(
            audio_folder, use_relative_paths=not absolute_paths
        )

        # Show summary
        rows, cols = config["layout"]["rows"], config["layout"]["cols"]
        click.echo(f"📁 Found {len(audio_files)} audio files in {audio_folder}")
        click.echo(
            f"📐 Generated {rows}×{cols} grid layout ({rows * cols} total slots)"
        )
        click.echo(f"🎵 Buttons created: {len(config['buttons'])}")

        if preview:
            # Show preview
            click.echo("\n🔍 Configuration Preview:")
            click.echo("-" * 50)
            click.echo(json.dumps(config, indent=2))
        else:
            # Determine output path
            if output is None:
                output = audio_folder / "soundboard.json"

            # Write configuration to file
            with open(output, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2)

            click.echo(f"✅ Soundboard configuration saved to: {output}")
            click.echo("\nTo use this configuration:")
            click.echo(f"   asa-soundboard {output}")

        # Show file list
        click.echo("\n📋 Audio files included:")
        for i, file_path in enumerate(audio_files[:10]):  # Show first 10
            click.echo(f"   {i + 1:2d}. {file_path.name}")
        if len(audio_files) > 10:
            click.echo(f"   ... and {len(audio_files) - 10} more files")

    except Exception as e:
        click.echo(f"❌ Error: {e}", err=True)
        return 1


if __name__ == "__main__":
    main()
