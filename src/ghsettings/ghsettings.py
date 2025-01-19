#!/usr/bin/env python3
import argparse
from ghsettings.implementations.config.json_config import JsonConfig
from ghsettings.implementations.settings.repo import RepoSettings
from ghsettings.interfaces.repo_settings import Permission


def create_parser():
    parser = argparse.ArgumentParser(
        description="Configure GitHub settings through the CLI", prog="ghsettings"
    )

    main_subparser = parser.add_subparsers(dest="command")

    configure_parser = main_subparser.add_parser(
        "configure", help="Edit your configuration file"
    )

    repo_parser = main_subparser.add_parser("repo", help="Repository settings")
    repo_parser.add_argument("repository", help="Repository name")

    repo_subparser = repo_parser.add_subparsers(dest="repo_command")

    adduser_parser = repo_subparser.add_parser(
        "adduser", help="Add user to a repository"
    )
    adduser_parser.add_argument("username", help="Username to add")
    adduser_parser.add_argument(
        "permissions",
        choices=["read", "write", "admin"],
        help="Permission level: read, write, or admin",
    )

    deluser_parser = repo_subparser.add_parser(
        "deluser", help="Delete user from a repository"
    )
    deluser_parser.add_argument("username", help="Username to remove")

    repo_subparser.add_parser("users", help="List users in a repository")

    return parser


def main():
    config = JsonConfig()
    parser = create_parser()
    args = parser.parse_args()

    if args.command == "configure":
        config.configure()

    elif args.command == "repo" and args.repo_command:
        repo_settings = RepoSettings(config)
        if args.repo_command == "adduser":
            permission = Permission(args.permissions)
            repo_settings.useradd(args.repo, args.username, permission)
        elif args.repo_command == "deluser":
            repo_settings.deluser(args.repo, args.username)
        elif args.repo_command == "users":
            repo_settings.users(args.repo)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
