from typing import List, Optional
import re
from camel_tools.tokenizers.word import simple_word_tokenize
from camel_tools.utils.normalize import normalize_unicode

class ArabicTokenizer:
    """Tokenizer for Arabic text using CAMeL Tools with additional customizations."""
    
    def __init__(self, preserve_diacritics: bool = False):
        """
        Initialize the tokenizer.
        
        Args:
            preserve_diacritics: Whether to preserve Arabic diacritics during tokenization
        """
        self.preserve_diacritics = preserve_diacritics
        self.diacritic_pattern = re.compile(r'[\u064B-\u065F\u0670]')

    def preprocess(self, text: str) -> str:
        """
        Preprocess Arabic text before tokenization.
        
        Args:
            text: Input Arabic text
        
        Returns:
            Preprocessed text
        """
        # Normalize Unicode representations
        text = normalize_unicode(text)
        
        if not self.preserve_diacritics:
            text = self.remove_diacritics(text)
        
        return text
    
    def remove_diacritics(self, text: str) -> str:
        """
        Remove Arabic diacritical marks from text.
        
        Args:
            text: Input Arabic text
        
        Returns:
            Text with diacritics removed
        """
        return self.diacritic_pattern.sub('', text)
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize Arabic text into words.
        
        Args:
            text: Input Arabic text
        
        Returns:
            List of tokens
        """
        preprocessed_text = self.preprocess(text)
        tokens = simple_word_tokenize(preprocessed_text)
        return tokens
