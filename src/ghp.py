#!/usr/bin/env python3
import argparse
import os
import sys
import json
import signal
from pathlib import Path
from getpass import getpass
from github import Github
from github.GithubException import GithubException

from src.interfaces.repo_settings import Permission

# Add the parent directory to sys.path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.implementations.config.json_config import JsonConfig
from src.implementations.settings.repo import RepoSettings


def main():
    config = JsonConfig()
    repo_settings = RepoSettings(config)
    repo_settings.useradd("ghplus", "tmelzerb-hss", Permission.READ)
    repo_settings.users("ghplus")


if __name__ == "__main__":
    main()
