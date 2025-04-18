"""Dependencies for FastAPI application."""

from fastapi import Header, HTTPException

async def get_query_token(token: str = Header(...)):
    """Example dependency."""
    if token != "expected_token":
        raise HTTPException(status_code=400, detail="Invalid token")
    return token
