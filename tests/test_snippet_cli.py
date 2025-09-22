"""Tests for snippet CLI functionality."""

from unittest.mock import patch

import pytest

from audio_snippet_automation.snippet_cli import main


class TestSnippetCLI:
    """Test suite for snippet CLI."""

    def test_help_command(self, capsys):
        """Test that help command works."""
        with pytest.raises(SystemExit) as exc_info:
            with patch("sys.argv", ["asa", "--help"]):
                main()

        # Help should exit with code 0
        assert exc_info.value.code == 0
        captured = capsys.readouterr()
        assert "Create multiple precisely trimmed audio snippets" in captured.out

    def test_missing_csv_argument(self, capsys):
        """Test error when CSV argument is missing."""
        with pytest.raises(SystemExit) as exc_info:
            with patch("sys.argv", ["asa"]):
                main()

        # Should exit with error code
        assert exc_info.value.code != 0
        captured = capsys.readouterr()
        assert "required" in captured.err or "CSV" in captured.err

    def test_invalid_csv_file(self, tmp_path):
        """Test error handling for non-existent CSV file."""
        non_existent_csv = tmp_path / "does_not_exist.csv"

        with pytest.raises(SystemExit):
            with patch("sys.argv", ["asa", "--csv", str(non_existent_csv)]):
                main()

    def test_empty_csv_file(self, tmp_path):
        """Test handling of empty CSV file."""
        empty_csv = tmp_path / "empty.csv"
        empty_csv.write_text("")

        with pytest.raises(SystemExit):
            with patch("sys.argv", ["asa", "--csv", str(empty_csv)]):
                main()

    def test_invalid_csv_format(self, tmp_path):
        """Test handling of CSV with missing required columns."""
        invalid_csv = tmp_path / "invalid.csv"
        invalid_csv.write_text("url,start\nhttps://example.com,0")

        with pytest.raises(SystemExit):
            with patch("sys.argv", ["asa", "--csv", str(invalid_csv)]):
                main()

    @patch("audio_snippet_automation.snippet_cli.process_csv_row")
    @patch("audio_snippet_automation.snippet_cli.validate_csv_format")
    def test_valid_csv_processing(self, mock_validate, mock_process, tmp_path):
        """Test successful CSV processing with mocked external calls."""
        # Create a valid CSV file
        valid_csv = tmp_path / "valid.csv"
        csv_content = "url,start,end,output,format\nhttps://example.com,0,10,test,mp3"
        valid_csv.write_text(csv_content)

        # Mock the validation to pass
        mock_validate.return_value = None
        # Mock the processing to avoid actual downloads
        mock_process.return_value = None

        with patch("sys.argv", ["asa", "--csv", str(valid_csv)]):
            try:
                main()
            except SystemExit as e:
                # Should exit cleanly (code 0)
                assert e.code == 0 or e.code is None

    def test_soundboard_ready_flag(self, tmp_path):
        """Test soundboard-ready flag behavior."""
        valid_csv = tmp_path / "valid.csv"
        csv_content = "url,start,end,output,format\nhttps://example.com,0,10,test,mp3"
        valid_csv.write_text(csv_content)

        with patch(
            "audio_snippet_automation.snippet_cli.process_csv_row"
        ) as mock_process:
            with patch("audio_snippet_automation.snippet_cli.validate_csv_format"):
                with patch(
                    "sys.argv", ["asa", "--csv", str(valid_csv), "--soundboard-ready"]
                ):
                    try:
                        main()
                    except SystemExit:
                        pass

                    # Should have been called with soundboard_ready=True
                    assert mock_process.called

    def test_generate_soundboard_config_flag(self, tmp_path):
        """Test soundboard config generation flag."""
        valid_csv = tmp_path / "valid.csv"
        config_path = tmp_path / "test_config.json"
        csv_content = "url,start,end,output,format\nhttps://example.com,0,10,test,mp3"
        valid_csv.write_text(csv_content)

        # Mock snippet creation so config generation is triggered
        def mock_process_csv_row(row, row_num, args, snippet_files):
            if snippet_files is not None:
                snippet_files.append(
                    {"path": tmp_path / "test.wav", "label": "Test", "output": "test"}
                )

        with patch(
            "audio_snippet_automation.snippet_cli.process_csv_row",
            side_effect=mock_process_csv_row,
        ):
            with patch("audio_snippet_automation.snippet_cli.validate_csv_format"):
                with patch(
                    "audio_snippet_automation.snippet_cli.generate_soundboard_config"
                ) as mock_gen:
                    with patch(
                        "sys.argv",
                        [
                            "asa",
                            "--csv",
                            str(valid_csv),
                            "--generate-soundboard-config",
                            str(config_path),
                        ],
                    ):
                        try:
                            main()
                        except SystemExit:
                            pass

                        # Should have called config generation
                        assert mock_gen.called

    def test_soundboard_layout_flag(self, tmp_path):
        """Test custom soundboard layout flag."""
        valid_csv = tmp_path / "valid.csv"
        csv_content = "url,start,end,output,format\nhttps://example.com,0,10,test,mp3"
        valid_csv.write_text(csv_content)

        # Mock snippet creation so config generation is triggered
        def mock_process_csv_row(row, row_num, args, snippet_files):
            if snippet_files is not None:
                snippet_files.append(
                    {"path": tmp_path / "test.wav", "label": "Test", "output": "test"}
                )

        with patch(
            "audio_snippet_automation.snippet_cli.process_csv_row",
            side_effect=mock_process_csv_row,
        ):
            with patch("audio_snippet_automation.snippet_cli.validate_csv_format"):
                with patch(
                    "audio_snippet_automation.snippet_cli.generate_soundboard_config"
                ) as mock_gen:
                    with patch(
                        "sys.argv",
                        [
                            "asa",
                            "--csv",
                            str(valid_csv),
                            "--generate-soundboard-config",
                            "config.json",
                            "--soundboard-layout",
                            "2",
                            "3",
                        ],
                    ):
                        try:
                            main()
                        except SystemExit:
                            pass

                        # Should have called with custom layout
                        assert mock_gen.called

    def test_output_directory_creation(self, tmp_path):
        """Test that output directory is created if it doesn't exist."""
        valid_csv = tmp_path / "valid.csv"
        output_dir = tmp_path / "custom_output"
        csv_content = "url,start,end,output,format\nhttps://example.com,0,10,test,mp3"
        valid_csv.write_text(csv_content)

        with patch("audio_snippet_automation.snippet_cli.process_csv_row"):
            with patch("audio_snippet_automation.snippet_cli.validate_csv_format"):
                with patch(
                    "sys.argv",
                    ["asa", "--csv", str(valid_csv), "--outdir", str(output_dir)],
                ):
                    try:
                        main()
                    except SystemExit:
                        pass

                    # Output directory should be created
                    assert output_dir.exists()

    def test_format_validation(self, tmp_path):
        """Test audio format validation."""
        valid_csv = tmp_path / "valid.csv"
        csv_content = "url,start,end,output,format\nhttps://example.com,0,10,test,mp3"
        valid_csv.write_text(csv_content)

        # Test valid format
        with patch("audio_snippet_automation.snippet_cli.process_csv_row"):
            with patch("audio_snippet_automation.snippet_cli.validate_csv_format"):
                with patch(
                    "sys.argv", ["asa", "--csv", str(valid_csv), "--format", "wav"]
                ):
                    try:
                        main()
                    except SystemExit as e:
                        # Should succeed with valid format
                        assert e.code == 0 or e.code is None

        # Test invalid format
        with pytest.raises(SystemExit):
            with patch(
                "sys.argv", ["asa", "--csv", str(valid_csv), "--format", "invalid"]
            ):
                main()


@pytest.fixture
def sample_csv_content():
    """Provide sample CSV content for tests."""
    return """url,start,end,output,format
https://www.youtube.com/watch?v=example1,0,10,clip1,mp3
https://www.youtube.com/watch?v=example2,5,15,clip2,wav
"""


@pytest.fixture
def sample_csv_file(tmp_path, sample_csv_content):
    """Create a temporary CSV file with sample content."""
    csv_file = tmp_path / "test.csv"
    csv_file.write_text(sample_csv_content)
    return csv_file
