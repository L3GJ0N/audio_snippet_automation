"""
Virtual DJ Soundboard - A customizable grid-based audio playback interface.

This module provides a web-based soundboard interface where users can:
- Define custom button layouts via JSON configuration
- Play audio snippets by clicking buttons
- Handle multiple simultaneous audio playback
- Cross-platform support (Windows/Mac/Linux)
"""

import json
import logging
from pathlib import Path

import pygame
from flask import Flask, jsonify, render_template

logger = logging.getLogger(__name__)


class AudioSnippetError(Exception):
    """Custom exception for audio snippet related errors."""

    pass


class SoundboardConfig:
    """Handles loading and validation of soundboard configuration."""

    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.layout: tuple[int, int] = (0, 0)  # (rows, cols)
        self.buttons: list[dict] = []
        self._load_config()

    def _load_config(self) -> None:
        """Load and validate the JSON configuration file."""
        try:
            with open(self.config_path, encoding="utf-8") as f:
                config = json.load(f)
        except FileNotFoundError:
            raise AudioSnippetError(
                f"Configuration file not found: {self.config_path}"
            ) from None
        except json.JSONDecodeError as e:
            raise AudioSnippetError(f"Invalid JSON in configuration file: {e}") from e

        # Validate layout
        layout = config.get("layout", {})
        rows = layout.get("rows", 0)
        cols = layout.get("cols", 0)

        if (
            not isinstance(rows, int)
            or not isinstance(cols, int)
            or rows <= 0
            or cols <= 0
        ):
            raise AudioSnippetError(
                "Layout must specify positive integer values for 'rows' and 'cols'"
            )

        self.layout = (rows, cols)

        # Validate buttons
        buttons = config.get("buttons", [])
        if not isinstance(buttons, list):
            raise AudioSnippetError("'buttons' must be a list")

        for i, button in enumerate(buttons):
            self._validate_button(button, i)

        self.buttons = buttons

    def _validate_button(self, button: dict, index: int) -> None:
        """Validate a single button configuration."""
        required_fields = ["file", "row", "col"]
        for field in required_fields:
            if field not in button:
                raise AudioSnippetError(
                    f"Button {index}: missing required field '{field}'"
                )

        # Validate file path
        file_path = Path(button["file"])
        if not file_path.exists():
            raise AudioSnippetError(
                f"Button {index}: audio file not found: {file_path}"
            )

        # Validate position
        row, col = button["row"], button["col"]
        max_row, max_col = self.layout

        if not (1 <= row <= max_row and 1 <= col <= max_col):
            raise AudioSnippetError(
                f"Button {index}: position ({row}, {col}) is outside layout bounds "
                f"({max_row}x{max_col})"
            )


class AudioPlayer:
    """Handles audio playback using pygame mixer."""

    def __init__(self):
        self._initialized = False
        self._channels: dict[str, pygame.mixer.Channel] = {}
        self._sounds: dict[str, pygame.mixer.Sound] = {}
        self._init_pygame()

    def _init_pygame(self) -> None:
        """Initialize pygame mixer for audio playback."""
        try:
            pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
            pygame.mixer.init()
            # Set number of channels for simultaneous playback
            pygame.mixer.set_num_channels(32)
            self._initialized = True
            logger.info("Audio player initialized successfully")
        except pygame.error as e:
            raise AudioSnippetError(f"Failed to initialize audio player: {e}") from e

    def load_sound(self, file_path: Path, button_id: str) -> None:
        """Load an audio file for a specific button."""
        if not self._initialized:
            raise AudioSnippetError("Audio player not initialized")

        try:
            sound = pygame.mixer.Sound(str(file_path))
            self._sounds[button_id] = sound
            logger.debug(f"Loaded sound for button {button_id}: {file_path}")
        except pygame.error as e:
            # Check if it's a format issue
            file_ext = file_path.suffix.lower()
            if file_ext in [".m4a", ".aac", ".flac"]:
                raise AudioSnippetError(
                    f"Unsupported audio format {file_ext} for file {file_path}. "
                    f"Please convert to WAV, MP3, or OGG format. "
                    f'You can use: ffmpeg -i "{file_path}" "{file_path.with_suffix(".wav")}"'
                ) from e
            else:
                raise AudioSnippetError(
                    f"Failed to load audio file {file_path}: {e}"
                ) from e

    def play_sound(self, button_id: str) -> bool:
        """Play sound for a specific button. Returns True if successful."""
        if button_id not in self._sounds:
            logger.warning(f"Sound not loaded for button {button_id}")
            return False

        try:
            # Stop previous instance of this sound if still playing
            if button_id in self._channels and self._channels[button_id].get_busy():
                self._channels[button_id].stop()

            # Play the sound
            channel = self._sounds[button_id].play()
            if channel:
                self._channels[button_id] = channel
                logger.debug(f"Playing sound for button {button_id}")
                return True
            else:
                logger.warning(f"No available channel for button {button_id}")
                return False
        except pygame.error as e:
            logger.error(f"Failed to play sound for button {button_id}: {e}")
            return False

    def stop_sound(self, button_id: str) -> bool:
        """Stop sound for a specific button. Returns True if successful."""
        if button_id in self._channels and self._channels[button_id].get_busy():
            self._channels[button_id].stop()
            logger.debug(f"Stopped sound for button {button_id}")
            return True
        return False

    def stop_all_sounds(self) -> None:
        """Stop all currently playing sounds."""
        pygame.mixer.stop()
        logger.debug("Stopped all sounds")

    def cleanup(self) -> None:
        """Clean up pygame mixer resources."""
        if self._initialized:
            pygame.mixer.quit()
            logger.info("Audio player cleaned up")


class VirtualDJSoundboard:
    """Main soundboard application using Flask web server."""

    def __init__(self, config_path: Path, host: str = "localhost", port: int = 8080):
        self.config = SoundboardConfig(config_path)
        self.audio_player = AudioPlayer()
        self.host = host
        self.port = port

        # Create Flask app
        self.app = Flask(__name__, template_folder=self._get_template_dir())
        self._setup_routes()
        self._load_sounds()

    def _get_template_dir(self) -> str:
        """Get the template directory path."""
        return str(Path(__file__).parent / "templates")

    def _setup_routes(self) -> None:
        """Setup Flask routes for the web interface."""

        @self.app.route("/")
        def index():
            """Serve the main soundboard interface."""
            return render_template(
                "soundboard.html",
                layout=self.config.layout,
                buttons=self.config.buttons,
            )

        @self.app.route("/api/play/<button_id>", methods=["POST"])
        def play_sound(button_id: str):
            """API endpoint to play a sound."""
            success = self.audio_player.play_sound(button_id)
            return jsonify({"success": success})

        @self.app.route("/api/stop/<button_id>", methods=["POST"])
        def stop_sound(button_id: str):
            """API endpoint to stop a sound."""
            success = self.audio_player.stop_sound(button_id)
            return jsonify({"success": success})

        @self.app.route("/api/stop-all", methods=["POST"])
        def stop_all_sounds():
            """API endpoint to stop all sounds."""
            self.audio_player.stop_all_sounds()
            return jsonify({"success": True})

        @self.app.route("/api/config")
        def get_config():
            """API endpoint to get current configuration."""
            return jsonify(
                {
                    "layout": {
                        "rows": self.config.layout[0],
                        "cols": self.config.layout[1],
                    },
                    "buttons": self.config.buttons,
                }
            )

    def _load_sounds(self) -> None:
        """Load all audio files specified in the configuration."""
        for i, button in enumerate(self.config.buttons):
            button_id = f"btn_{button['row']}_{button['col']}"
            file_path = Path(button["file"])

            try:
                self.audio_player.load_sound(file_path, button_id)
                # Add button_id to button config for frontend use
                button["id"] = button_id
            except AudioSnippetError as e:
                logger.error(f"Failed to load sound for button {i}: {e}")
                # Remove button from config if sound can't be loaded
                continue

    def run(self, debug: bool = False) -> None:
        """Start the Flask web server."""
        try:
            logger.info(
                f"Starting Virtual DJ Soundboard on http://{self.host}:{self.port}"
            )
            logger.info(
                f"Layout: {self.config.layout[0]}x{self.config.layout[1]} ({len(self.config.buttons)} buttons)"
            )

            self.app.run(host=self.host, port=self.port, debug=debug, threaded=True)
        except KeyboardInterrupt:
            logger.info("Shutting down soundboard...")
        finally:
            self.audio_player.cleanup()


def create_example_config(output_path: Path) -> None:
    """Create an example configuration file."""
    example_config = {
        "layout": {"rows": 4, "cols": 6},
        "buttons": [
            {
                "file": "snippets/example_clip_1.m4a",
                "row": 1,
                "col": 1,
                "label": "Example Sound 1",
            },
            {
                "file": "snippets/example_clip_2.wav",
                "row": 1,
                "col": 2,
                "label": "Example Sound 2",
            },
            {
                "file": "snippets/my_audio_snippet.m4a",
                "row": 1,
                "col": 3,
                "label": "My Custom Audio",
            },
            {
                "file": "C:/path/to/your/audio/file.wav",
                "row": 2,
                "col": 1,
                "label": "Absolute Path Example",
            },
            {
                "file": "./relative/path/to/audio.mp3",
                "row": 2,
                "col": 2,
                "label": "Relative Path Example",
            },
            {
                "file": "snippets/generated_by_asa.m4a",
                "row": 2,
                "col": 3,
                "label": "Generated Snippet",
            },
        ],
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(example_config, f, indent=2)

    print(f"Example configuration created: {output_path}")
