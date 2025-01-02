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

# Handle Ctrl+C gracefully
def signal_handler(sig, frame):
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

CONFIG_DIR = Path.home() / '.ghplus'
CONFIG_FILE = CONFIG_DIR / 'config'

def save_config(token: str):
    """Save GitHub token to config file."""
    CONFIG_DIR.mkdir(exist_ok=True, mode=0o700)
    config = {'github_token': token}
    CONFIG_FILE.write_text(json.dumps(config))
    CONFIG_FILE.chmod(0o600)
    print("✓ Configuration saved successfully")

def get_token():
    """Get GitHub token from config file or environment."""
    token = os.getenv('GITHUB_TOKEN')
    if token:
        return token
        
    if CONFIG_FILE.exists():
        try:
            config = json.loads(CONFIG_FILE.read_text())
            return config.get('github_token')
        except (json.JSONDecodeError, KeyError):
            return None
    return None

def add_user_to_repo(repo_name: str, username: str, permission: str):
    """Add a user as a collaborator to a GitHub repository."""
    token = get_token()
    if not token:
        print("Error: GitHub token not configured")
        print("Please run: ghplus configure")
        sys.exit(1)

    try:
        g = Github(token)
        user = g.get_user()
        repo = user.get_repo(repo_name)
        repo.add_to_collaborators(username, permission)
        print(f"✓ Successfully added {username} to {repo_name} with {permission} permissions")
    except GithubException as e:
        if e.status == 404:
            print(f"Error: Repository '{repo_name}' not found or you don't have access to it")
        elif e.status == 401:
            print("Error: Invalid GitHub token")
        else:
            print(f"Error: {e.data.get('message', str(e))}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description='interact with github through the cli!',
        usage='ghplus <command> <subcommand> [flags]'
    )
    
    subparsers = parser.add_subparsers(dest='command')

    # Configure command
    configure_parser = subparsers.add_parser('configure', help='Configure GitHub credentials')
    configure_parser.add_argument('--token', help='GitHub Personal Access Token')

    # Repository command
    repo_parser = subparsers.add_parser('repo', help='Manage repositories')
    repo_parser.add_argument('repo_name', metavar='<repo_name>', help='name of the repository')
    repo_subparsers = repo_parser.add_subparsers(dest='repo_command')

    # Add user command
    adduser_parser = repo_subparsers.add_parser('adduser', help='Add a user to the repository')
    adduser_parser.add_argument('username', metavar='<username>', help='username to add')
    adduser_parser.add_argument('permission', 
        choices=['read', 'write', 'admin'],
        help='permission level for the user'
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == 'configure':
        token = args.token or getpass("Enter your GitHub Personal Access Token: ").strip()
        if token:
            try:
                g = Github(token)
                g.get_user().login
                save_config(token)
            except GithubException:
                print("Error: Invalid GitHub token")
                sys.exit(1)
        else:
            print("Error: Token cannot be empty")
            sys.exit(1)
    
    elif args.command == 'repo' and args.repo_command == 'adduser':
        add_user_to_repo(args.repo_name, args.username, args.permission)
    
    else:
        repo_parser.print_help()

if __name__ == "__main__":
    main()
