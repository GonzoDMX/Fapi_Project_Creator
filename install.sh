#!/bin/bash
# Script to install the Fapi CLI tool

set -e

# Define constants
SCRIPT_NAME="fapi"
SYSTEM_INSTALL_DIR="/usr/local/bin"
USER_INSTALL_DIR="$HOME/.local/bin"
CONFIG_DIR_NAME="fapi"

# Get the directory where this script is located (should be the repo root)
REPO_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Function to install templates
install_templates() {
    local config_dir="$1"
    
    # Create directory for templates if it doesn't exist
    mkdir -p "${config_dir}/templates/licenses"
    
    echo "Setting up templates..."
    
    # Copy templates from the local repository
    cp -r "${REPO_DIR}/templates/"* "${config_dir}/templates/"
    
    # Create an empty directory if licenses directory doesn't exist in the repo
    mkdir -p "${REPO_DIR}/templates/licenses"
    
    # Copy license templates
    cp -r "${REPO_DIR}/templates/licenses/"* "${config_dir}/templates/licenses/" 2>/dev/null || true
    
    # Display warning if templates directory is empty
    if [ ! "$(ls -A "${config_dir}/templates/" 2>/dev/null)" ]; then
        echo "Warning: No templates found in the repository. The tool will use fallback templates."
    fi
}

# Function to perform installation
perform_installation() {
    local install_dir="$1"
    local config_dir="$2"
    
    # Ensure install directory exists
    mkdir -p "${install_dir}"
    
    # Copy the main script from the repo
    echo "Installing Fapi CLI tool..."
    cp "${REPO_DIR}/fapi-cli.py" "${install_dir}/${SCRIPT_NAME}"
    
    # Make the script executable
    chmod +x "${install_dir}/${SCRIPT_NAME}"
    
    # Install templates
    install_templates "${config_dir}"
    
    echo "Fapi CLI tool has been installed successfully!"
    echo "You can now create new FastAPI projects with the command: fapi init <project_name>"
    echo "Run 'fapi --help' to see all available commands."
    
    # Check if the installation directory is in PATH
    if [[ ":$PATH:" != *":${install_dir}:"* ]]; then
        echo ""
        echo "NOTE: ${install_dir} is not in your PATH environment variable."
        echo "You might need to add the following line to your shell profile (~/.bashrc, ~/.zshrc, etc.):"
        echo "  export PATH=\"\$PATH:${install_dir}\""
        echo ""
        echo "Or you can run the command using the full path: ${install_dir}/fapi"
    fi
}

# Check for required dependencies
echo "Checking dependencies..."
command -v python3 >/dev/null 2>&1 || { echo "Python 3 is required but not installed. Aborting."; exit 1; }
command -v pip3 >/dev/null 2>&1 || { echo "pip3 is required but not installed. Aborting."; exit 1; }

# Check for main script file
if [ ! -f "${REPO_DIR}/fapi-cli.py" ]; then
    echo "Error: fapi-cli.py not found in the repository. Make sure you're running this script from the root of the Fapi_Project_Creator repository."
    exit 1
fi

# Install required Python packages
echo "Installing required Python packages..."
pip3 install --user requests >/dev/null || { echo "Failed to install Python dependencies. Aborting."; exit 1; }

# Check if running with sudo/root privileges
if [ "$(id -u)" -eq 0 ]; then
    # Running with sudo, offer choice of installation locations
    echo "You are running this script with sudo privileges."
    echo "Select installation location:"
    echo "1) System-wide installation (${SYSTEM_INSTALL_DIR})"
    echo "2) Current user only (${USER_INSTALL_DIR})"
    read -p "Enter your choice (1/2): " choice
    
    case $choice in
        1)
            echo "Installing system-wide..."
            perform_installation "${SYSTEM_INSTALL_DIR}" "/etc/${CONFIG_DIR_NAME}"
            ;;
        2)
            echo "Installing for current user only..."
            # Get the actual home directory of the user who invoked sudo
            SUDO_USER_HOME=$(eval echo ~${SUDO_USER})
            perform_installation "${SUDO_USER_HOME}/.local/bin" "${SUDO_USER_HOME}/.config/${CONFIG_DIR_NAME}"
            # Fix ownership
            chown -R ${SUDO_USER}:$(id -gn ${SUDO_USER}) "${SUDO_USER_HOME}/.local/bin/${SCRIPT_NAME}" "${SUDO_USER_HOME}/.config/${CONFIG_DIR_NAME}"
            ;;
        *)
            echo "Invalid choice. Exiting."
            exit 1
            ;;
    esac
else
    # Not running with sudo, install to user's local bin
    echo "You are running this script without sudo privileges."
    echo "The Fapi CLI tool will be installed to ${USER_INSTALL_DIR} and will only be available for your user."
    echo "If you want to install system-wide (available for all users), please run this script with sudo."
    read -p "Proceed with user installation? (y/n): " proceed
    
    case $proceed in
        [Yy]*)
            # Ensure ~/.local/bin exists and is in PATH
            mkdir -p "${USER_INSTALL_DIR}"
            
            perform_installation "${USER_INSTALL_DIR}" "${HOME}/.config/${CONFIG_DIR_NAME}"
            ;;
        *)
            echo "Installation cancelled."
            exit 0
            ;;
    esac
fi
