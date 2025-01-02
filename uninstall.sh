#!/bin/bash

if [ "$EUID" -ne 0 ]; then 
    echo "Please run with sudo"
    exit 1
fi

rm /usr/local/bin/ghp
echo "✓ Uninstallation complete" 
