# Fapi Project Creator

A command-line tool for creating and managing FastAPI projects.

## Overview

Fapi Project Creator helps you quickly bootstrap and manage FastAPI projects with a well-organized structure and common dependencies. It provides an intuitive CLI interface to create projects, add components, and run your API in development mode.

## Features

- Initialize new FastAPI projects with standardized structure
- Generate essential configuration files
- Create routers, models, and other components
- Run development server
- Choose from various license options
- Initialize git repository

## Installation

### Prerequisites

- Python 3.6+
- pip
- git (optional, but recommended)

### Installation Steps

```bash
# Clone the repository
git clone https://github.com/GonzoDMX/Fapi_Project_Creator.git

# Run the installation script
cd Fapi_Project_Creator
sudo bash install.sh
```

## Usage

### Create a new FastAPI project

```bash
fapi init my_new_project
```

### Create a new router in an existing project

```bash
cd my_project
fapi router user
```

### Create a new Pydantic model

```bash
fapi model user
```

### Run the development server

```bash
fapi run
```

### Show version information

```bash
fapi version
```

### Show help

```bash
fapi --help
```

## Generated Project Structure

When you initialize a new project, it will have the following structure:

```
my_new_project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── dependencies.py
│   ├── routers/
│   │   └── __init__.py
│   ├── core/
│   │   └── __init__.py
│   ├── models/
│   │   └── __init__.py
│   ├── config/
│   │   └── __init__.py
│   └── services/
│       └── __init__.py
├── tests/
│   └── __init__.py
├── .gitignore
├── requirements.txt
├── README.md
├── .env.example
└── LICENSE (if selected)
```

## Customization

### Modifying Templates

All template files are stored in the `templates` directory of the GitHub repository:

```
templates/
├── gitignore
├── requirements.txt
├── readme.md
├── env.example
├── main.py
├── dependencies.py
├── router.py
├── model.py
└── licenses/
    ├── mit
    ├── apache2
    ├── gpl2
    ├── gpl3
    └── closed_source
```

To customize any template, simply edit the corresponding file. Variable substitution is supported using the following placeholders:

- `{{PROJECT_NAME}}` - Name of the project
- `{{AUTHOR_NAME}}` - Author name (for licenses)
- `{{YEAR}}` - Current year (for licenses)

## Available Commands

| Command | Description |
|---------|-------------|
| `init <project_name>` | Create a new FastAPI project |
| `router <router_name>` | Create a new router in the current project |
| `model <model_name>` | Create a new Pydantic model in the current project |
| `run` | Run the development server for the current project |
| `version` | Show version information |

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](https://raw.githubusercontent.com/GonzoDMX/Fapi_Project_Creator/refs/heads/main/LICENSE) file for details.

## Contact

If you have any questions or suggestions, please open an issue on GitHub.
