from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from pathlib import Path
import json
import numpy as np
from ..nlp.morphology import ArabicMorphologyAnalyzer
from ..nlp.syntax import ArabicSyntaxAnalyzer
from ..nlp.semantics import ArabicSemanticAnalyzer

@dataclass
class Character:
    """Data class representing a character in a narrative."""
    name: str
    mentions: List[str]  # Different forms of referring to the character
    role: str           # protagonist, antagonist, etc.
    attributes: List[str]
    relationships: Dict[str, List[str]]  # Character relationships

@dataclass
class Event:
    """Data class representing an event in a narrative."""
    text: str
    type: str          # action, dialogue, description
    participants: List[str]
    time_markers: List[str]
    location: Optional[str]

@dataclass
class NarrativeStructure:
    """Data class representing the complete narrative structure."""
    title: str
    frame_level: int
    characters: List[Character]
    events: List[Event]
    settings: List[str]
    themes: List[str]

class NarrativeExtractor:
    """Extracts narrative elements from Arabic texts."""
    
    def __init__(self):
        """Initialize the narrative extractor with required analyzers."""
        self.morph_analyzer = ArabicMorphologyAnalyzer()
        self.syntax_analyzer = ArabicSyntaxAnalyzer()
        self.semantic_analyzer = ArabicSemanticAnalyzer()
        
        # Load narrative markers
        self.narrative_markers = self._load_narrative_markers()

    def _load_narrative_markers(self) -> Dict[str, List[str]]:
        """Load narrative markers from configuration file."""
        markers_path = Path(__file__).parent / "config" / "narrative_markers.json"
        try:
            with open(markers_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "time": ["في يوم", "كان", "ثم", "بعد ذلك"],
                "location": ["في", "عند", "قصر", "مدينة"],
                "dialogue": ["قال", "أجاب", "صاح", "همس"],
                "action": ["ذهب", "جاء", "فعل", "قام"]
            }

    def extract_characters(self, text: str) -> List[Character]:
        """
        Extract characters and their attributes from text.
        
        Args:
            text: Input Arabic narrative text
            
        Returns:
            List of Character objects
        """
        characters = []
        morph_analysis = self.morph_analyzer.analyze_text(text)
        syntax_structure = self.syntax_analyzer.analyze_sentence_structure(text)
        
        # Extract character mentions using NER and syntax analysis
        named_entities = self._extract_named_entities(text)
        for entity in named_entities:
            if self._is_character_entity(entity):
                character = Character(
                    name=entity["name"],
                    mentions=self._find_character_mentions(entity["name"], text),
                    role=self._determine_character_role(entity["name"], syntax_structure),
                    attributes=self._extract_character_attributes(entity["name"], text),
                    relationships=self._extract_character_relationships(entity["name"], text)
                )
                characters.append(character)
        
        return characters

    def extract_events(self, text: str) -> List[Event]:
        """
        Extract events and their details from text.
        
        Args:
            text: Input Arabic narrative text
            
        Returns:
            List of Event objects
        """
        events = []
        sentences = self._split_into_sentences(text)
        
        for sentence in sentences:
            if self._is_event_sentence(sentence):
                event = Event(
                    text=sentence,
                    type=self._determine_event_type(sentence),
                    participants=self._extract_event_participants(sentence),
                    time_markers=self._extract_time_markers(sentence),
                    location=self._extract_location(sentence)
                )
                events.append(event)
                
        return events

    def extract_structure(self, text: str, title: str) -> NarrativeStructure:
        """
        Extract complete narrative structure from text.
        
        Args:
            text: Input Arabic narrative text
            title: Title of the narrative
            
        Returns:
            NarrativeStructure object
        """
        return NarrativeStructure(
            title=title,
            frame_level=self._determine_frame_level(text),
            characters=self.extract_characters(text),
            events=self.extract_events(text),
            settings=self._extract_settings(text),
            themes=self._extract_themes(text)
        )

    # Helper methods
    def _extract_named_entities(self, text: str) -> List[Dict[str, Any]]:
        """Extract named entities using NLP tools."""
        # Implementation using Arabic NER
        pass

    def _is_character_entity(self, entity: Dict[str, Any]) -> bool:
        """Determine if named entity is a character."""
        # Implementation
        pass

    def _find_character_mentions(self, character_name: str, text: str) -> List[str]:
        """Find different mentions of the same character."""
        # Implementation
        pass

    def _determine_character_role(self, character_name: str, syntax_structure: Dict[str, Any]) -> str:
        """Determine character's role in the narrative."""
        # Implementation
        pass
