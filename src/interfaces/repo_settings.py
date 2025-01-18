from abc import ABC, abstractmethod

from enum import Enum


class Permission(Enum):
    """Enum representing GitHub repository access permission levels"""

    READ = "read"  # Read-only access to the repository
    WRITE = "write"  # Read and write access to the repository
    ADMIN = "admin"  # Full administrative access to the repository


class RepoSettingsInterface(ABC):
    @abstractmethod
    def useradd(self, repo: str, user: str, permission: Permission) -> None:
        """Add a user to a repository with a given permission level"""
        pass

    @abstractmethod
    def deluser(self, repo: str, user: str) -> None:
        """Remove a user from a repository"""
        pass

    @abstractmethod
    def users(self, repo: str) -> None:
        """List all users in a repository"""
        pass
