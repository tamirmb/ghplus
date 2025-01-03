## GitHub Plus

A superset of the official GitHub CLI tools with a bunch of commands that they should have included, but for some reason didn't.

### Setup

First, install `ghp` so you can use it from anywhere:

```bash
sudo ./install.sh
```

Then, [generate a GitHub personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-personal-access-token-classic) with the following scopes:

- `repo`

### Configuration

Configure `ghp` and enter your personal access token:

```bash
ghp configure
```

Your personal access token <ins>**is written as plaintext**</ins> to `~/.ghp/config`.

### Commands

```bash
# Add a user to one of your repositories
ghp repo [repo] adduser [user] [read|write|admin]

# Remove a user from one of your repositories
ghp repo [repo] rmuser [user]

# List organization secrets
ghp secrets ls
```
