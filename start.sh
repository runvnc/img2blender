#!/bin/bash

# Check if Python virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Check if Blender is installed
if ! command -v blender &> /dev/null; then
    echo "Error: Blender is not installed or not in PATH"
    echo "Please install Blender and make sure it's accessible from command line"
    exit 1
fi

# Create outputs directory if it doesn't exist
mkdir -p outputs

# Start the Flask application
echo "Starting Image to Blender converter..."
python app.py
