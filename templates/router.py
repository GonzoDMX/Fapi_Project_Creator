"""Router for {{PROJECT_NAME}} endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional

router = APIRouter(
    prefix="/{{PROJECT_NAME.lower()}}",
    tags=["{{PROJECT_NAME}}"],
    responses={404: {"description": "Not found"}}
)

@router.get("/")
async def get_all():
    """Get all {{PROJECT_NAME.lower()}} items."""
    return {"message": "List of {{PROJECT_NAME.lower()}} items"}

@router.get("/{item_id}")
async def get_one(item_id: int):
    """Get a specific {{PROJECT_NAME.lower()}} item."""
    return {"id": item_id, "name": "Example {{PROJECT_NAME.lower()}} item"}

@router.post("/")
async def create():
    """Create a new {{PROJECT_NAME.lower()}} item."""
    return {"message": "Created new {{PROJECT_NAME.lower()}} item"}

@router.put("/{item_id}")
async def update(item_id: int):
    """Update a {{PROJECT_NAME.lower()}} item."""
    return {"id": item_id, "message": "Updated {{PROJECT_NAME.lower()}} item"}

@router.delete("/{item_id}")
async def delete(item_id: int):
    """Delete a {{PROJECT_NAME.lower()}} item."""
    return {"message": f"Deleted {{PROJECT_NAME.lower()}} item with id {item_id}"}
