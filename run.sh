#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 to run this application."
    exit 1
fi

# Check if virtual environment exists, if not create it
if [ ! -d "llmquant_env" ]; then
    echo "Creating virtual environment..."
    python3 -m venv llmquant_env
fi

# Activate virtual environment
echo "Activating virtual environment..."
source llmquant_env/bin/activate

# Check if the required packages are installed
echo "Checking and installing required packages..."
pip install -r requirements.txt

# Set default font path to the project font
DEFAULT_FONT_PATH="$(pwd)/font/STKaiti.ttf"

# Get font path from command line argument
FONT_PATH=""
if [ "$1" != "" ]; then
    FONT_PATH="$1"
    if [ ! -f "$FONT_PATH" ]; then
        echo "Warning: Font file not found at $FONT_PATH. Will use default font."
        FONT_PATH="$DEFAULT_FONT_PATH"
    else
        echo "Using custom font: $FONT_PATH"
    fi
else
    # Use the default font if no argument is provided
    if [ -f "$DEFAULT_FONT_PATH" ]; then
        FONT_PATH="$DEFAULT_FONT_PATH"
        echo "Using default font: $FONT_PATH"
    else
        echo "Warning: Default font not found at $DEFAULT_FONT_PATH. Will use system font."
    fi
fi

# Run the report generator
echo "Generating PDF report..."
if [ "$FONT_PATH" != "" ]; then
    python generate_report_simple.py "$FONT_PATH"
else
    python generate_report_simple.py
fi

echo "Done! Check output/LLMQuant_Report.pdf for the generated report."

# Deactivate virtual environment
deactivate 