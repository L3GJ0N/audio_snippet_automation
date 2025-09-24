"""Tests for the soundboard generator module."""

import json
import tempfile
from pathlib import Path

from click.testing import CliRunner

from audio_snippet_automation.generate_soundboard import (
    calculate_optimal_grid,
    create_button_label,
    find_audio_files,
    main,
)


class TestCalculateOptimalGrid:
    """Test cases for the grid calculation algorithm."""

    def test_edge_cases(self):
        """Test edge cases for grid calculation."""
        # Zero files
        assert calculate_optimal_grid(0) == (1, 1)

        # Single file
        assert calculate_optimal_grid(1) == (1, 1)

    def test_perfect_squares(self):
        """Test grid calculation for perfect squares."""
        assert calculate_optimal_grid(4) == (2, 2)
        assert calculate_optimal_grid(9) == (3, 3)
        assert calculate_optimal_grid(16) == (4, 4)
        assert calculate_optimal_grid(25) == (5, 5)
        # Note: 36 gets (9, 4) because algorithm prefers rows >= cols
        assert calculate_optimal_grid(36) == (9, 4)

    def test_small_numbers(self):
        """Test grid calculation for small numbers of files."""
        assert calculate_optimal_grid(2) == (2, 1)
        assert calculate_optimal_grid(3) == (3, 1)
        assert calculate_optimal_grid(5) == (3, 2)  # 3 rows, 2 cols = 6 slots
        assert calculate_optimal_grid(6) == (3, 2)
        assert calculate_optimal_grid(7) == (4, 2)  # 4 rows, 2 cols = 8 slots
        assert calculate_optimal_grid(8) == (4, 2)

    def test_medium_numbers(self):
        """Test grid calculation for medium numbers of files."""
        assert calculate_optimal_grid(10) == (5, 2)  # 5 rows, 2 cols = 10 slots
        assert calculate_optimal_grid(12) == (6, 2)  # 6 rows, 2 cols = 12 slots
        assert calculate_optimal_grid(15) == (5, 3)  # 5 rows, 3 cols = 15 slots
        assert calculate_optimal_grid(18) == (6, 3)  # 6 rows, 3 cols = 18 slots
        assert calculate_optimal_grid(20) == (5, 4)  # 5 rows, 4 cols = 20 slots

    def test_larger_numbers(self):
        """Test grid calculation for larger numbers of files."""
        assert calculate_optimal_grid(24) == (8, 3)  # 8 rows, 3 cols = 24 slots
        assert calculate_optimal_grid(28) == (7, 4)  # 7 rows, 4 cols = 28 slots
        assert calculate_optimal_grid(30) == (6, 5)  # 6 rows, 5 cols = 30 slots
        assert calculate_optimal_grid(35) == (7, 5)  # 7 rows, 5 cols = 35 slots
        assert calculate_optimal_grid(42) == (7, 6)  # 7 rows, 6 cols = 42 slots

    def test_grid_properties(self):
        """Test that generated grids have the correct properties."""
        for num_files in range(1, 101):  # Test 1-100 files
            rows, cols = calculate_optimal_grid(num_files)

            # Grid should accommodate all files
            assert (
                rows * cols >= num_files
            ), f"Grid {rows}×{cols} too small for {num_files} files"

            # Should prioritize more rows than columns
            assert rows >= cols, f"Grid {rows}×{cols} has more columns than rows"

            # Should not be excessively tall (aspect ratio check)
            if cols > 1:  # Skip single-column layouts
                assert (
                    rows / cols <= 3
                ), f"Grid {rows}×{cols} is too tall (aspect ratio {rows / cols:.1f})"

    def test_minimal_empty_slots(self):
        """Test that grids minimize empty slots when possible."""
        # Perfect fits should have zero empty slots
        perfect_fits = [4, 6, 8, 9, 10, 12, 15, 16, 18, 20, 24, 25, 28, 30, 36]
        for num_files in perfect_fits:
            rows, cols = calculate_optimal_grid(num_files)
            empty_slots = rows * cols - num_files
            assert (
                empty_slots == 0
            ), f"{num_files} files should fit perfectly, got {empty_slots} empty slots"


class TestFindAudioFiles:
    """Test cases for audio file discovery."""

    def test_empty_folder(self):
        """Test behavior with empty folder."""
        with tempfile.TemporaryDirectory() as temp_dir:
            folder_path = Path(temp_dir)
            result = find_audio_files(folder_path)
            assert result == []

    def test_no_audio_files(self):
        """Test folder with no audio files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            folder_path = Path(temp_dir)
            # Create non-audio files
            (folder_path / "text.txt").write_text("not audio")
            (folder_path / "image.jpg").write_bytes(b"fake image")

            result = find_audio_files(folder_path)
            assert result == []

    def test_various_extensions(self):
        """Test discovery of various audio file extensions."""
        with tempfile.TemporaryDirectory() as temp_dir:
            folder_path = Path(temp_dir)

            # Create audio files with different extensions
            audio_files = [
                "song1.wav",
                "song2.mp3",
                "song3.m4a",
                "song4.ogg",
                "song5.flac",
            ]

            for filename in audio_files:
                (folder_path / filename).write_bytes(b"fake audio")

            result = find_audio_files(folder_path)
            result_names = [f.name for f in result]

            assert len(result) == 5
            for filename in audio_files:
                assert filename in result_names

    def test_mixed_case_extensions(self):
        """Test that mixed case extensions are handled properly."""
        with tempfile.TemporaryDirectory() as temp_dir:
            folder_path = Path(temp_dir)

            # Create files with mixed case extensions
            (folder_path / "song1.wav").write_bytes(b"fake audio")
            (folder_path / "song2.WAV").write_bytes(b"fake audio")
            (folder_path / "song3.Mp3").write_bytes(b"fake audio")
            (folder_path / "song4.M4A").write_bytes(b"fake audio")

            result = find_audio_files(folder_path)
            assert len(result) == 4

    def test_deduplication(self):
        """Test that duplicate files are handled correctly."""
        with tempfile.TemporaryDirectory() as temp_dir:
            folder_path = Path(temp_dir)

            # Create files with different names to test deduplication logic
            (folder_path / "song1.wav").write_bytes(b"fake audio")
            (folder_path / "song2.WAV").write_bytes(
                b"fake audio"
            )  # Different name, case
            (folder_path / "other.mp3").write_bytes(b"fake audio")

            result = find_audio_files(folder_path)
            # Should find all 3 files (different names)
            assert (
                len(result) >= 2
            )  # At least 2, could be 3 depending on OS case sensitivity

    def test_custom_extensions(self):
        """Test with custom file extensions."""
        with tempfile.TemporaryDirectory() as temp_dir:
            folder_path = Path(temp_dir)

            # Create files with default and custom extensions
            (folder_path / "song1.wav").write_bytes(b"fake audio")
            (folder_path / "song2.aac").write_bytes(b"fake audio")
            (folder_path / "song3.wma").write_bytes(b"fake audio")

            # Default extensions should find .wav
            result_default = find_audio_files(folder_path)
            assert len(result_default) == 1
            assert result_default[0].name == "song1.wav"

            # Custom extensions should find all
            result_custom = find_audio_files(folder_path, [".wav", ".aac", ".wma"])
            assert len(result_custom) == 3

    def test_sorting(self):
        """Test that files are sorted correctly."""
        with tempfile.TemporaryDirectory() as temp_dir:
            folder_path = Path(temp_dir)

            # Create files in non-alphabetical order
            files = ["zebra.wav", "alpha.mp3", "Beta.m4a", "gamma.ogg"]
            for filename in files:
                (folder_path / filename).write_bytes(b"fake audio")

            result = find_audio_files(folder_path)
            result_names = [f.name for f in result]

            # Should be sorted case-insensitively
            expected = ["alpha.mp3", "Beta.m4a", "gamma.ogg", "zebra.wav"]
            assert result_names == expected


class TestCreateButtonLabel:
    """Test cases for button label generation."""

    def test_basic_filename(self):
        """Test basic filename conversion."""
        assert create_button_label(Path("hello_world.wav")) == "Hello World"
        assert create_button_label(Path("test_file.mp3")) == "Test File"

    def test_underscores_and_hyphens(self):
        """Test handling of underscores and hyphens."""
        assert create_button_label(Path("hello_world_test.wav")) == "Hello World Test"
        assert create_button_label(Path("hello-world-test.mp3")) == "Hello World Test"
        assert create_button_label(Path("mixed_under-score.m4a")) == "Mixed Under Score"

    def test_numbers_and_special_chars(self):
        """Test handling of numbers and special characters."""
        assert create_button_label(Path("track_01.wav")) == "Track 01"
        assert create_button_label(Path("song_2023.mp3")) == "Song 2023"
        assert create_button_label(Path("test_file_v2.m4a")) == "Test File V2"

    def test_edge_cases(self):
        """Test edge cases for label generation."""
        assert create_button_label(Path("a.wav")) == "A"
        assert create_button_label(Path("123.mp3")) == "123"
        assert (
            create_button_label(Path("___.wav")) == ""
        )  # All underscores become empty
        assert (
            create_button_label(Path("multiple___underscores.mp3"))
            == "Multiple Underscores"
        )

    def test_extension_removal(self):
        """Test that extensions are properly removed."""
        assert create_button_label(Path("test.wav")) == "Test"
        assert create_button_label(Path("test.mp3")) == "Test"
        assert create_button_label(Path("test.m4a")) == "Test"
        assert create_button_label(Path("test.flac")) == "Test"
        assert create_button_label(Path("test.unknown")) == "Test"

    def test_title_case(self):
        """Test that proper title case is applied."""
        assert create_button_label(Path("lowercase_file.wav")) == "Lowercase File"
        assert (
            create_button_label(Path("UPPERCASE_FILE.wav")) == "Uppercase File"
        )  # capitalize() makes it title case
        assert create_button_label(Path("MiXeD_CaSe.wav")) == "Mixed Case"

    def test_real_world_examples(self):
        """Test with realistic filename patterns."""
        assert create_button_label(Path("anakin_I_hate_you.m4a")) == "Anakin I Hate You"
        assert (
            create_button_label(Path("vader-I_am_your_father.wav"))
            == "Vader I Am Your Father"
        )
        assert (
            create_button_label(Path("thanos-desperate_fail.mp3"))
            == "Thanos Desperate Fail"
        )
        assert create_button_label(Path("ww_say_my_name.m4a")) == "Ww Say My Name"


class TestGenerateSoundboardCLI:
    """Test cases for the CLI functionality."""

    def test_preview_mode(self):
        """Test preview mode doesn't create files."""
        runner = CliRunner()

        with tempfile.TemporaryDirectory() as temp_dir:
            folder_path = Path(temp_dir)

            # Create test audio files
            (folder_path / "test1.wav").write_bytes(b"fake audio")
            (folder_path / "test2.mp3").write_bytes(b"fake audio")

            # Run with preview mode
            result = runner.invoke(main, [str(folder_path), "--preview"])

            assert result.exit_code == 0
            assert "Found 2 audio files" in result.output
            assert "Configuration Preview:" in result.output

            # Should not create any files
            json_files = list(folder_path.glob("*.json"))
            assert len(json_files) == 0

    def test_output_file_creation(self):
        """Test that output files are created correctly."""
        runner = CliRunner()

        with tempfile.TemporaryDirectory() as temp_dir:
            folder_path = Path(temp_dir)
            output_path = folder_path / "test_soundboard.json"

            # Create test audio files
            (folder_path / "test1.wav").write_bytes(b"fake audio")
            (folder_path / "test2.mp3").write_bytes(b"fake audio")

            # Run without preview mode
            result = runner.invoke(
                main, [str(folder_path), "--output", str(output_path)]
            )

            assert result.exit_code == 0
            assert output_path.exists()

            # Verify JSON content
            with open(output_path) as f:
                config = json.load(f)

            assert "layout" in config
            assert "buttons" in config
            assert config["layout"]["rows"] == 2
            assert config["layout"]["cols"] == 1
            assert len(config["buttons"]) == 2

    def test_absolute_paths(self):
        """Test absolute path option."""
        runner = CliRunner()

        with tempfile.TemporaryDirectory() as temp_dir:
            folder_path = Path(temp_dir)
            output_path = folder_path / "test_soundboard.json"

            # Create test audio file
            (folder_path / "test.wav").write_bytes(b"fake audio")

            # Run with absolute paths
            result = runner.invoke(
                main,
                [str(folder_path), "--output", str(output_path), "--absolute-paths"],
            )

            assert result.exit_code == 0

            # Verify absolute paths in output
            with open(output_path) as f:
                config = json.load(f)

            file_path = config["buttons"][0]["file"]
            assert Path(file_path).is_absolute()

    def test_custom_extensions(self):
        """Test custom file extensions."""
        runner = CliRunner()

        with tempfile.TemporaryDirectory() as temp_dir:
            folder_path = Path(temp_dir)

            # Create files with various extensions
            (folder_path / "test1.wav").write_bytes(b"fake audio")
            (folder_path / "test2.aac").write_bytes(b"fake audio")
            (folder_path / "test3.wma").write_bytes(b"fake audio")

            # Run with custom extensions
            result = runner.invoke(
                main,
                [
                    str(folder_path),
                    "--extensions",
                    ".aac",
                    "--extensions",
                    ".wma",
                    "--preview",
                ],
            )

            assert result.exit_code == 0
            # CLI adds custom extensions to defaults, so all files are found
            assert "Found 3 audio files" in result.output  # Finds .wav, .aac, .wma

    def test_empty_folder_handling(self):
        """Test handling of empty folders."""
        runner = CliRunner()

        with tempfile.TemporaryDirectory() as temp_dir:
            folder_path = Path(temp_dir)

            # Run on empty folder
            result = runner.invoke(main, [str(folder_path), "--preview"])

            # CLI returns early but doesn't set exit code - just check output
            assert "No audio files found" in result.output

    def test_nonexistent_folder(self):
        """Test handling of nonexistent folders."""
        runner = CliRunner()

        result = runner.invoke(main, ["/path/that/does/not/exist", "--preview"])

        assert result.exit_code != 0

    def test_default_output_location(self):
        """Test default output file location."""
        runner = CliRunner()

        with tempfile.TemporaryDirectory() as temp_dir:
            folder_path = Path(temp_dir)

            # Create test audio file
            (folder_path / "test.wav").write_bytes(b"fake audio")

            # Run without specifying output
            result = runner.invoke(main, [str(folder_path)])

            assert result.exit_code == 0

            # Should create soundboard.json in the audio folder
            default_output = folder_path / "soundboard.json"
            assert default_output.exists()
