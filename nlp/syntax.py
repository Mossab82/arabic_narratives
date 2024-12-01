from typing import List, Dict, Any
from dataclasses import dataclass
import spacy
from camel_tools.disambig.mle import MLEDisambiguator

@dataclass
class SyntacticDependency:
    """Data class for syntactic dependencies between words."""
    head: str          # Head word
    dependent: str     # Dependent word
    relation: str      # Dependency relation type
    head_pos: str      # Head part of speech
    dep_pos: str       # Dependent part of speech

class ArabicSyntaxAnalyzer:
    """Analyzer for Arabic syntactic structure."""
    
    def __init__(self):
        """Initialize the syntax analyzer with required models."""
        try:
            self.nlp = spacy.load("xx_ent_wiki_sm")  # Multilingual model
            self.mle = MLEDisambiguator.pretrained()
        except Exception as e:
            raise RuntimeError(f"Failed to initialize syntax analyzer: {str(e)}")

    def analyze_dependencies(self, text: str) -> List[SyntacticDependency]:
        """
        Analyze syntactic dependencies in text.
        
        Args:
            text: Input Arabic text
            
        Returns:
            List of syntactic dependencies
        """
        doc = self.nlp(text)
        dependencies = []
        
        for token in doc:
            if token.dep_ != "ROOT":
                dependency = SyntacticDependency(
                    head=token.head.text,
                    dependent=token.text,
                    relation=token.dep_,
                    head_pos=token.head.pos_,
                    dep_pos=token.pos_
                )
                dependencies.append(dependency)
                
        return dependencies

    def analyze_sentence_structure(self, text: str) -> Dict[str, Any]:
        """
        Analyze overall sentence structure.
        
        Args:
            text: Input Arabic text
            
        Returns:
            Dictionary containing sentence structure analysis
        """
        doc = self.nlp(text)
        
        structure = {
            'sentence_type': self._determine_sentence_type(doc),
            'main_verb': self._find_main_verb(doc),
            'subject': self._find_subject(doc),
            'objects': self._find_objects(doc),
            'clauses': self._identify_clauses(doc)
        }
        
        return structure

    def _determine_sentence_type(self, doc) -> str:
        """Determine the type of sentence (verbal, nominal, etc.)."""
        # Implementation based on Arabic sentence structure rules
        first_token = doc[0]
        if first_token.pos_ == "VERB":
            return "verbal"
        return "nominal"

    def _find_main_verb(self, doc) -> str:
        """Find the main verb in the sentence."""
        for token in doc:
            if token.dep_ == "ROOT" and token.pos_ == "VERB":
                return token.text
        return ""

    def _find_subject(self, doc) -> str:
        """Find the subject of the sentence."""
        for token in doc:
            if token.dep_ == "nsubj":
                return token.text
        return ""

    def _find_objects(self, doc) -> List[str]:
        """Find objects in the sentence."""
        objects = []
        for token in doc:
            if token.dep_ in ["dobj", "iobj"]:
                objects.append(token.text)
        return objects

    def _identify_clauses(self, doc) -> List[str]:
        """Identify clauses in the sentence."""
        clauses = []
        current_clause = []
        
        for token in doc:
            if token.dep_ == "ROOT" or token.dep_.endswith("cl"):
                if current_clause:
                    clauses.append(" ".join(current_clause))
                    current_clause = []
            current_clause.append(token.text)
            
        if current_clause:
            clauses.append(" ".join(current_clause))
            
        return clauses
