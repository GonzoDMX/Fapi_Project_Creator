"""Main FastAPI application for {{PROJECT_NAME}}."""

from fastapi import FastAPI, Depends
from app.dependencies import get_query_token

app = FastAPI(
    title="{{PROJECT_NAME}}",
    description="FastAPI project created with fastapi-project-creator",
    version="0.1.0"
)

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to {{PROJECT_NAME}} API"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}
