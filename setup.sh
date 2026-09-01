#!/bin/bash

# Setup script for Vulnerability Detection with CodeT5
# This script sets up the environment and prepares the project

echo "================================================"
echo "  Vulnerability Detection Setup"
echo "================================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo ""
echo "Creating project directories..."
mkdir -p data
mkdir -p outputs
mkdir -p logs

# Create .gitkeep files to preserve empty directories
touch data/.gitkeep
touch outputs/.gitkeep
touch logs/.gitkeep

echo ""
echo "================================================"
echo "  Setup Complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "  1. Place your function.json in the 'data/' directory"
echo "  2. Update DATA_PATH in vulnerability_detection_improved.py to 'data/function.json'"
echo "  3. Run: python vulnerability_detection_improved.py"
echo ""
echo "To activate the virtual environment later:"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    echo "  venv\\Scripts\\activate"
else
    echo "  source venv/bin/activate"
fi
echo ""
