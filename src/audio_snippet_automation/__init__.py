"""Audio Snippet Automation - Batch YouTube audio snippet extractor and virtual DJ soundboard."""

__version__ = "0.2.0"
__author__ = "Your Name"
__description__ = "Create multiple precisely trimmed audio snippets from YouTube URLs using a single CSV file, and play them with a virtual DJ soundboard."

from .cli import main
from .soundboard_cli import main as soundboard_main

__all__ = ["main", "soundboard_main"]
