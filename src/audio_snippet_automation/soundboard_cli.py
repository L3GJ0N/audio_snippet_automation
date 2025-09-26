#!/usr/bin/env python3
"""
Command-line interface for the Virtual DJ Soundboard.

This module provides a CLI to launch the web-based soundboard interface.
"""

import logging
import sys
import webbrowser
from pathlib import Path
from threading import Timer

import click

from .soundboard import AudioSnippetError, VirtualDJSoundboard, create_example_config


def setup_logging(verbose: bool = False) -> None:
    """Configure logging for the application."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def open_browser(url: str, delay: float = 1.5) -> None:
    """Open the browser to the soundboard URL after a delay."""

    def open_url():
        try:
            webbrowser.open(url)
            print(f"Opened browser to: {url}")
        except Exception as e:
            print(f"Could not open browser automatically: {e}")
            print(f"Please open your browser manually and go to: {url}")

    Timer(delay, open_url).start()


def validate_config_file(config_path: Path) -> None:
    """Validate that the configuration file exists and is readable."""
    if not config_path.exists():
        raise AudioSnippetError(f"Configuration file not found: {config_path}")

    if not config_path.is_file():
        raise AudioSnippetError(f"Configuration path is not a file: {config_path}")

    try:
        with open(config_path, encoding="utf-8"):
            pass
    except PermissionError:
        raise AudioSnippetError(
            f"Permission denied reading configuration file: {config_path}"
        ) from None
    except Exception as e:
        raise AudioSnippetError(
            f"Cannot read configuration file {config_path}: {e}"
        ) from e


@click.command()
@click.option(
    "--config",
    "-c",
    type=click.Path(exists=True, path_type=Path),
    help="Path to JSON configuration file",
)
@click.option(
    "--host",
    default="localhost",
    help="Host to bind the web server (default: localhost)",
)
@click.option(
    "--port",
    "-p",
    type=int,
    default=8080,
    help="Port for the web server (default: 8080)",
)
@click.option(
    "--no-browser",
    is_flag=True,
    help="Do not automatically open browser",
)
@click.option(
    "--debug",
    is_flag=True,
    help="Enable Flask debug mode",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Enable verbose logging",
)
@click.option(
    "--create-example",
    type=click.Path(path_type=Path),
    help="Create an example configuration file and exit",
)
@click.version_option(version="0.2.0", prog_name="asa-soundboard")
def main(
    config: Path,
    host: str,
    port: int,
    no_browser: bool,
    debug: bool,
    verbose: bool,
    create_example: Path,
) -> int:
    """Virtual DJ Soundboard - A customizable grid-based audio playback interface

    Examples:
      asa-soundboard --config soundboard.json
      asa-soundboard --config my_sounds.json --host 0.0.0.0 --port 8080
      asa-soundboard --create-example example.json
      asa-soundboard --config sounds.json --no-browser --verbose

    The configuration file should be in JSON format with this structure:
    {
      "layout": {"rows": 3, "cols": 4},
      "buttons": [
        {
          "file": "path/to/audio.m4a",
          "row": 1,
          "col": 1,
          "label": "Button Label"
        }
      ]
    }
    """
    setup_logging(verbose)
    logger = logging.getLogger(__name__)

    try:
        # Handle example creation
        if create_example:
            create_example_config(create_example)
            print(f"Example configuration created: {create_example}")
            print(
                "Edit the file to customize your soundboard layout and button assignments."
            )
            return 0

        # Validate required arguments
        if not config:
            ctx = click.get_current_context()
            ctx.fail("--config is required (or use --create-example to get started)")

        # Validate configuration file
        validate_config_file(config)

        # Create and start soundboard
        logger.info(f"Loading configuration from: {config}")
        soundboard = VirtualDJSoundboard(config_path=config, host=host, port=port)

        # Open browser unless disabled
        if not no_browser:
            url = f"http://{host}:{port}"
            open_browser(url)
        else:
            print(f"Soundboard available at: http://{host}:{port}")

        # Start the web server
        soundboard.run(debug=debug)

        return 0

    except KeyboardInterrupt:
        logger.info("Shutting down soundboard...")
        return 0

    except click.ClickException:
        # Re-raise click exceptions to preserve proper exit codes
        raise

    except AudioSnippetError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    except Exception as e:
        logger.exception("Unexpected error occurred")
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
