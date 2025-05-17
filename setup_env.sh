#!/bin/bash

# Exit on any error
set -e


# Define environment name
ENV_NAME="simon_hochmuth_portfolio"

# If exists already, remove environment to reinstall
echo "📦 Removing virtual environment: $ENV_NAME if exists"
rm -rf simon_hochmuth_portfolio

echo "📦 Creating new virtual environment with Python 3.11: $ENV_NAME"
py -3.11 -m venv $ENV_NAME

echo "✅ Activating virtual environment"
source $ENV_NAME/Scripts/activate

echo "⬆️  Upgrading pip"
$ENV_NAME/Scripts/python.exe -m pip install --upgrade pip

echo "📚 Installing dependencies from requirements.txt (with prefer-binary)"
$ENV_NAME/Scripts/python.exe -m pip install --prefer-binary -r requirements.txt

echo "✅ Setup complete! Virtual environment '$ENV_NAME' is ready."
echo "To activate later, run:"
echo "  source $ENV_NAME/Scripts/activate"
