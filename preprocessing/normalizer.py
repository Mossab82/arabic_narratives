from typing import Dict, List
import re
from camel_tools.utils.normalize import normalize_alef, normalize_tah_marbota

class ArabicNormalizer:
    """Normalizer for Arabic text with configurable normalization rules."""
    
    def __init__(self):
        """Initialize the normalizer with default normalization rules."""
        self.char_map = {
            'أ': 'ا',
            'إ': 'ا',
            'آ': 'ا',
            'ة': 'ه',
            'ى': 'ي',
            'ئ': 'ي',
        }
        self.compilation_flags = re.UNICODE | re.MULTILINE

    def normalize(self, text: str) -> str:
        """
        Apply all normalization rules to input text.
        
        Args:
            text: Input Arabic text
        
        Returns:
            Normalized text
        """
        text = normalize_alef(text)
        text = normalize_tah_marbota(text)
        
        # Apply character mapping
        for original, replacement in self.char_map.items():
            text = text.replace(original, replacement)
            
        # Remove consecutive whitespace
        text = ' '.join(text.split())
        
        return text
