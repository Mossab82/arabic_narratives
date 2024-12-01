from typing import List, Dict, Any
import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity

class ArabicSemanticAnalyzer:
    """Analyzer for Arabic semantic features using transformer models."""
    
    def __init__(self, model_name: str = "asafaya/bert-base-arabic"):
        """
        Initialize the semantic analyzer.
        
        Args:
            model_name: Name of the pretrained model to use
        """
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModel.from_pretrained(model_name)
            self.model.eval()
        except Exception as e:
            raise RuntimeError(f"Failed to initialize semantic analyzer: {str(e)}")

    def get_embeddings(self, text: str) -> np.ndarray:
        """
        Generate embeddings for input text.
        
        Args:
            text: Input Arabic text
            
        Returns:
            Numpy array of embeddings
        """
        with torch.no_grad():
            inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True)
            outputs = self.model(**inputs)
            embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
            
        return embeddings

    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate semantic similarity between two texts.
        
        Args:
            text1: First input text
            text2: Second input text
            
        Returns:
            Similarity score between 0 and 1
        """
        emb1 = self.get_embeddings(text1).reshape(1, -1)
        emb2 = self.get_embeddings(text2).reshape(1, -1)
        
        similarity = cosine_similarity(emb1, emb2)[0][0]
        return float(similarity)

    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """
        Analyze sentiment of Arabic text.
        
        Args:
            text: Input Arabic text
            
        Returns:
            Dictionary containing sentiment scores
        """
        # Using a simple rule-based approach for demonstration
        # In practice, you would use a fine-tuned model for Arabic sentiment
        positive_words = {"جميل", "رائع", "ممتاز", "جيد"}
        negative_words = {"سيء", "قبيح", "رديء", "ضعيف"}
        
        words = set(text.split())
        pos_count = len(words.intersection(positive_words))
        neg_count = len(words.intersection(negative_words))
        total = pos_count + neg_count or 1
        
        return {
            "positive": pos_count / total,
            "negative": neg_count / total,
            "neutral": 1 - (pos_count + neg_count) / len(words)
        }

def main():
    """Demonstrate usage of NLP modules."""
    # Example text
    text = "وقال شهريار لشهرزاد: حدثيني حديثا جميلا عن الملك العادل"
    
    # Morphological analysis
    morph_analyzer = ArabicMorphologyAnalyzer()
    morph_analysis = morph_analyzer.analyze_text(text)
    print("Morphological Analysis:", morph_analysis)
    
    # Syntactic analysis
    syntax_analyzer = ArabicSyntaxAnalyzer()
    dependencies = syntax_analyzer.analyze_dependencies(text)
    structure = syntax_analyzer.analyze_sentence_structure(text)
    print("Syntactic Dependencies:", dependencies)
    print("Sentence Structure:", structure)
    
    # Semantic analysis
    semantic_analyzer = ArabicSemanticAnalyzer()
    embeddings = semantic_analyzer.get_embeddings(text)
    sentiment = semantic_analyzer.analyze_sentiment(text)
    print("Embeddings shape:", embeddings.shape)
    print("Sentiment:", sentiment)

if __name__ == '__main__':
    main()
