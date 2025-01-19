# GitHub Settings (ghsettings)

Configure GitHub settings from the command line

## Installation

```bash
# Build and install package in current directory
pip install -e .

# Add Python bin directory to PATH


# Set up your configuration file
ghsettings configure
```

You can generate a personal access token at: https://github.com/settings/tokens

## Commands

```bash
ghsettings repo <repository> adduser <username> <read|write|admin>
ghsettings repo <repository> deluser <username>
ghsettings repo <repository> users
```
