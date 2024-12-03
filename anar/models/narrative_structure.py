"""
Core data models for narrative structure representation in ANAR system.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import numpy as np
from datetime import datetime

@dataclass
class StoryMetadata:
    """Metadata for narrative stories."""
    era: str
    genre: List[str]
    narrative_style: str
    source_reference: str
    timestamp: datetime = field(default_factory=datetime.now)
    additional_info: Dict = field(default_factory=dict)

@dataclass
class ProcessedText:
    """Container for processed Arabic text."""
    original: str
    normalized: str
    morphemes: List[Dict]
    features: np.ndarray
    metadata: Dict = field(default_factory=dict)

@dataclass
class CulturalElement:
    """Representation of cultural elements in text."""
    type: str
    text: str
    context: str
    confidence: float
    metadata: Dict = field(default_factory=dict)
    references: List[str] = field(default_factory=list)

@dataclass
class Character:
    """Character representation in narratives."""
    id: str
    name_ar: str
    name_en: str
    role: str
    attributes: Dict
    relationships: List['Relationship'] = field(default_factory=list)
    cultural_markers: List[CulturalElement] = field(default_factory=list)

@dataclass
class Event:
    """Narrative event representation."""
    id: str
    type: str
    description_ar: str
    description_en: str
    participants: List[Character]
    temporal_markers: Dict
    cultural_context: List[CulturalElement]
    metadata: Dict = field(default_factory=dict)

@dataclass
class Relationship:
    """Character or event relationships."""
    source_id: str
    target_id: str
    type: str
    strength: float
    temporal: bool = False
    metadata: Dict = field(default_factory=dict)

@dataclass
class Frame:
    """Frame story structure."""
    id: str
    level: int
    text: str
    parent: Optional['Frame']
    children: List['Frame'] = field(default_factory=list)
    events: List[Event] = field(default_factory=list)
    characters: List[Character] = field(default_factory=list)
    cultural_elements: List[CulturalElement] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)

@dataclass
class NarrativeStructure:
    """Complete narrative structure representation."""
    id: str
    title: Dict[str, str]  # Arabic/English
    frame_level: int
    metadata: StoryMetadata
    frames: List[Frame]
    characters: List[Character]
    events: List[Event]
    relationships: List[Relationship]
    cultural_elements: List[CulturalElement]
    
    def get_frame_hierarchy(self) -> Dict:
        """Get hierarchical structure of frames."""
        hierarchy = {}
        for frame in self.frames:
            hierarchy[frame.id] = {
                'level': frame.level,
                'parent': frame.parent.id if frame.parent else None,
                'children': [child.id for child in frame.children]
            }
        return hierarchy
    
    def get_character_network(self) -> Dict:
        """Get character relationship network."""
        network = {}
        for character in self.characters:
            network[character.id] = {
                'relationships': [
                    {
                        'target': rel.target_id,
                        'type': rel.type,
                        'strength': rel.strength
                    }
                    for rel in character.relationships
                ]
            }
        return network
    
    def get_event_sequence(self) -> List[Dict]:
        """Get chronological sequence of events."""
        return sorted(
            [
                {
                    'id': event.id,
                    'type': event.type,
                    'time': event.temporal_markers.get('timestamp'),
                    'participants': [char.id for char in event.participants]
                }
                for event in self.events
            ],
            key=lambda x: x['time']
        )
    
    def get_cultural_context(self) -> Dict:
        """Get cultural context mapping."""
        context = {}
        for element in self.cultural_elements:
            if element.type not in context:
                context[element.type] = []
            context[element.type].append({
                'text': element.text,
                'context': element.context,
                'confidence': element.confidence
            })
        return context

class NarrativeEncoder:
    """Encoder for narrative structures to JSON format."""
    
    @staticmethod
    def encode(narrative: NarrativeStructure) -> Dict:
        """Encode narrative structure to JSON-compatible format."""
        return {
            'id': narrative.id,
            'title': narrative.title,
            'frame_level': narrative.frame_level,
            'metadata': {
                'era': narrative.metadata.era,
                'genre': narrative.metadata.genre,
                'style': narrative.metadata.narrative_style,
                'source': narrative.metadata.source_reference,
                'timestamp': narrative.metadata.timestamp.isoformat(),
                'info': narrative.metadata.additional_info
            },
            'frames': [
                NarrativeEncoder._encode_frame(frame)
                for frame in narrative.frames
            ],
            'characters': [
                NarrativeEncoder._encode_character(char)
                for char in narrative.characters
            ],
            'events': [
                NarrativeEncoder._encode_event(event)
                for event in narrative.events
            ],
            'relationships': [
                NarrativeEncoder._encode_relationship(rel)
                for rel in narrative.relationships
            ],
            'cultural_elements': [
                NarrativeEncoder._encode_cultural_element(elem)
                for elem in narrative.cultural_elements
            ]
        }
    
    @staticmethod
    def _encode_frame(frame: Frame) -> Dict:
        """Encode frame structure."""
        return {
            'id': frame.id,
            'level': frame.level,
            'text': frame.text,
            'parent': frame.parent.id if frame.parent else None,
            'children': [child.id for child in frame.children],
            'events': [event.id for event in frame.events],
            'characters': [char.id for char in frame.characters],
            'cultural_elements': [
                elem.text for elem in frame.cultural_elements
            ],
            'metadata': frame.metadata
        }
    
    @staticmethod
    def _encode_character(character: Character) -> Dict:
        """Encode character information."""
        return {
            'id': character.id,
            'name': {
                'ar': character.name_ar,
                'en': character.name_en
            },
            'role': character.role,
            'attributes': character.attributes,
            'relationships': [
                rel.target_id for rel in character.relationships
            ],
            'cultural_markers': [
                marker.text for marker in character.cultural_markers
            ]
        }
    
    @staticmethod
    def _encode_event(event: Event) -> Dict:
        """Encode event information."""
        return {
            'id': event.id,
            'type': event.type,
            'description': {
                'ar': event.description_ar,
                'en': event.description_en
            },
            'participants': [
                char.id for char in event.participants
            ],
            'temporal_markers': event.temporal_markers,
            'cultural_context': [
                elem.text for elem in event.cultural_context
            ],
            'metadata': event.metadata
        }
    
    @staticmethod
    def _encode_relationship(relationship: Relationship) -> Dict:
        """Encode relationship information."""
        return {
            'source': relationship.source_id,
            'target': relationship.target_id,
            'type': relationship.type,
            'strength': relationship.strength,
            'temporal': relationship.temporal,
            'metadata': relationship.metadata
        }
    
    @staticmethod
    def _encode_cultural_element(element: CulturalElement) -> Dict:
        """Encode cultural element information."""
        return {
            'type': element.type,
            'text': element.text,
            'context': element.context,
            'confidence': element.confidence,
            'metadata': element.metadata,
            'references': element.references
        }
