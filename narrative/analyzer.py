from typing import List, Dict, Any
import networkx as nx
from dataclasses import dataclass
from .extractor import NarrativeStructure, Character, Event

@dataclass
class NarrativeAnalysis:
    """Data class for narrative analysis results."""
    complexity_score: float
    character_network: nx.Graph
    event_sequence: List[Dict[str, Any]]
    theme_analysis: Dict[str, float]
    structural_patterns: List[Dict[str, Any]]

class NarrativeAnalyzer:
    """Analyzes extracted narrative structures."""
    
    def __init__(self):
        """Initialize the narrative analyzer."""
        self.semantic_analyzer = ArabicSemanticAnalyzer()

    def analyze_narrative(self, narrative: NarrativeStructure) -> NarrativeAnalysis:
        """
        Perform comprehensive analysis of narrative structure.
        
        Args:
            narrative: NarrativeStructure object
            
        Returns:
            NarrativeAnalysis object
        """
        return NarrativeAnalysis(
            complexity_score=self._calculate_complexity(narrative),
            character_network=self._build_character_network(narrative),
            event_sequence=self._analyze_event_sequence(narrative),
            theme_analysis=self._analyze_themes(narrative),
            structural_patterns=self._identify_patterns(narrative)
        )

    def _calculate_complexity(self, narrative: NarrativeStructure) -> float:
        """Calculate narrative complexity score."""
        factors = [
            len(narrative.characters),
            len(narrative.events),
            narrative.frame_level,
            self._calculate_relationship_density(narrative),
            self._calculate_theme_diversity(narrative)
        ]
        return np.mean(factors)

    def _build_character_network(self, narrative: NarrativeStructure) -> nx.Graph:
        """Build network of character relationships."""
        G = nx.Graph()
        
        # Add characters as nodes
        for character in narrative.characters:
            G.add_node(character.name, role=character.role)
        
        # Add relationships as edges
        for character in narrative.characters:
            for related_char, relations in character.relationships.items():
                if G.has_node(related_char):
                    G.add_edge(character.name, related_char, 
                              relationship_types=relations)
        
        return G
