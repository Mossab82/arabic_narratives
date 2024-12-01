from typing import List, Dict, Any
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from .extractor import NarrativeStructure
from .analyzer import NarrativeAnalysis

class NarrativeClassifier:
    """Classifies narratives based on their structure and content."""
    
    def __init__(self):
        """Initialize the narrative classifier."""
        self.classifier = RandomForestClassifier()
        self.semantic_analyzer = ArabicSemanticAnalyzer()

    def extract_features(self, narrative: NarrativeStructure, 
                        analysis: NarrativeAnalysis) -> np.ndarray:
        """
        Extract features for classification.
        
        Args:
            narrative: NarrativeStructure object
            analysis: NarrativeAnalysis object
            
        Returns:
            Feature vector
        """
        features = [
            analysis.complexity_score,
            len(narrative.characters),
            len(narrative.events),
            narrative.frame_level,
            nx.density(analysis.character_network),
            len(narrative.themes),
            self._calculate_narrative_embedding(narrative)
        ]
        return np.array(features)

    def classify_narrative(self, narrative: NarrativeStructure, 
                         analysis: NarrativeAnalysis) -> Dict[str, float]:
        """
        Classify narrative into different categories.
        
        Args:
            narrative: NarrativeStructure object
            analysis: NarrativeAnalysis object
            
        Returns:
            Dictionary of classification probabilities
        """
        features = self.extract_features(narrative, analysis)
        
        # Classification categories
        categories = {
            "hero_journey": self._classify_hero_journey(features),
            "moral_tale": self._classify_moral_tale(features),
            "love_story": self._classify_love_story(features),
            "adventure": self._classify_adventure(features),
            "wisdom_tale": self._classify_wisdom_tale(features)
        }
        
        return categories

def main():
    """Demonstrate usage of narrative analysis modules."""
    # Example text
    text = """
    وفي يوم من الأيام، قال شهريار لشهرزاد: "حدثيني عن قصة الملك العادل."
    فقالت شهرزاد: "حسناً، سأحدثك عن ملك كان يحكم بالعدل والحكمة..."
    """
    
    # Extract narrative structure
    extractor = NarrativeExtractor()
    narrative = extractor.extract_structure(text, "قصة الملك العادل")
    
    # Analyze narrative
    analyzer = NarrativeAnalyzer()
    analysis = analyzer.analyze_narrative(narrative)
    
    # Classify narrative
    classifier = NarrativeClassifier()
    classifications = classifier.classify_narrative(narrative, analysis)
    
    print("Narrative Structure:", narrative)
    print("Analysis Results:", analysis)
    print("Classifications:", classifications)

if __name__ == '__main__':
    main()
