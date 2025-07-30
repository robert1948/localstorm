"""Health Routes"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def health_root():
    return {"message": "health endpoint"}
