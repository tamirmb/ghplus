import sys
from halo import Halo
from github import Github, GithubIntegration, Auth
from github.GithubException import GithubException
from ...interfaces.config import ConfigInterface
from ...interfaces.repo_settings import RepoSettingsInterface, Permission


class RepoSettings(RepoSettingsInterface):
    def __init__(self, config: ConfigInterface):
        self.config = config
        self.token = config.get("token")
        self.user = config.get("user")
        self.gh = Github(auth=Auth.Token(self.token))

    def useradd(self, repo: str, user: str, permission: Permission) -> None:
        """Add a user to a repository with a given permission level"""
        try:
            repository = self.gh.get_repo(f"{self.user}/{repo}")
            repository.add_to_collaborators(user, permission.value)
            print(f"✓ Added {user} [{permission.value}] to {self.user}/{repo}")
        except GithubException as e:
            print(f"Error accessing repository: {e.data.get('message', str(e))}")
            sys.exit(1)
        finally:
            self.gh.close()

    def deluser(self, repo: str, user: str) -> None:
        """Remove a user from a repository"""
        try:
            repository = self.gh.get_repo(f"{self.user}/{repo}")
            repository.remove_from_collaborators(user)
            print(f"✓ Removed {user} from {self.user}/{repo}")

        except GithubException as e:
            print(f"Error accessing repository: {e.data.get('message', str(e))}")
            sys.exit(1)
        finally:
            self.gh.close()

    def users(self, repo: str) -> None:
        """List all users in a repository"""
        try:
            spinner = Halo(text="Fetching users...", spinner="dots")
            spinner.start()

            repository = self.gh.get_repo(f"{self.user}/{repo}")
            users = repository.get_collaborators()
            user_and_perms = []

            for user in users:
                perm = repository.get_collaborator_permission(user)
                user_and_perms.append((user.login, perm))

            spinner.stop()

            print(f"Users in {repo}:\n")
            for user, perm in user_and_perms:
                print(f"{user} [{perm}]")

        except GithubException as e:
            print(f"Error accessing repository: {e.data.get('message', str(e))}")
            sys.exit(1)
        finally:
            self.gh.close()
