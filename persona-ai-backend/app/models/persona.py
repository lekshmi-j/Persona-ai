from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

class PersonaCreate(BaseModel):
    """Data the user sends when creating a persona."""
    name: str
    description: str
    personality_traits: List[str] = []
    beliefs: List[str] = []
    speech_style: str
    tone: str

class PersonaUpdate(BaseModel):
    """All fields optional — user can update any subset."""
    name: Optional[str] = None
    description: Optional[str] = None
    personality_traits: Optional[List[str]] = None
    beliefs: Optional[List[str]] = None
    speech_style: Optional[str] = None
    tone: Optional[str] = None

class PersonaResponse(BaseModel):
    """What the API returns — safe to expose publicly."""
    persona_id: str
    name: str
    description: str
    personality_traits: List[str]
    beliefs: List[str]
    speech_style: str
    tone: str
    created_by: str
    created_at: str
    updated_at: str

class PersonaInDB(PersonaResponse):
    """
    Internal model — same as response for personas.
    Kept separate so you can add internal-only fields
    later without touching the public response shape.
    """
    pass