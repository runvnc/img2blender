@echo off

REM Check if Python virtual environment exists
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate
)

REM Check if Blender is installed
blender --version >nul 2>&1
if errorlevel 1 (
    echo Error: Blender is not installed or not in PATH
    echo Please install Blender and make sure it's accessible from command line
    exit /b 1
)

REM Create outputs directory if it doesn't exist
if not exist outputs mkdir outputs

REM Start the Flask application
echo Starting Image to Blender converter...
python app.py
