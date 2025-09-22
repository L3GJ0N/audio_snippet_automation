"""Tests for soundboard CLI functionality."""

import json
from unittest.mock import patch

import pytest
from audio_snippet_automation.soundboard_cli import main


class TestSoundboardCLI:
    """Test suite for soundboard CLI."""

    def test_help_command(self, capsys):
        """Test that help command works."""
        with pytest.raises(SystemExit) as exc_info:
            with patch("sys.argv", ["asa-soundboard", "--help"]):
                main()

        # Help should exit with code 0
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "Virtual DJ Soundboard" in captured.out

    def test_missing_config_argument(self, capsys):
        """Test error when no arguments provided."""
        with pytest.raises(SystemExit) as exc_info:
            with patch("sys.argv", ["asa-soundboard"]):
                main()

        # Should exit with error code
        assert exc_info.value.code != 0
        captured = capsys.readouterr()
        assert "one of the arguments" in captured.err or "required" in captured.err

    def test_create_example_config(self, tmp_path):
        """Test creating example configuration."""
        config_path = tmp_path / "example_config.json"

        with patch(
            "sys.argv", ["asa-soundboard", "--create-example", str(config_path)]
        ):
            try:
                main()
            except SystemExit as e:
                # Should exit cleanly
                assert e.code == 0 or e.code is None

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
        non_existent_config = tmp_path / "does_not_exist.json"

        with pytest.raises(SystemExit):
            with patch(
                "sys.argv", ["asa-soundboard", "--config", str(non_existent_config)]
            ):
                main()

    def test_invalid_json_config(self, tmp_path):
        """Test error handling for invalid JSON config."""
        invalid_config = tmp_path / "invalid.json"
        invalid_config.write_text("{ invalid json }")

        with pytest.raises(SystemExit):
            with patch("sys.argv", ["asa-soundboard", "--config", str(invalid_config)]):
                main()

    def test_config_missing_required_fields(self, tmp_path):
        """Test error handling for config missing required fields."""
        incomplete_config = tmp_path / "incomplete.json"
        config_data = {"layout": {"rows": 4}}  # Missing cols and buttons
        incomplete_config.write_text(json.dumps(config_data))

        with pytest.raises(SystemExit):
            with patch(
                "sys.argv", ["asa-soundboard", "--config", str(incomplete_config)]
            ):
                main()

    @patch("audio_snippet_automation.soundboard.VirtualDJSoundboard.run")
    def test_valid_config_starts_server(self, mock_run, tmp_path):
        """Test that valid config starts the soundboard server."""
        valid_config = tmp_path / "valid.json"
        config_data = {
            "layout": {"rows": 2, "cols": 2},
            "buttons": [
                {
                    "file": "test.wav",
                    "row": 1,
                    "col": 1,
                    "label": "Test Button",
                }
            ],
        }
        valid_config.write_text(json.dumps(config_data))

        # Mock the server run method to avoid actually starting Flask
        mock_run.return_value = None

        with patch("sys.argv", ["asa-soundboard", "--config", str(valid_config)]):
            try:
                main()
            except SystemExit:
                pass

        # Verify that the soundboard server was attempted to start
        mock_run.assert_called_once()

    def test_custom_host_and_port(self, tmp_path):
        """Test custom host and port arguments."""
        valid_config = tmp_path / "valid.json"
        config_data = {
            "layout": {"rows": 2, "cols": 2},
            "buttons": [],
        }
        valid_config.write_text(json.dumps(config_data))

        with patch(
            "audio_snippet_automation.soundboard.VirtualDJSoundboard.run"
        ) as mock_run:
            with patch(
                "sys.argv",
                [
                    "asa-soundboard",
                    "--config",
                    str(valid_config),
                    "--host",
                    "0.0.0.0",
                    "--port",
                    "8080",
                ],
            ):
                try:
                    main()
                except SystemExit:
                    pass

            # Check that run was called with custom host and port
            mock_run.assert_called_once()
            args, kwargs = mock_run.call_args
            assert kwargs.get("host") == "0.0.0.0"
            assert kwargs.get("port") == 8080

    def test_no_browser_flag(self, tmp_path):
        """Test --no-browser flag."""
        valid_config = tmp_path / "valid.json"
        config_data = {
            "layout": {"rows": 2, "cols": 2},
            "buttons": [],
        }
        valid_config.write_text(json.dumps(config_data))

        with patch(
            "audio_snippet_automation.soundboard.VirtualDJSoundboard"
        ) as mock_soundboard:
            mock_instance = mock_soundboard.return_value
            mock_instance.run.return_value = None

            with patch(
                "sys.argv",
                ["asa-soundboard", "--config", str(valid_config), "--no-browser"],
            ):
                try:
                    main()
                except SystemExit:
                    pass

            # Verify soundboard was created without auto_open_browser
            mock_soundboard.assert_called_once()
            args, kwargs = mock_soundboard.call_args
            assert kwargs.get("auto_open_browser") is False

    def test_debug_and_verbose_flags(self, tmp_path):
        """Test debug and verbose flags."""
        valid_config = tmp_path / "valid.json"
        config_data = {
            "layout": {"rows": 2, "cols": 2},
            "buttons": [],
        }
        valid_config.write_text(json.dumps(config_data))

        with patch(
            "audio_snippet_automation.soundboard.VirtualDJSoundboard.run"
        ) as mock_run:
            with patch(
                "sys.argv",
                [
                    "asa-soundboard",
                    "--config",
                    str(valid_config),
                    "--debug",
                    "--verbose",
                ],
            ):
                try:
                    main()
                except SystemExit:
                    pass

            # Check that run was called with debug enabled
            mock_run.assert_called_once()
            args, kwargs = mock_run.call_args
            assert kwargs.get("debug") is True

    def test_config_validation_button_positions(self, tmp_path):
        """Test config validation for button positions."""
        invalid_config = tmp_path / "invalid_positions.json"
        config_data = {
            "layout": {"rows": 2, "cols": 2},
            "buttons": [
                {
                    "file": "test.wav",
                    "row": 5,  # Invalid: outside grid
                    "col": 1,
                    "label": "Test Button",
                }
            ],
        }
        invalid_config.write_text(json.dumps(config_data))

        with pytest.raises(SystemExit):
            with patch("sys.argv", ["asa-soundboard", "--config", str(invalid_config)]):
                main()


@pytest.fixture
def sample_soundboard_config():
    """Provide sample soundboard configuration for tests."""
    return {
        "layout": {"rows": 4, "cols": 6},
        "buttons": [
            {
                "file": "test1.wav",
                "row": 1,
                "col": 1,
                "label": "Test Button 1",
            },
            {
                "file": "test2.wav",
                "row": 1,
                "col": 2,
                "label": "Test Button 2",
            },
        ],
    }


@pytest.fixture
def sample_config_file(tmp_path, sample_soundboard_config):
    """Create a temporary config file with sample content."""
    config_file = tmp_path / "test_config.json"
    config_file.write_text(json.dumps(sample_soundboard_config))
    return config_file
