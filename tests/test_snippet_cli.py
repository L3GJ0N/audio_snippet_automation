"""Tests for snippet CLI functionality."""

from click.testing import CliRunner

from audio_snippet_automation.snippet_cli import main


class TestSnippetCLI:
    """Test suite for snippet CLI."""

    def test_help_command(self):
        """Test that help command works."""
        runner = CliRunner()
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "Create multiple precisely trimmed audio snippets" in result.output

    def test_version_option(self):
        """Test version option."""
        runner = CliRunner()
        result = runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "0.2.0" in result.output
