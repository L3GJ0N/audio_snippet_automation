"""Test utilities and mock data for audio snippet automation tests."""

import tempfile
from pathlib import Path
from unittest.mock import Mock, patch


class MockYoutubeDL:
    """Mock YouTube-DL for testing without actual downloads."""

    def __init__(self, *args, **kwargs):
        self.downloaded_files = {}

    def download(self, urls):
        """Mock download that creates fake files."""
        for url in urls:
            # Simulate successful download
            video_id = self.extract_video_id(url)
            filename = f"{video_id}.m4a"

            # Create a fake audio file
            fake_content = b"fake audio content for testing"
            temp_file = Path(tempfile.gettempdir()) / filename
            temp_file.write_bytes(fake_content)

            self.downloaded_files[url] = str(temp_file)

        return True

    def extract_video_id(self, url):
        """Extract video ID from YouTube URL."""
        if "watch?v=" in url:
            return url.split("watch?v=")[1].split("&")[0]
        elif "youtu.be/" in url:
            return url.split("youtu.be/")[1].split("?")[0]
        else:
            return "mock_video_id"


class MockFFmpeg:
    """Mock FFmpeg for testing without actual audio processing."""

    @staticmethod
    def run_command(cmd, *args, **kwargs):
        """Mock FFmpeg command execution."""
        # Extract output filename from command
        if "-i" in cmd and any(cmd[i : i + 2] == ["-i"] for i in range(len(cmd) - 1)):
            # Find output file (last argument typically)
            output_file = cmd[-1]

            # Create fake output file
            if isinstance(output_file, str):
                output_path = Path(output_file)
                output_path.parent.mkdir(parents=True, exist_ok=True)

                # Create different content based on format
                if output_file.endswith(".wav"):
                    fake_content = b"WAVE fake audio data for testing"
                elif output_file.endswith(".mp3"):
                    fake_content = b"MP3 fake audio data for testing"
                else:
                    fake_content = b"M4A fake audio data for testing"

                output_path.write_bytes(fake_content)

        return Mock(returncode=0, stdout="", stderr="")


def create_mock_audio_file(file_path, format="wav"):
    """Create a mock audio file for testing."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if format.lower() == "wav":
        # Minimal WAV header + data
        content = (
            b"RIFF\x24\x08\x00\x00WAVEfmt \x10\x00\x00\x00"
            b"\x01\x00\x02\x00\x44\xac\x00\x00\x10\xb1\x02\x00"
            b"\x04\x00\x10\x00data\x00\x08\x00\x00"
            b"\x00\x00\x00\x00" * 100  # Fake audio data
        )
    elif format.lower() == "mp3":
        # MP3 header
        content = b"\xff\xfb\x90\x00" + b"\x00" * 1000  # MP3 header  # Fake MP3 data
    else:  # m4a
        # Basic M4A/MP4 header
        content = (
            b"\x00\x00\x00\x20ftypM4A \x00\x00\x02\x00"
            b"M4A isomiso2\x00\x00\x00\x08free"
            b"\x00" * 1000  # Fake audio data
        )

    path.write_bytes(content)
    return path


def mock_youtube_download():
    """Decorator to mock YouTube downloads in tests."""

    def decorator(func):
        def wrapper(*args, **kwargs):
            with patch("subprocess.run") as mock_run:
                # Mock yt-dlp calls
                def side_effect(cmd, *args, **kwargs):
                    if "yt-dlp" in cmd:
                        if "--get-id" in cmd:
                            # Return fake video ID
                            return Mock(
                                returncode=0, stdout="mock_video_id\n", stderr=""
                            )
                        else:
                            # Mock download - create fake file
                            url = None
                            for _i, arg in enumerate(cmd):
                                if arg.startswith("http"):
                                    url = arg
                                    break

                            if url:
                                video_id = MockYoutubeDL().extract_video_id(url)
                                fake_file = Path("downloads") / f"{video_id}.m4a"
                                create_mock_audio_file(fake_file, "m4a")

                            return Mock(returncode=0, stdout="", stderr="")

                    elif "ffmpeg" in cmd:
                        # Mock FFmpeg calls
                        return MockFFmpeg.run_command(cmd, *args, **kwargs)

                    else:
                        # Default mock for other commands
                        return Mock(returncode=0, stdout="", stderr="")

                mock_run.side_effect = side_effect
                return func(*args, **kwargs)

        return wrapper

    return decorator


def cleanup_mock_files():
    """Clean up mock files created during testing."""
    import shutil

    # Common test directories to clean up
    test_dirs = ["downloads", "test_output", "snippets"]

    for dir_name in test_dirs:
        test_dir = Path(dir_name)
        if test_dir.exists():
            shutil.rmtree(test_dir)

    # Clean up temp files
    temp_dir = Path(tempfile.gettempdir())
    for pattern in ["*.m4a", "*.wav", "*.mp3"]:
        for file in temp_dir.glob(pattern):
            if file.name.startswith("mock_") or "test" in file.name.lower():
                try:
                    file.unlink()
                except OSError:
                    pass  # File might be in use


# Test configuration constants
SAMPLE_CSV_CONTENT = """url,start,end,output,format
https://www.youtube.com/watch?v=test1,0,10,test_clip_1,m4a
https://www.youtube.com/watch?v=test2,5,15,test_clip_2,wav
https://www.youtube.com/watch?v=test3,10,20,test_clip_3,mp3
"""

SAMPLE_SOUNDBOARD_CONFIG = {
    "layout": {"rows": 2, "cols": 3},
    "buttons": [
        {
            "file": "test_clip_1.wav",
            "row": 1,
            "col": 1,
            "label": "Test Clip 1",
        },
        {
            "file": "test_clip_2.wav",
            "row": 1,
            "col": 2,
            "label": "Test Clip 2",
        },
        {
            "file": "test_clip_3.wav",
            "row": 2,
            "col": 1,
            "label": "Test Clip 3",
        },
    ],
}
