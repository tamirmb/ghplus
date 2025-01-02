#!/bin/bash

# Check if script is run with sudo
if [ "$EUID" -ne 0 ]; then 
    echo "Please run with sudo"
    exit 1
fi

# Clean up existing installation
if [ -f "/usr/local/bin/ghp" ]; then
    echo "Removing existing installation..."
    rm /usr/local/bin/ghp
fi

# Install dependencies
pip3 install -r requirements.txt

# Make the script executable
chmod +x ghp.py

# Copy to /usr/local/bin
cp ghp.py /usr/local/bin/ghp

echo "✓ Installation complete! You can now run 'ghp' from anywhere"
