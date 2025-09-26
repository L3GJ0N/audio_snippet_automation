"""Tests for soundboard CLI functionality."""

from click.testing import CliRunner

from audio_snippet_automation.soundboard_cli import main


class TestSoundboardCLI:
    """Test suite for soundboard CLI."""

    def test_help_command(self):
        """Test that help command works."""
        runner = CliRunner()
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "Virtual DJ Soundboard" in result.output

    def test_version_option(self):
        """Test version option."""
        runner = CliRunner()
        result = runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "0.2.0" in result.output

    def test_missing_config_argument(self):
        """Test error when no arguments provided."""
        runner = CliRunner()
        result = runner.invoke(main, [])
        # Should return error code (click uses exit code 2 for usage errors)
        assert result.exit_code == 2
        assert "--config is required" in result.output

    def test_create_example_config(self, tmp_path):
        """Test creating example configuration."""
        runner = CliRunner()
        config_path = tmp_path / "example_config.json"

        result = runner.invoke(main, ["--create-example", str(config_path)])
        # Should exit cleanly
        assert result.exit_code == 0

        # Check that config file was created
        assert config_path.exists()
