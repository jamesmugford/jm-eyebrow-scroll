#!/bin/bash

echo "Setting up Eyebrow Scroll..."

# Check if xdotool is installed (needed for Linux scrolling)
#if ! command -v xdotool &> /dev/null; then
#    echo "Installing xdotool..."
#    sudo apt-get update
#    sudo apt-get install -y xdotool
#fi

# Create virtual environment if it doesn't exist
#if [ ! -d ".venv" ]; then
#    echo "Creating virtual environment..."
#    python3 -m venv .venv
#fi

# Activate virtual environment
#echo "Activating virtual environment..."
#source .venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Start the application
echo "Starting Eyebrow Scroll..."
python3 jm_eyebrow_scroll.py

# Keep terminal open if there's an error
read -p "Press Enter to exit..."
