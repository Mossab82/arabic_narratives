from typing import List, Set
import re
from pathlib import Path

class ArabicCleaner:
    """Text cleaner for Arabic text with configurable cleaning rules."""
    
    def __init__(self, stopwords_file: Optional[str] = None):
        """
        Initialize the cleaner.
        
        Args:
            stopwords_file: Path to file containing Arabic stopwords
        """
        self.stopwords = self._load_stopwords(stopwords_file) if stopwords_file else set()
        self.noise_pattern = re.compile(
            r'[^\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF\s]+'
        )

    def _load_stopwords(self, filepath: str) -> Set[str]:
        """
        Load Arabic stopwords from file.
        
        Args:
            filepath: Path to stopwords file
        
        Returns:
            Set of stopwords
        """
        stopwords = set()
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                stopwords.update(line.strip() for line in f if line.strip())
        except FileNotFoundError:
            print(f"Warning: Stopwords file {filepath} not found")
        return stopwords

    def clean(self, text: str) -> str:
        """
        Clean Arabic text by removing noise and applying cleaning rules.
        
        Args:
            text: Input Arabic text
        
        Returns:
            Cleaned text
        """
        # Remove non-Arabic characters
        text = self.noise_pattern.sub(' ', text)
        
        # Remove stopwords if loaded
        if self.stopwords:
            words = text.split()
            words = [w for w in words if w not in self.stopwords]
            text = ' '.join(words)
        
        return text.strip()

def main():
    """Demonstrate usage of preprocessing modules."""
    # Example Arabic text
    text = "وَقَالَ شَهْرِيَارُ لِشَهْرَزَادَ: حَدِّثِينِي حَدِيثًا"
    
    # Initialize components
    tokenizer = ArabicTokenizer(preserve_diacritics=False)
    normalizer = ArabicNormalizer()
    cleaner = ArabicCleaner()
    
    # Process text
    print("Original text:", text)
    print("Tokenized:", tokenizer.tokenize(text))
    print("Normalized:", normalizer.normalize(text))
    print("Cleaned:", cleaner.clean(text))

if __name__ == '__main__':
    main()
