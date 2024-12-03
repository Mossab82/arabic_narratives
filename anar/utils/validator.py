"""
Validation utilities for the ANAR system.
Provides comprehensive validation for Arabic text, network structures,
and cultural elements.
"""

import re
import logging
from typing import Dict, List, Any, Union
import networkx as nx
from ..models import (
    ProcessedText,
    NarrativeStructure,
    Frame,
    CulturalElement
)

class Validator:
    """
    Validator for ANAR system components.
    
    Features:
    - Arabic text validation
    - Network structure validation
    - Cultural preservation validation
    - Frame structure validation
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Arabic text patterns
        self.arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F]+')
        self.diacritics_pattern = re.compile(r'[\u064B-\u065F\u0670]')
        
    def is_valid_arabic(self, text: str) -> bool:
        """
        Validate Arabic text.
        
        Args:
            text: Input text
            
        Returns:
            True if valid Arabic text
        """
        if not text or not isinstance(text, str):
            return False
            
        # Check for Arabic characters
        if not self.arabic_pattern.search(text):
            return False
            
        # Additional checks can be added here
        return True
        
    def validate_network(
        self,
        G: nx.MultiDiGraph
    ) -> bool:
        """
        Validate narrative network structure.
        
        Args:
            G: Narrative network
            
        Returns:
            True if valid network
        """
        try:
            # Check basic network properties
            if not G.number_of_nodes() > 0:
                return False
                
            # Verify node types
            for node, data in G.nodes(data=True):
                if 'type' not in data:
                    return False
                    
            # Verify edge properties
            for u, v, data in G.edges(data=True):
                if 'type' not in data or 'weight' not in data:
                    return False
                    
            return True
            
        except Exception as e:
            self.logger.error(f"Network validation error: {e}")
            return False
            
    def validate_frames(
        self,
        frames: List[Frame]
    ) -> bool:
        """
        Validate frame story structure.
        
        Args:
            frames: List of frames
            
        Returns:
            True if valid frame structure
        """
        try:
            if not frames:
                return False
                
            # Check frame hierarchy
            frame_ids = set(frame.id for frame in frames)
            
            for frame in frames:
                # Check parent reference
                if frame.parent and frame.parent.id not in frame_ids:
                    return False
                    
                # Check children references
                for child in frame.children:
                    if child.id not in frame_ids:
                        return False
                        
            return True
            
        except Exception as e:
            self.logger.error(f"Frame validation error: {e}")
            return False
            
    def validate_cultural_preservation(
        self,
        elements: List[CulturalElement]
    ) -> bool:
        """
        Validate cultural element preservation.
        
        Args:
            elements: Cultural elements
            
        Returns:
            True if valid preservation
        """
        try:
            if not elements:
                return False
                
            for element in elements:
                # Validate basic properties
                if not all([
                    element.type,
                    element.text,
                    element.context,
                    isinstance(element.confidence, float),
                    0 <= element.confidence <= 1
                ]):
                    return False
                    
                # Validate references
                if element.references and not all(
                    isinstance(ref, str) for ref in element.references
                ):
                    return False
                    
            return True
            
        except Exception as e:
            self.logger.error(f"Cultural preservation validation error: {e}")
            return False
            
    def validate_narrative_structure(
        self,
        narrative: NarrativeStructure
    ) -> bool:
        """
        Validate complete narrative structure.
        
        Args:
            narrative: Narrative structure
            
        Returns:
            True if valid structure
        """
        try:
            # Validate basic properties
            if not all([
                narrative.id,
                narrative.title,
                isinstance(narrative.frame_level, int),
                narrative.metadata
            ]):
                return False
                
            # Validate components
            validations = [
                self.validate_frames(narrative.frames),
                self.validate_cultural_preservation(
                    narrative.cultural_elements
                )
            ]
            
            return all(validations)
            
        except Exception as e:
            self.logger.error(f"Narrative structure validation error: {e}")
            return False
            
    def validate_processing_result(
        self,
        result: ProcessedText
    ) -> bool:
        """
        Validate text processing result.
        
        Args:
            result: Processing result
            
        Returns:
            True if valid result
        """
        try:
            # Validate basic properties
            if not all([
                result.original,
                result.normalized,
                result.morphemes,
                isinstance(result.features, (np.ndarray, list))
            ]):
                return False
                
            # Validate morphological analysis
            for morpheme in result.morphemes:
                if not all([
                    'token' in morpheme,
                    'root' in morpheme,
                    'pattern' in morpheme,
                    'pos' in morpheme
                ]):
                    return False
                    
            return True
            
        except Exception as e:
            self.logger.error(f"Processing result validation error: {e}")
            return False
