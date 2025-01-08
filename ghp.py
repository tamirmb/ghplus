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

CONFIG_DIR = Path.home() / '.ghp'
CONFIG_FILE = CONFIG_DIR / 'config'

def save_config(token: str, org: str):
    """Save GitHub token and organization to config file."""
    CONFIG_DIR.mkdir(exist_ok=True, mode=0o700)
    config = {'github_token': token, 'github_org': org}
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

def get_org():
    """Get GitHub organization from config file or environment."""
    org = os.getenv('GITHUB_ORG')
    if org:
        return org
    
    if CONFIG_FILE.exists():
        config = json.loads(CONFIG_FILE.read_text())
        return config.get('github_org')
    return None

def summarize_permissions(permissions):
    """
    Convert GitHub's permission object into a simple permission level string.
    """
    if permissions.admin:
        return 'admin'
    if permissions.maintain:
        return 'maintain'
    if permissions.push:
        return 'write'
    if permissions.triage:
        return 'triage'
    if permissions.pull:
        return 'read'
    return 'none'

def list_users_in_repo(repo_name: str):
  """List all users in a GitHub repository."""
  token = get_token()
  org = get_org()

  if not token:
    print("Error: GitHub token not configured")
    print("Please run: ghp configure")
    sys.exit(1)

  try:
    g = Github(token)
    target = g.get_organization(org) if org else g.get_user()
    repo = target.get_repo(repo_name)
    users = repo.get_collaborators()
    print(f"Users in {repo_name}:")
    for user in users:
        permission_level = summarize_permissions(user.permissions)
        print(f"  - {user.login} ({user.type}) [{permission_level}]")
  except GithubException as e:
    if e.status == 404:
      print(f"Error: Repository '{repo_name}' not found or you don't have access to it")
    elif e.status == 401:
      print("Error: Invalid GitHub token")
    else:
      print(f"Error: {e.data.get('message', str(e))}")
    sys.exit(1)

def add_user_to_repo(repo_name: str, username: str, permission: str):
  """Add a user as a collaborator to a GitHub repository."""
  token = get_token()
  org = get_org()

  if not token:
      print("Error: GitHub token not configured")
      print("Please run: ghp configure")
      sys.exit(1)

  try:
    g = Github(token)
    target = g.get_organization(org) if org else g.get_user()
    repo = target.get_repo(repo_name)
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

def remove_user_from_repo(repo_name: str, username: str):
  """Remove a user from a GitHub repository."""
  token = get_token()
  org = get_org()

  if not token:
    print("Error: GitHub token not configured")
    print("Please run: ghp configure")
    sys.exit(1)
  
  try:
    g = Github(token)
    target = g.get_organization(org) if org else g.get_user()
    repo = target.get_repo(repo_name)
    repo.remove_from_collaborators(username)
    print(f"✓ Successfully removed {username} from {repo_name}")
  except GithubException as e:
    if e.status == 404:
      print(f"Error: Repository '{repo_name}' not found or you don't have access to it")
    elif e.status == 401:
      print("Error: Invalid GitHub token")
    else:
      print(f"Error: {e.data.get('message', str(e))}")
    sys.exit(1)

def add_secret_to_repo(repo_name: str, secret_name: str = None, secret_value: str = None):
    """Add a secret to a GitHub repository."""
    token = get_token()
    org = get_org()

    if not token:
        print("Error: GitHub token not configured")
        print("Please run: ghp configure")
        sys.exit(1)

    # Prompt for secret name if not provided
    if not secret_name:
        secret_name = input("Enter secret name: ").strip()
        if not secret_name:
            print("Error: Secret name cannot be empty")
            sys.exit(1)

    # Prompt for secret value if not provided, using getpass to hide input
    if not secret_value:
        secret_value = getpass(f"Enter value for secret '{secret_name}': ").strip()
        if not secret_value:
            print("Error: Secret value cannot be empty")
            sys.exit(1)
        
        # Show masked preview
        visible_chars = len(secret_value) // 4  # Show last 25% of characters
        masked_value = '*' * (len(secret_value) - visible_chars) + secret_value[-visible_chars:]
        confirm = input(f"\nAdd secret '{secret_name}' with value '{masked_value}'? [y/N] ").lower()
        if confirm != 'y':
            print("Cancelled")
            sys.exit(0)

    try:
        g = Github(token)
        org_obj = g.get_organization(org)
        repo = org_obj.get_repo(repo_name)
        
        repo.create_secret(secret_name, secret_value)
        print(f"✓ Successfully added secret '{secret_name}' to {repo_name}")

    except GithubException as e:
        if e.status == 404:
            print(f"Error: Repository '{repo_name}' not found or you don't have access to it")
        elif e.status == 401:
            print("Error: Invalid GitHub token")
        else:
            print(f"Error: {e.data.get('message', str(e))}")
        sys.exit(1)


def list_org_secrets():
    """List all organization secrets."""
    token = get_token()
    org = get_org()

    if not token:
        print("Error: GitHub token not configured")
        print("Please run: ghp configure")
        sys.exit(1)

    try:
        g = Github(token)
        org_obj = g.get_organization(org)
        secrets = org_obj.get_secrets()
        print(f"\nSecrets for {org}:")
        
        for secret in secrets:
            print(f"  • {secret.name}")
            
    except GithubException as e:
        if e.status == 404:
            print(f"Error: Organization '{org}' not found or you don't have access to it")
        elif e.status == 401:
            print("Error: Invalid GitHub token")
        else:
            print(f"Error: {e.data.get('message', str(e))}")
        sys.exit(1)
  

def main():
    parser = argparse.ArgumentParser(
      description='Configure your GitHub settings through the CLI',
      usage='ghp <command> <subcommand> [flags]'
    )
    
    subparsers = parser.add_subparsers(dest='command')

    # Configure command
    configure_parser = subparsers.add_parser('configure', help='Configure GitHub credentials')
    configure_parser.add_argument('--token', help='GitHub Personal Access Token')
    configure_parser.add_argument('--org', help='GitHub Organization')

    # Repository command
    repo_parser = subparsers.add_parser('repo', help='Manage repositories')
    repo_parser.add_argument('repo_name', metavar='<repo_name>', help='name of the repository')
    repo_subparsers = repo_parser.add_subparsers(dest='repo_command')
    userls_parser = repo_subparsers.add_parser('userls', help='List users in the repository')

    # Remove user command
    rmuser_parser = repo_subparsers.add_parser('rmuser', help='Remove a user from the repository')
    rmuser_parser.add_argument('username', metavar='<username>', help='username to remove')

    # Add user command
    adduser_parser = repo_subparsers.add_parser('adduser', help='Add a user to the repository')
    adduser_parser.add_argument('username', metavar='<username>', help='username to add')
    adduser_parser.add_argument('permission', 
      choices=['read', 'write', 'admin'],
      help='permission level for the user'
    )

    # List secrets command
    # Secrets command
    secrets_parser = subparsers.add_parser('secrets', help='Manage organization secrets')
    secrets_subparsers = secrets_parser.add_subparsers(dest='secrets_command')
    secrets_ls_parser = secrets_subparsers.add_parser('ls', help='List organization secrets')

    # Add secret command
    addsecret_parser = repo_subparsers.add_parser('addsecret', help='Add a secret to the repository')
    addsecret_parser.add_argument('--name', help='Name of the secret')
    addsecret_parser.add_argument('--value', help='Value of the secret (not recommended, use interactive prompt instead)')

    args = parser.parse_args()

    if not args.command:
      parser.print_help()
      return

    if args.command == 'configure':
      token = args.token or getpass("Enter your GitHub Personal Access Token: ").strip()
      org = args.org or input("Enter your GitHub Organization: ").strip()

      if token:
        try:
          g = Github(token)
          g.get_user().login
        except GithubException:
          print("Error: Invalid GitHub token")
          sys.exit(1)
      else:
        print("Error: Token cannot be empty")
        sys.exit(1)

      if org:
        try:    
          g = Github(token)
          g.get_organization(org)
        except GithubException:
          print("Error: Invalid GitHub organization")
          sys.exit(1)

      save_config(token, org)
    
    elif args.command == 'repo' and args.repo_command == 'adduser':
      add_user_to_repo(args.repo_name, args.username, args.permission)
    elif args.command == 'repo' and args.repo_command == 'rmuser':
      remove_user_from_repo(args.repo_name, args.username)
    elif args.command == 'repo' and args.repo_command == 'userls':
      list_users_in_repo(args.repo_name)
    elif args.command == 'repo' and args.repo_command == 'addsecret':
      add_secret_to_repo(args.repo_name, args.name, args.value)
    elif args.command == 'secrets' and args.secrets_command == 'ls':
      list_org_secrets()
    else:
      repo_parser.print_help()

if __name__ == "__main__":
  main()
