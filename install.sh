#!/bin/bash

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install package in editable mode
pip install -e .

echo "✓ Installation complete!"
echo "To use the tool, run: python3 -m ghp"

