#!/bin/bash
# Script to install the Fapi CLI tool

set -e

# Define constants
SCRIPT_NAME="fapi"
INSTALL_DIR="/usr/local/bin"
REPO_URL="https://github.com/GonzoDMX/Fapi_Project_Creator.git"

# Check if running with sudo/root privileges
if [ "$(id -u)" -ne 0 ]; then
    echo "This script requires administrative privileges. Please run with sudo."
    exit 1
fi

# Check for required dependencies
echo "Checking dependencies..."
command -v python3 >/dev/null 2>&1 || { echo "Python 3 is required but not installed. Aborting."; exit 1; }
command -v pip3 >/dev/null 2>&1 || { echo "pip3 is required but not installed. Aborting."; exit 1; }

# Install required Python packages
echo "Installing required Python packages..."
pip3 install requests

# Download the main script
echo "Downloading Fapi CLI tool..."
wget -q "${REPO_URL}/raw/main/fapi-cli.py" -O "${INSTALL_DIR}/${SCRIPT_NAME}" || \
curl -s "${REPO_URL}/raw/main/fapi-cli.py" -o "${INSTALL_DIR}/${SCRIPT_NAME}"

# Make the script executable
chmod +x "${INSTALL_DIR}/${SCRIPT_NAME}"

# Create directory for assets if it doesn't exist
mkdir -p ~/.config/fapi/templates/licenses

# Download assets
echo "Setting up templates..."
TEMPLATES=("gitignore" "requirements.txt" "readme.md" "env.example" "main.py" "dependencies.py" "router.py" "model.py")
for template in "${TEMPLATES[@]}"; do
    wget -q "${REPO_URL}/raw/main/templates/${template}" -O ~/.config/fapi/templates/${template} || \
    curl -s "${REPO_URL}/raw/main/templates/${template}" -o ~/.config/fapi/templates/${template}
done

LICENSES=("mit" "apache2" "gpl2" "gpl3" "closed_source")
for license in "${LICENSES[@]}"; do
    wget -q "${REPO_URL}/raw/main/templates/licenses/${license}" -O ~/.config/fapi/templates/licenses/${license} || \
    curl -s "${REPO_URL}/raw/main/templates/licenses/${license}" -o ~/.config/fapi/templates/licenses/${license}
done

echo "Fapi CLI tool has been installed successfully!"
echo "You can now create new FastAPI projects with the command: fapi init <project_name>"
echo "Run 'fapi --help' to see all available commands."
