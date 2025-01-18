import sys
import json
from pathlib import Path
from src.interfaces.config import ConfigInterface


class JsonConfig(ConfigInterface):
    def __init__(self, filename="config.json"):
        # Create config directory in user's home directory
        self.config_dir = Path.home() / ".ghp"
        self.file_path = self.config_dir / filename

        # Create config directory if it doesn't exist
        self.config_dir.mkdir(exist_ok=True)

        # Initialize empty config if file doesn't exist
        if not self.file_path.exists():
            self.config = {}
            self.save()  # Create the file with empty config
        else:
            self.config = self.load()

    def load(self):
        """Load configuration from file."""
        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save(self):
        """Save configuration to file."""
        with open(self.file_path, "w") as file:
            json.dump(self.config, file, indent=2)

    def get(self, key, default=None):
        """Get a value from configuration."""
        return self.config.get(key, default)

    def set(self, key, value):
        """Set a value in configuration."""
        self.config[key] = value

    def check(self):
        """Check if the config is configured with required values"""
        if not self.config.get("token"):
            print("Error: GitHub token not configured")
            print("Please run: ghp configure")
            sys.exit(1)
