"""Pydantic models for {{PROJECT_NAME}}."""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class {{PROJECT_NAME}}Base(BaseModel):
    """Base {{PROJECT_NAME}} model with common attributes."""
    name: str = Field(..., description="Name of the {{PROJECT_NAME.lower()}}")
    description: Optional[str] = Field(None, description="Description of the {{PROJECT_NAME.lower()}}")

class {{PROJECT_NAME}}Create({{PROJECT_NAME}}Base):
    """Model for creating a new {{PROJECT_NAME}}."""
    pass

class {{PROJECT_NAME}}({{PROJECT_NAME}}Base):
    """Model for a {{PROJECT_NAME}} with all attributes."""
    id: int = Field(..., description="Unique identifier")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

    class Config:
        """Pydantic config."""
        orm_mode = True
