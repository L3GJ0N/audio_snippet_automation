"""Audio Snippet Automation - Batch YouTube audio snippet extractor."""

__version__ = "0.2.0"
__author__ = "Your Name"
__description__ = "Create multiple precisely trimmed audio snippets from YouTube URLs using a single CSV file."

from .cli import main

__all__ = ["main"]
