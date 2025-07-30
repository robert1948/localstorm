"""Cape_ai Routes"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def cape_ai_root():
    return {"message": "cape_ai endpoint"}
