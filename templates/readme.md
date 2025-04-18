# {{PROJECT_NAME}}

## Overview
A FastAPI project created with fastapi-project-creator.

## Setup

### Requirements
- Python 3.10+
- pip

### Installation
```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables
Copy the example environment file:
```bash
cp .env.example .env
```
Then edit the `.env` file with your configuration.

## Running the Application

### Development
```bash
uvicorn app.main:app --reload
```

### Production
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Documentation
Once the application is running, you can access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing
```bash
pytest
```

## License
Copyright © {{YEAR}}
