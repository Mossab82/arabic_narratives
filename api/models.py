from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class CharacterModel(BaseModel):
    """API model for character data."""
    name: str
    mentions: List[str]
    role: str
    attributes: List[str]
    relationships: dict[str, List[str]]

    class Config:
        schema_extra = {
            "example": {
                "name": "شهرزاد",
                "mentions": ["شهرزاد", "الراوية"],
                "role": "narrator",
                "attributes": ["حكيمة", "ذكية"],
                "relationships": {
                    "شهريار": ["زوجة", "راوية"]
                }
            }
        }

class EventModel(BaseModel):
    """API model for event data."""
    text: str
    type: str
    participants: List[str]
    time_markers: List[str]
    location: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "text": "قال الملك للوزير",
                "type": "dialogue",
                "participants": ["الملك", "الوزير"],
                "time_markers": ["في الصباح"],
                "location": "القصر"
            }
        }

class NarrativeInputModel(BaseModel):
    """API model for narrative input."""
    title: str
    text: str
    source: Optional[str] = None
    metadata: Optional[dict] = Field(default_factory=dict)

    class Config:
        schema_extra = {
            "example": {
                "title": "قصة الملك العادل",
                "text": "كان يا ما كان في قديم الزمان...",
                "source": "ألف ليلة وليلة",
                "metadata": {
                    "era": "العصر العباسي",
                    "genre": "حكايات شعبية"
                }
            }
        }

class NarrativeAnalysisModel(BaseModel):
    """API model for narrative analysis results."""
    narrative_id: str
    title: str
    characters: List[CharacterModel]
    events: List[EventModel]
    themes: List[str]
    complexity_score: float
    classification: dict[str, float]
    created_at: datetime
    
    class Config:
        schema_extra = {
            "example": {
                "narrative_id": "12345",
                "title": "قصة الملك العادل",
                "characters": [...],
                "events": [...],
                "themes": ["العدل", "الحكمة"],
                "complexity_score": 0.85,
                "classification": {
                    "moral_tale": 0.75,
                    "wisdom_tale": 0.25
                },
                "created_at": "2024-01-01T12:00:00Z"
            }
        }
