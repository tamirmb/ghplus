#!/usr/bin/env python3
import os
import sys
import argparse

# Add the parent directory to sys.path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.implementations.config.json_config import JsonConfig
from src.implementations.settings.repo import RepoSettings
from src.interfaces.repo_settings import Permission


def create_parser():
    parser = argparse.ArgumentParser()

    main_subparser = parser.add_subparsers(dest="command")

    repo_parser = main_subparser.add_parser("repo", help="Repository operations")
    repo_parser.add_argument("repo", help="Repository name")

    repo_subparser = repo_parser.add_subparsers(dest="repo_command")

    adduser_parser = repo_subparser.add_parser(
        "adduser", help="Add a user to a repository"
    )
    adduser_parser.add_argument("username", help="Username to add")
    adduser_parser.add_argument(
        "permissions",
        choices=["read", "write", "admin"],
        help="Permission level: read, write, or admin",
    )

    deluser_parser = repo_subparser.add_parser(
        "deluser", help="Delete a user from a repository"
    )
    deluser_parser.add_argument("username", help="Username to remove")

    repo_subparser.add_parser("users", help="List users in a repository")

    return parser


def main():
    config = JsonConfig()
    repo_settings = RepoSettings(config)

    parser = create_parser()
    args = parser.parse_args()

    if args.command == "repo" and args.repo_command:
        if args.repo_command == "adduser":
            permission = Permission(args.permissions)
            repo_settings.useradd(args.repo, args.username, permission)
        elif args.repo_command == "deluser":
            repo_settings.deluser(args.repo, args.username)
        elif args.repo_command == "users":
            repo_settings.users(args.repo)


if __name__ == "__main__":
    main()
