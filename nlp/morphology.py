from typing import Dict, List, Tuple
from dataclasses import dataclass
from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer
from camel_tools.tokenizers.word import simple_word_tokenize

@dataclass
class MorphologicalFeatures:
    """Data class for morphological features of Arabic words."""
    pos: str                # Part of speech
    root: str              # Root form
    pattern: str           # Word pattern
    prefix: str            # Prefix if any
    stem: str              # Word stem
    suffix: str            # Suffix if any
    gender: str            # Gender
    number: str            # Number (singular, dual, plural)
    person: str           # Person (1st, 2nd, 3rd)
    voice: str            # Voice (active/passive)
    state: str            # State (definite/indefinite)

class ArabicMorphologyAnalyzer:
    """Analyzer for Arabic morphological features using CAMeL Tools."""
    
    def __init__(self):
        """Initialize the morphological analyzer with CAMeL Tools database."""
        try:
            self.db = MorphologyDB.builtin_db()
            self.analyzer = Analyzer(self.db)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize morphology analyzer: {str(e)}")

    def analyze_word(self, word: str) -> List[MorphologicalFeatures]:
        """
        Analyze morphological features of a single word.
        
        Args:
            word: Single Arabic word
            
        Returns:
            List of possible morphological analyses
        """
        analyses = self.analyzer.analyze(word)
        features = []
        
        for analysis in analyses:
            feature = MorphologicalFeatures(
                pos=analysis.get('pos', ''),
                root=analysis.get('root', ''),
                pattern=analysis.get('pattern', ''),
                prefix=analysis.get('prefix', ''),
                stem=analysis.get('stem', ''),
                suffix=analysis.get('suffix', ''),
                gender=analysis.get('gen', ''),
                number=analysis.get('num', ''),
                person=analysis.get('per', ''),
                voice=analysis.get('vox', ''),
                state=analysis.get('stt', '')
            )
            features.append(feature)
            
        return features

    def analyze_text(self, text: str) -> Dict[str, List[MorphologicalFeatures]]:
        """
        Analyze morphological features of all words in text.
        
        Args:
            text: Input Arabic text
            
        Returns:
            Dictionary mapping words to their morphological analyses
        """
        tokens = simple_word_tokenize(text)
        analyses = {}
        
        for token in tokens:
            analyses[token] = self.analyze_word(token)
            
        return analyses
