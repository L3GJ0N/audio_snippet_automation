"""Tests for soundboard CLI functionality."""

import json
from unittest.mock import patch

from click.testing import CliRunner

from audio_snippet_automation.soundboard_cli import main


class TestSoundboardCLI:
    """Test suite for soundboard CLI."""

    def test_help_command(self):
        """Test that help command works."""
        runner = CliRunner()
        result = runner.invoke(main, ["--help"])
        assert result.exit_code == 0
        assert "MemeDeck Live" in result.output

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

        # Verify it's valid JSON
        with open(config_path) as f:
            config = json.load(f)
            assert "layout" in config
            assert "buttons" in config
            assert config["layout"]["rows"] > 0
            assert config["layout"]["cols"] > 0

    def test_invalid_config_file(self, tmp_path):
        """Test error handling for non-existent config file."""
        runner = CliRunner()
        non_existent_config = tmp_path / "does_not_exist.json"

        result = runner.invoke(main, ["--config", str(non_existent_config)])
        # Should return error code (click uses 2 for path validation errors)
        assert result.exit_code == 2

    def test_invalid_json_config(self, tmp_path):
        """Test error handling for invalid JSON config."""
        runner = CliRunner()
        invalid_config = tmp_path / "invalid.json"
        invalid_config.write_text("{ invalid json }")

        result = runner.invoke(main, ["--config", str(invalid_config)])
        # Should return error code
        assert result.exit_code != 0

    def test_config_missing_required_fields(self, tmp_path):
        """Test error handling for config missing required fields."""
        runner = CliRunner()
        incomplete_config = tmp_path / "incomplete.json"
        config_data = {"layout": {"rows": 4}}  # Missing cols and buttons
        incomplete_config.write_text(json.dumps(config_data))

        result = runner.invoke(main, ["--config", str(incomplete_config)])
        # Should return error code
        assert result.exit_code != 0

    @patch("audio_snippet_automation.soundboard.pygame.mixer.init")
    @patch("audio_snippet_automation.soundboard.pygame.mixer.pre_init")
    @patch("audio_snippet_automation.soundboard.pygame.mixer.set_num_channels")
    @patch("audio_snippet_automation.soundboard.VirtualDJSoundboard.run")
    def test_valid_config_starts_server(
        self, mock_run, mock_set_channels, mock_pre_init, mock_init, tmp_path
    ):
        """Test that valid config starts the server."""
        runner = CliRunner()
        config_path = tmp_path / "valid_config.json"

        # Create dummy audio file
        audio_file = tmp_path / "test.mp3"
        audio_file.write_text("dummy audio content")

        config_data = {
            "layout": {"rows": 2, "cols": 2},
            "buttons": [{"file": str(audio_file), "row": 1, "col": 1, "label": "Test"}],
        }
        config_path.write_text(json.dumps(config_data))

        # Mock pygame and server initialization
        mock_init.return_value = None
        mock_pre_init.return_value = None
        mock_set_channels.return_value = None
        mock_run.return_value = None

        with patch("audio_snippet_automation.soundboard_cli.open_browser"):
            result = runner.invoke(main, ["--config", str(config_path)])

        # Should start successfully
        assert result.exit_code == 0
        assert mock_run.called

    def test_version_option(self):
        """Test version option."""
        runner = CliRunner()
        result = runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "0.2.0" in result.output

    @patch("audio_snippet_automation.soundboard.pygame.mixer.init")
    @patch("audio_snippet_automation.soundboard.pygame.mixer.pre_init")
    @patch("audio_snippet_automation.soundboard.pygame.mixer.set_num_channels")
    @patch("audio_snippet_automation.soundboard.VirtualDJSoundboard.run")
    def test_custom_host_port(
        self, mock_run, mock_set_channels, mock_pre_init, mock_init, tmp_path
    ):
        """Test custom host and port options."""
        runner = CliRunner()
        config_path = tmp_path / "valid_config.json"

        # Create dummy audio file
        audio_file = tmp_path / "test.mp3"
        audio_file.write_text("dummy audio content")

        config_data = {
            "layout": {"rows": 2, "cols": 2},
            "buttons": [{"file": str(audio_file), "row": 1, "col": 1, "label": "Test"}],
        }
        config_path.write_text(json.dumps(config_data))

        mock_run.return_value = None

        with patch("audio_snippet_automation.soundboard_cli.open_browser"):
            result = runner.invoke(
                main,
                ["--config", str(config_path), "--host", "0.0.0.0", "--port", "9000"],
            )

        assert result.exit_code == 0

    @patch("audio_snippet_automation.soundboard.pygame.mixer.init")
    @patch("audio_snippet_automation.soundboard.pygame.mixer.pre_init")
    @patch("audio_snippet_automation.soundboard.pygame.mixer.set_num_channels")
    @patch("audio_snippet_automation.soundboard.VirtualDJSoundboard.run")
    def test_no_browser_flag(
        self, mock_run, mock_set_channels, mock_pre_init, mock_init, tmp_path
    ):
        """Test --no-browser flag."""
        runner = CliRunner()
        config_path = tmp_path / "valid_config.json"

        # Create dummy audio file
        audio_file = tmp_path / "test.mp3"
        audio_file.write_text("dummy audio content")

        config_data = {
            "layout": {"rows": 2, "cols": 2},
            "buttons": [{"file": str(audio_file), "row": 1, "col": 1, "label": "Test"}],
        }
        config_path.write_text(json.dumps(config_data))

        mock_run.return_value = None

        with patch(
            "audio_snippet_automation.soundboard_cli.open_browser"
        ) as mock_browser:
            result = runner.invoke(main, ["--config", str(config_path), "--no-browser"])

        assert result.exit_code == 0
        # Browser should not be opened
        assert not mock_browser.called

    @patch("audio_snippet_automation.soundboard.pygame.mixer.init")
    @patch("audio_snippet_automation.soundboard.pygame.mixer.pre_init")
    @patch("audio_snippet_automation.soundboard.pygame.mixer.set_num_channels")
    @patch("audio_snippet_automation.soundboard.VirtualDJSoundboard.run")
    def test_debug_flag(
        self, mock_run, mock_set_channels, mock_pre_init, mock_init, tmp_path
    ):
        """Test --debug flag."""
        runner = CliRunner()
        config_path = tmp_path / "valid_config.json"

        # Create dummy audio file
        audio_file = tmp_path / "test.mp3"
        audio_file.write_text("dummy audio content")

        config_data = {
            "layout": {"rows": 2, "cols": 2},
            "buttons": [{"file": str(audio_file), "row": 1, "col": 1, "label": "Test"}],
        }
        config_path.write_text(json.dumps(config_data))

        mock_run.return_value = None

        with patch("audio_snippet_automation.soundboard_cli.open_browser"):
            result = runner.invoke(main, ["--config", str(config_path), "--debug"])

        assert result.exit_code == 0
        # Debug should be passed to run method
        assert mock_run.called

    @patch("audio_snippet_automation.soundboard.pygame.mixer.init")
    @patch("audio_snippet_automation.soundboard.pygame.mixer.pre_init")
    @patch("audio_snippet_automation.soundboard.pygame.mixer.set_num_channels")
    @patch("audio_snippet_automation.soundboard.VirtualDJSoundboard.run")
    def test_verbose_flag(
        self, mock_run, mock_set_channels, mock_pre_init, mock_init, tmp_path
    ):
        """Test --verbose flag."""
        runner = CliRunner()
        config_path = tmp_path / "valid_config.json"

        # Create dummy audio file
        audio_file = tmp_path / "test.mp3"
        audio_file.write_text("dummy audio content")

        config_data = {
            "layout": {"rows": 2, "cols": 2},
            "buttons": [{"file": str(audio_file), "row": 1, "col": 1, "label": "Test"}],
        }
        config_path.write_text(json.dumps(config_data))

        mock_run.return_value = None

        with patch("audio_snippet_automation.soundboard_cli.open_browser"):
            result = runner.invoke(main, ["--config", str(config_path), "--verbose"])

        assert result.exit_code == 0

    def test_config_with_audio_files_validation(self, tmp_path):
        """Test config validation with actual audio file references."""
        runner = CliRunner()
        config_path = tmp_path / "config_with_files.json"

        # Create fake audio files
        audio_file1 = tmp_path / "sound1.mp3"
        audio_file2 = tmp_path / "sound2.wav"
        audio_file1.touch()
        audio_file2.touch()

        config_data = {
            "layout": {"rows": 2, "cols": 2},
            "buttons": [
                {"file": str(audio_file1), "row": 1, "col": 1, "label": "Sound 1"},
                {"file": str(audio_file2), "row": 1, "col": 2, "label": "Sound 2"},
            ],
        }
        config_path.write_text(json.dumps(config_data))

        with patch("audio_snippet_automation.soundboard.VirtualDJSoundboard.run"):
            with patch("audio_snippet_automation.soundboard_cli.open_browser"):
                result = runner.invoke(main, ["--config", str(config_path)])

        # Should handle config with file references correctly
        assert result.exit_code == 0

    @patch("audio_snippet_automation.soundboard.pygame.mixer.init")
    @patch("audio_snippet_automation.soundboard.pygame.mixer.pre_init")
    @patch("audio_snippet_automation.soundboard.pygame.mixer.set_num_channels")
    @patch("audio_snippet_automation.soundboard.VirtualDJSoundboard.run")
    def test_comprehensive_options(
        self, mock_run, mock_set_channels, mock_pre_init, mock_init, tmp_path
    ):
        """Test CLI with comprehensive combination of options."""
        runner = CliRunner()
        config_path = tmp_path / "comprehensive_config.json"

        # Create dummy audio files
        audio_file1 = tmp_path / "test1.mp3"
        audio_file2 = tmp_path / "test2.wav"
        audio_file1.write_text("dummy audio content 1")
        audio_file2.write_text("dummy audio content 2")

        config_data = {
            "layout": {"rows": 3, "cols": 4},
            "buttons": [
                {"file": str(audio_file1), "row": 1, "col": 1, "label": "Test 1"},
                {"file": str(audio_file2), "row": 1, "col": 2, "label": "Test 2"},
            ],
        }
        config_path.write_text(json.dumps(config_data))

        mock_run.return_value = None

        with patch("audio_snippet_automation.soundboard_cli.open_browser"):
            result = runner.invoke(
                main,
                [
                    "--config",
                    str(config_path),
                    "--host",
                    "localhost",
                    "--port",
                    "8080",
                    "--no-browser",
                    "--debug",
                    "--verbose",
                ],
            )

        assert result.exit_code == 0
        assert mock_run.called
