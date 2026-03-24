# app/routers/personas.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_personas():
    return []