#!/usr/bin/env python3
"""
Fapi - FastAPI Project Management Tool

A CLI tool for managing FastAPI projects.
Usage: fapi <command> [options]
"""

import os
import sys
import shutil
import argparse
import tempfile
import datetime
import requests
import sys
import subprocess
from pathlib import Path

# GitHub repository where template files are stored
GITHUB_REPO_URL = "https://raw.githubusercontent.com/GonzoDMX/Fapi_Project_Creator/refs/heads/main"

# Directory structure to create
PROJECT_STRUCTURE = [
    "app",
    "app/routers",
    "app/core",
    "app/models",
    "app/config",
    "app/services",
    "tests"
]

# Files to create with their paths
PROJECT_FILES = [
    "app/__init__.py",
    "app/main.py",
    "app/dependencies.py",
    "app/routers/__init__.py",
    "app/core/__init__.py",
    "app/models/__init__.py",
    "app/config/__init__.py",
    "app/services/__init__.py",
    "tests/__init__.py"
]

# License options
LICENSES = {
    "1": "Closed Source",
    "2": "MIT",
    "3": "Apache 2.0",
    "4": "GPL v2",
    "5": "GPL v3",
    "6": "None"
}

def download_template(template_path, output_path, project_name=None, author_name=None):
    """
    Download a template file from GitHub and apply any necessary substitutions.
    
    Args:
        template_path: Path to the template in the GitHub repo
        output_path: Where to save the file locally
        project_name: Name of the project for template substitution
        author_name: Author name for template substitution
    """
    # First try to load from config directory
    config_dir = os.environ.get('FAPI_CONFIG_DIR')
    
    if config_dir and os.path.exists(os.path.join(config_dir, "templates", template_path)):
        # Use local template from config directory
        template_file = os.path.join(config_dir, "templates", template_path)
        try:
            with open(template_file, 'r') as f:
                content = f.read()
        except Exception as e:
            print(f"Failed to read template '{template_path}' from config directory: {e}")
            return False
    else:
        # Fallback to GitHub download
        url = f"{GITHUB_REPO_URL}/templates/{template_path}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            content = response.text
        except requests.RequestException as e:
            print(f"Failed to download template '{template_path}': {e}")
            return False
    
    # Apply template substitutions
    if project_name:
        content = content.replace("{{PROJECT_NAME}}", project_name)
    if author_name:
        content = content.replace("{{AUTHOR_NAME}}", author_name)
    content = content.replace("{{YEAR}}", str(datetime.datetime.now().year))
    
    # Create directory for the file if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Write the file
    with open(output_path, 'w') as f:
        f.write(content)
    return True

def create_empty_file(path):
    """Create an empty file, ensuring its directory exists."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write('"""Initialize package."""\n')

def init_project(project_name, no_git=False):
    """Create a new FastAPI project."""
    # Check if the project directory already exists
    if os.path.exists(project_name):
        print(f"Error: Directory '{project_name}' already exists.")
        return False

    # Create the project directory
    os.makedirs(project_name)
    print(f"Created project directory: {project_name}")

    # Create the project structure
    for directory in PROJECT_STRUCTURE:
        os.makedirs(os.path.join(project_name, directory), exist_ok=True)
        print(f"Created directory: {directory}")

    # Create __init__.py files
    for file_path in PROJECT_FILES:
        if file_path.endswith("__init__.py"):
            create_empty_file(os.path.join(project_name, file_path))
            print(f"Created file: {file_path}")

    # Download template files
    template_files = {
        "main.py": "app/main.py",
        "dependencies.py": "app/dependencies.py",
        "requirements.txt": "requirements.txt",
        "env.example": ".env.example",
        "readme.md": "README.md",
        "gitignore": ".gitignore"
    }
    
    for template_name, file_path in template_files.items():
        success = download_template(template_name, os.path.join(project_name, file_path), project_name)
        if success:
            print(f"Created {file_path} from template")
        else:
            print(f"Failed to create {file_path}, using fallback")
            # If download fails, create a minimal placeholder file
            with open(os.path.join(project_name, file_path), 'w') as f:
                f.write(f"# {os.path.basename(file_path)} for {project_name}\n")

    # Handle license selection
    print("\nSelect a license for your project:")
    for key, license_name in LICENSES.items():
        print(f"{key}. {license_name}")
    
    license_choice = input("Enter your choice (1-6): ")
    while license_choice not in LICENSES:
        license_choice = input("Invalid choice. Enter a number from 1 to 6: ")
    
    license_type = LICENSES[license_choice]
    
    if license_type != "None":
        author_name = input("Enter the author/organization name for the license: ")
        license_filename = "LICENSE"
        
        if license_type == "Closed Source":
            license_template = "licenses/closed_source"
        elif license_type == "MIT":
            license_template = "licenses/mit"
        elif license_type == "Apache 2.0":
            license_template = "licenses/apache2"
        elif license_type == "GPL v2":
            license_template = "licenses/gpl2"
        elif license_type == "GPL v3":
            license_template = "licenses/gpl3"
        
        success = download_template(
            license_template, 
            os.path.join(project_name, license_filename),
            project_name,
            author_name
        )
        
        if success:
            print(f"Created {license_filename} with {license_type} license")
        else:
            print(f"Failed to create license file")

    # Initialize git repository if not disabled
    if not no_git:
        setup_git(project_name)

    print(f"\nProject '{project_name}' created successfully!")
    return True

def setup_git(project_dir):
    """Initialize git repository in the project directory."""
    try:
        subprocess.run(["git", "init"], cwd=project_dir, check=True, stdout=subprocess.PIPE)
        print("Initialized git repository")
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        print("Git initialization skipped (git may not be installed)")
        return False

def create_router(project_dir, router_name):
    """Create a new router in an existing project."""
    if not os.path.exists(project_dir):
        print(f"Error: Project directory '{project_dir}' does not exist.")
        return False
    
    router_dir = os.path.join(project_dir, "app/routers")
    if not os.path.exists(router_dir):
        print(f"Error: Routers directory not found in '{project_dir}'.")
        return False
    
    # Create router file
    router_file = os.path.join(router_dir, f"{router_name}.py")
    if os.path.exists(router_file):
        print(f"Error: Router '{router_name}' already exists.")
        return False
    
    # Try to download router template
    success = download_template(
        "router.py", 
        router_file, 
        router_name.replace("_", " ").title().replace(" ", "")
    )
    
    if not success:
        # Use fallback template if download fails
        router_content = f'''"""Router for {router_name} endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional

router = APIRouter(
    prefix="/{router_name}",
    tags=["{router_name.replace('_', ' ').title()}"],
    responses={{404: {{"description": "Not found"}}}}
)

@router.get("/")
async def get_{router_name}s():
    """Get all {router_name.replace('_', ' ')}s."""
    return {{"message": "List of {router_name.replace('_', ' ')}s"}}

@router.get("/{{item_id}}")
async def get_{router_name}(item_id: int):
    """Get a specific {router_name.replace('_', ' ')}."""
    return {{"id": item_id, "name": "{router_name.replace('_', ' ')} name"}}

@router.post("/")
async def create_{router_name}():
    """Create a new {router_name.replace('_', ' ')}."""
    return {{"message": "Created {router_name.replace('_', ' ')}"}}

@router.put("/{{item_id}}")
async def update_{router_name}(item_id: int):
    """Update a {router_name.replace('_', ' ')}."""
    return {{"id": item_id, "message": "Updated {router_name.replace('_', ' ')}"}}

@router.delete("/{{item_id}}")
async def delete_{router_name}(item_id: int):
    """Delete a {router_name.replace('_', ' ')}."""
    return {{"message": "Deleted {router_name.replace('_', ' ')} with id {{item_id}}"}}
'''
        with open(router_file, 'w') as f:
            f.write(router_content)
    
    print(f"Created router: {router_name}")
    
    # Suggest import in main.py
    print("\nTo use this router, add the following to your app/main.py:")
    print(f"from app.routers import {router_name}")
    print(f"app.include_router({router_name}.router)")
    
    return True

def create_model(project_dir, model_name):
    """Create a new Pydantic model in an existing project."""
    if not os.path.exists(project_dir):
        print(f"Error: Project directory '{project_dir}' does not exist.")
        return False
    
    models_dir = os.path.join(project_dir, "app/models")
    if not os.path.exists(models_dir):
        print(f"Error: Models directory not found in '{project_dir}'.")
        return False
    
    # Create model file
    model_file = os.path.join(models_dir, f"{model_name}.py")
    if os.path.exists(model_file):
        print(f"Error: Model '{model_name}' already exists.")
        return False
    
    # Try to download model template
    success = download_template(
        "model.py", 
        model_file, 
        model_name.replace("_", " ").title().replace(" ", "")
    )
    
    if not success:
        # Use fallback template if download fails
        class_name = model_name.replace("_", " ").title().replace(" ", "")
        model_content = f'''"""Pydantic models for {model_name}."""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class {class_name}Base(BaseModel):
    """Base {class_name} model with common attributes."""
    name: str = Field(..., description="Name of the {model_name.replace('_', ' ')}")
    description: Optional[str] = Field(None, description="Description of the {model_name.replace('_', ' ')}")

class {class_name}Create({class_name}Base):
    """Model for creating a new {class_name}."""
    pass

class {class_name}({class_name}Base):
    """Model for a {class_name} with all attributes."""
    id: int = Field(..., description="Unique identifier")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

    class Config:
        """Pydantic config."""
        orm_mode = True
'''
        with open(model_file, 'w') as f:
            f.write(model_content)
    
    print(f"Created model: {model_name}")
    
    # Suggest import
    print("\nTo use this model, add the following import where needed:")
    print(f"from app.models.{model_name} import {model_name.replace('_', ' ').title().replace(' ', '')}")
    
    return True

def run_dev_server(project_dir):
    """Run development server for a project."""
    if not os.path.exists(project_dir):
        print(f"Error: Project directory '{project_dir}' does not exist.")
        return False
    
    # Check for app/main.py
    main_file = os.path.join(project_dir, "app/main.py")
    if not os.path.exists(main_file):
        print(f"Error: app/main.py not found in '{project_dir}'.")
        return False
    
    # Check if uvicorn is installed
    try:
        subprocess.run(["uvicorn", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except (subprocess.SubprocessError, FileNotFoundError):
        print("Error: uvicorn is not installed. Installing required packages...")
        try:
            # Try to install from requirements.txt if it exists
            req_file = os.path.join(project_dir, "requirements.txt")
            if os.path.exists(req_file):
                subprocess.run(["pip", "install", "-r", req_file], check=True)
            else:
                subprocess.run(["pip", "install", "uvicorn", "fastapi"], check=True)
        except subprocess.SubprocessError:
            print("Failed to install required packages. Please install manually.")
            return False
    
    # Run the server
    print(f"Starting development server for '{project_dir}'...")
    print("Access the API at http://127.0.0.1:8000")
    print("API documentation at http://127.0.0.1:8000/docs")
    print("Press CTRL+C to stop the server")
    
    try:
        subprocess.run(["uvicorn", "app.main:app", "--reload"], cwd=project_dir)
        return True
    except subprocess.SubprocessError:
        print("Failed to start development server.")
        return False

def main():
    # Set config directory in environment for template loading
    config_dir = os.environ.get('FAPI_CONFIG_DIR')
    if not config_dir:
        # Try to find the config directory
        possible_config_dirs = [
            os.path.join(os.path.expanduser("~"), ".config", "fapi"),
            "/etc/fapi"
        ]
        for dir_path in possible_config_dirs:
            if os.path.exists(dir_path) and os.path.isdir(dir_path):
                os.environ['FAPI_CONFIG_DIR'] = dir_path
                break
    
    # Create the top-level parser
    parser = argparse.ArgumentParser(
        description="FastAPI Project Management Tool",
        usage="fapi <command> [<args>]"
    )
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Parser for 'init' command
    init_parser = subparsers.add_parser("init", help="Initialize a new FastAPI project")
    init_parser.add_argument("project_name", help="Name of the project to create")
    init_parser.add_argument("--no-git", action="store_true", help="Skip git initialization")
    
    # Parser for 'router' command
    router_parser = subparsers.add_parser("router", help="Create a new router")
    router_parser.add_argument("router_name", help="Name of the router to create")
    router_parser.add_argument("--project", "-p", default=".", help="Project directory (default: current directory)")
    
    # Parser for 'model' command
    model_parser = subparsers.add_parser("model", help="Create a new Pydantic model")
    model_parser.add_argument("model_name", help="Name of the model to create")
    model_parser.add_argument("--project", "-p", default=".", help="Project directory (default: current directory)")
    
    # Parser for 'run' command
    run_parser = subparsers.add_parser("run", help="Run development server")
    run_parser.add_argument("--project", "-p", default=".", help="Project directory (default: current directory)")
    
    # Parser for 'version' command
    version_parser = subparsers.add_parser("version", help="Show version information")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Handle commands
    if args.command == "init":
        init_project(args.project_name, args.no_git)
        
        print(f"\nNext steps:")
        print(f"  cd {args.project_name}")
        print(f"  python -m venv venv")
        print(f"  source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
        print(f"  pip install -r requirements.txt")
        print(f"  cp .env.example .env  # Update with your configuration")
        print(f"  fapi run")
        
    elif args.command == "router":
        create_router(args.project, args.router_name)
        
    elif args.command == "model":
        create_model(args.project, args.model_name)
        
    elif args.command == "run":
        run_dev_server(args.project)
        
    elif args.command == "version":
        print("Fapi - FastAPI Project Management Tool v0.1.0")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
