"""Tests for audio snippet automation."""

import csv
from io import StringIO

import pytest

from audio_snippet_automation.core import (
    AudioSnippetError,
    time_str,
    validate_csv_format,
)


def test_time_str():
    """Test time string validation."""
    assert time_str("00:01:30") == "00:01:30"
    assert time_str("90.5") == "90.5"
    assert time_str("  120  ") == "120"


def test_validate_csv_format_valid():
    """Test CSV validation with valid format."""
    csv_content = "url,start,end,output\nhttps://example.com,0,10,test"
    reader = csv.DictReader(StringIO(csv_content))
    # Should not raise
    validate_csv_format(reader)


def test_validate_csv_format_missing_columns():
    """Test CSV validation with missing required columns."""
    csv_content = "url,start\nhttps://example.com,0"
    reader = csv.DictReader(StringIO(csv_content))

    with pytest.raises(AudioSnippetError, match="CSV must include columns"):
        validate_csv_format(reader)


def test_audio_snippet_error():
    """Test custom exception."""
    with pytest.raises(AudioSnippetError):
        raise AudioSnippetError("Test error")
