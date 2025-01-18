#!/usr/bin/env python3
import os
import sys

# Add the parent directory to sys.path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.implementations.config.json_config import JsonConfig
from src.implementations.settings.repo import RepoSettings


def main():
    config = JsonConfig()
    repo_settings = RepoSettings(config)


if __name__ == "__main__":
    main()
