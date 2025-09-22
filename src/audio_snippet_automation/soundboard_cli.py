#!/usr/bin/env python3
"""
Command-line interface for the Virtual DJ Soundboard.

This module provides a CLI to launch the web-based soundboard interface.
"""

import argparse
import logging
import sys
import webbrowser
from pathlib import Path
from threading import Timer

from .soundboard import AudioSnippetError, VirtualDJSoundboard, create_example_config


def setup_logging(verbose: bool = False) -> None:
    """Configure logging for the application."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="Virtual DJ Soundboard - A customizable grid-based audio playback interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --config soundboard.json
  %(prog)s --config my_sounds.json --host 0.0.0.0 --port 8080
  %(prog)s --create-example example.json
  %(prog)s --config sounds.json --no-browser --verbose

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
        """,
    )

    parser.add_argument(
        "--config", "-c", type=Path, help="Path to JSON configuration file"
    )

    parser.add_argument(
        "--host",
        default="localhost",
        help="Host to bind the web server (default: localhost)",
    )

    parser.add_argument(
        "--port",
        "-p",
        type=int,
        default=8080,
        help="Port for the web server (default: 8080)",
    )

    parser.add_argument(
        "--no-browser", action="store_true", help="Do not automatically open browser"
    )

    parser.add_argument("--debug", action="store_true", help="Enable Flask debug mode")

    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    parser.add_argument(
        "--create-example",
        type=Path,
        metavar="FILENAME",
        help="Create an example configuration file and exit",
    )

    parser.add_argument("--version", action="version", version="%(prog)s 0.2.0")

    return parser


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


def main() -> int:
    """Main entry point for the soundboard CLI."""
    parser = create_parser()
    args = parser.parse_args()

    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)

    try:
        # Handle example creation
        if args.create_example:
            create_example_config(args.create_example)
            print(f"Example configuration created: {args.create_example}")
            print(
                "Edit the file to customize your soundboard layout and button assignments."
            )
            return 0

        # Validate required arguments
        if not args.config:
            print(
                "Error: --config is required (or use --create-example to get started)"
            )
            parser.print_help()
            return 1

        # Validate configuration file
        validate_config_file(args.config)

        # Create and start soundboard
        logger.info(f"Loading configuration from: {args.config}")
        soundboard = VirtualDJSoundboard(
            config_path=args.config, host=args.host, port=args.port
        )

        # Open browser unless disabled
        if not args.no_browser:
            url = f"http://{args.host}:{args.port}"
            open_browser(url)
        else:
            print(f"Soundboard available at: http://{args.host}:{args.port}")

        # Start the web server
        soundboard.run(debug=args.debug)

        return 0

    except KeyboardInterrupt:
        logger.info("Shutting down soundboard...")
        return 0

    except AudioSnippetError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    except Exception as e:
        logger.exception("Unexpected error occurred")
        print(f"Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
