"""Tests for snippet CLI functionality."""

from unittest.mock import patch

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

    def test_missing_csv_argument(self):
        """Test error when CSV argument is missing."""
        runner = CliRunner()
        result = runner.invoke(main, [])
        # Should exit with error code (click uses 2 for missing required args)
        assert result.exit_code == 2
        assert "required" in result.output.lower() or "csv" in result.output.lower()

    def test_invalid_csv_file(self, tmp_path):
        """Test error handling for non-existent CSV file."""
        runner = CliRunner()
        non_existent_csv = tmp_path / "does_not_exist.csv"

        result = runner.invoke(main, ["--csv", str(non_existent_csv)])
        assert result.exit_code == 2  # Click error for invalid path
        assert "does not exist" in result.output or "No such file" in result.output

    def test_empty_csv_file(self, tmp_path):
        """Test handling of empty CSV file."""
        runner = CliRunner()
        empty_csv = tmp_path / "empty.csv"
        empty_csv.write_text("")

        result = runner.invoke(main, ["--csv", str(empty_csv)])
        assert result.exit_code != 0

    def test_invalid_csv_format(self, tmp_path):
        """Test handling of CSV with missing required columns."""
        runner = CliRunner()
        invalid_csv = tmp_path / "invalid.csv"
        invalid_csv.write_text("url,start\nhttps://example.com,0")

        result = runner.invoke(main, ["--csv", str(invalid_csv)])
        assert result.exit_code != 0

    @patch("audio_snippet_automation.snippet_cli.process_csv_row")
    @patch("audio_snippet_automation.snippet_cli.validate_csv_format")
    def test_valid_csv_processing(self, mock_validate, mock_process, tmp_path):
        """Test successful CSV processing with mocked external calls."""
        runner = CliRunner()
        # Create a valid CSV file
        valid_csv = tmp_path / "valid.csv"
        csv_content = "url,start,end,output\nhttps://example.com,0,10,test"
        valid_csv.write_text(csv_content)

        # Mock the validation to pass
        mock_validate.return_value = None
        # Mock the processing to avoid actual downloads
        mock_process.return_value = None

        result = runner.invoke(main, ["--csv", str(valid_csv)])
        # Should exit cleanly with mocked functions
        assert result.exit_code == 0

    def test_generate_soundboard_config_flag(self, tmp_path):
        """Test soundboard config generation flag."""
        runner = CliRunner()
        valid_csv = tmp_path / "valid.csv"
        config_path = tmp_path / "test_config.json"
        csv_content = "url,start,end,output\nhttps://example.com,0,10,test"
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
                result = runner.invoke(
                    main,
                    [
                        "--csv",
                        str(valid_csv),
                        "--generate-soundboard-config",
                        str(config_path),
                    ],
                )
                # Should complete without error
                assert result.exit_code == 0

    @patch("audio_snippet_automation.snippet_cli.process_csv_row")
    @patch("audio_snippet_automation.snippet_cli.validate_csv_format")
    @patch("audio_snippet_automation.snippet_cli.Path.mkdir")
    def test_output_directory_creation(
        self, mock_mkdir, mock_validate, mock_process, tmp_path
    ):
        """Test that output directory is created."""
        runner = CliRunner()
        valid_csv = tmp_path / "valid.csv"
        valid_csv.write_text("url,start,end,output\nhttps://example.com,0,10,test")
        output_dir = tmp_path / "output"

        result = runner.invoke(
            main, ["--csv", str(valid_csv), "--outdir", str(output_dir)]
        )
        # Should complete with mocked functions
        assert result.exit_code == 0

    def test_custom_options(self, tmp_path):
        """Test CLI with custom options."""
        runner = CliRunner()
        valid_csv = tmp_path / "valid.csv"
        valid_csv.write_text("url,start,end,output\nhttps://example.com,0,10,test")

        with patch("audio_snippet_automation.snippet_cli.validate_csv_format"):
            with patch("audio_snippet_automation.snippet_cli.process_csv_row"):
                result = runner.invoke(main, ["--csv", str(valid_csv), "--precise"])
                # Should complete with mocked functions
                assert result.exit_code == 0

    def test_version_option(self):
        """Test version option."""
        runner = CliRunner()
        result = runner.invoke(main, ["--version"])
        assert result.exit_code == 0
        assert "0.2.0" in result.output

    def test_tempdir_option(self, tmp_path):
        """Test custom temporary directory option."""
        runner = CliRunner()
        valid_csv = tmp_path / "valid.csv"
        valid_csv.write_text("url,start,end,output\nhttps://example.com,0,10,test")
        temp_dir = tmp_path / "temp"

        with patch("audio_snippet_automation.snippet_cli.validate_csv_format"):
            with patch("audio_snippet_automation.snippet_cli.process_csv_row"):
                result = runner.invoke(
                    main, ["--csv", str(valid_csv), "--tempdir", str(temp_dir)]
                )
                assert result.exit_code == 0

    def test_cookies_from_browser_option(self, tmp_path):
        """Test cookies from browser option."""
        runner = CliRunner()
        valid_csv = tmp_path / "valid.csv"
        valid_csv.write_text("url,start,end,output\nhttps://example.com,0,10,test")

        with patch("audio_snippet_automation.snippet_cli.validate_csv_format"):
            with patch("audio_snippet_automation.snippet_cli.process_csv_row"):
                result = runner.invoke(
                    main, ["--csv", str(valid_csv), "--cookies-from-browser", "chrome"]
                )
                assert result.exit_code == 0

    def test_cookies_file_option(self, tmp_path):
        """Test cookies file option."""
        runner = CliRunner()
        valid_csv = tmp_path / "valid.csv"
        valid_csv.write_text("url,start,end,output\nhttps://example.com,0,10,test")
        cookies_file = tmp_path / "cookies.txt"
        cookies_file.write_text("# Netscape HTTP Cookie File")

        with patch("audio_snippet_automation.snippet_cli.validate_csv_format"):
            with patch("audio_snippet_automation.snippet_cli.process_csv_row"):
                result = runner.invoke(
                    main, ["--csv", str(valid_csv), "--cookies", str(cookies_file)]
                )
                assert result.exit_code == 0

    def test_soundboard_layout_option(self, tmp_path):
        """Test soundboard layout option."""
        runner = CliRunner()
        valid_csv = tmp_path / "valid.csv"
        config_path = tmp_path / "test_config.json"
        csv_content = "url,start,end,output\nhttps://example.com,0,10,test"
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
                result = runner.invoke(
                    main,
                    [
                        "--csv",
                        str(valid_csv),
                        "--generate-soundboard-config",
                        str(config_path),
                        "--soundboard-layout",
                        "3",
                        "5",
                    ],
                )
                # Should complete without error
                assert result.exit_code == 0

    def test_precise_flag(self, tmp_path):
        """Test precise re-encoding flag."""
        runner = CliRunner()
        valid_csv = tmp_path / "valid.csv"
        valid_csv.write_text("url,start,end,output\nhttps://example.com,0,10,test")

        with patch("audio_snippet_automation.snippet_cli.validate_csv_format"):
            with patch("audio_snippet_automation.snippet_cli.process_csv_row"):
                result = runner.invoke(main, ["--csv", str(valid_csv), "--precise"])
                # Should complete with mocked functions
                assert result.exit_code == 0

    @patch("audio_snippet_automation.snippet_cli.validate_csv_format")
    @patch("audio_snippet_automation.snippet_cli.process_csv_row")
    def test_comprehensive_options_combination(
        self, mock_process, mock_validate, tmp_path
    ):
        """Test CLI with comprehensive combination of options."""
        runner = CliRunner()
        valid_csv = tmp_path / "valid.csv"
        valid_csv.write_text("url,start,end,output\nhttps://example.com,0,10,test")
        output_dir = tmp_path / "output"
        temp_dir = tmp_path / "temp"
        config_path = tmp_path / "soundboard.json"
        cookies_file = tmp_path / "cookies.txt"
        cookies_file.write_text("# Netscape HTTP Cookie File")

        # Mock the functions to avoid actual processing
        mock_validate.return_value = None
        mock_process.return_value = None

        result = runner.invoke(
            main,
            [
                "--csv",
                str(valid_csv),
                "--precise",
                "--outdir",
                str(output_dir),
                "--tempdir",
                str(temp_dir),
                "--cookies",
                str(cookies_file),
                "--generate-soundboard-config",
                str(config_path),
                "--soundboard-layout",
                "4",
                "3",
            ],
        )

        # Should complete successfully with all options
        assert result.exit_code == 0
        assert mock_validate.called
        assert mock_process.called
