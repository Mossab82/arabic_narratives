from typing import List, Dict, Any, Optional
import numpy as np
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from ..nlp.semantics import ArabicSemanticAnalyzer
from ..narrative.extractor import NarrativeStructure

class ElasticVectorStore:
    """Storage backend for narrative vectors using Elasticsearch."""
    
    def __init__(self, hosts: List[str], index_name: str = "narratives"):
        """
        Initialize Elasticsearch connection.
        
        Args:
            hosts: List of Elasticsearch hosts
            index_name: Name of the index to use
        """
        try:
            self.es = Elasticsearch(hosts)
            self.index_name = index_name
            self.semantic_analyzer = ArabicSemanticAnalyzer()
            self.create_index()
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Elasticsearch: {str(e)}")

    def create_index(self):
        """Create Elasticsearch index with vector mapping."""
        mapping = {
            "mappings": {
                "properties": {
                    "narrative_vector": {
                        "type": "dense_vector",
                        "dims": 768  # BERT embedding dimension
                    },
                    "title": {"type": "text"},
                    "text": {"type": "text"},
                    "metadata": {"type": "object"}
                }
            }
        }
        
        if not self.es.indices.exists(index=self.index_name):
            self.es.indices.create(index=self.index_name, body=mapping)

    def store_narrative(self, narrative: NarrativeStructure, 
                       full_text: str) -> str:
        """
        Store narrative vectors in Elasticsearch.
        
        Args:
            narrative: NarrativeStructure object
            full_text: Full text of the narrative
            
        Returns:
            ID of stored document
        """
        # Generate vector embedding
        vector = self.semantic_analyzer.get_embeddings(full_text)
        
        # Prepare document
        doc = {
            "narrative_vector": vector.tolist(),
            "title": narrative.title,
            "text": full_text,
            "metadata": {
                "frame_level": narrative.frame_level,
                "character_count": len(narrative.characters),
                "event_count": len(narrative.events),
                "themes": narrative.themes
            }
        }
        
        # Store document
        result = self.es.index(index=self.index_name, body=doc)
        return result["_id"]

    def find_similar_narratives(self, query_text: str, 
                              num_results: int = 5) -> List[Dict]:
        """
        Find similar narratives using vector similarity.
        
        Args:
            query_text: Text to find similar narratives for
            num_results: Number of results to return
            
        Returns:
            List of similar narratives with scores
        """
        query_vector = self.semantic_analyzer.get_embeddings(query_text)
        
        script_query = {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'narrative_vector') + 1.0",
                    "params": {"query_vector": query_vector.tolist()}
                }
            }
        }
        
        response = self.es.search(
            index=self.index_name,
            body={"query": script_query, "size": num_results}
        )
        
        return [
            {
                "id": hit["_id"],
                "title": hit["_source"]["title"],
                "score": hit["_score"],
                "metadata": hit["_source"]["metadata"]
            }
            for hit in response["hits"]["hits"]
        ]

def main():
    """Demonstrate usage of storage modules."""
    # Example narrative
    narrative = NarrativeStructure(
        title="قصة الملك العادل",
        frame_level=1,
        characters=[
            Character(
                name="الملك",
                mentions=["الملك", "الحاكم"],
                role="protagonist",
                attributes=["عادل", "حكيم"],
                relationships={"الوزير": ["مستشار"]}
            )
        ],
        events=[
            Event(
                text="حكم الملك بالعدل",
                type="action",
                participants=["الملك"],
                time_markers=["ذات يوم"],
                location="القصر"
            )
        ],
        settings=["القصر", "المدينة"],
        themes=["العدل", "الحكمة"]
    )
    
    # Store in Neo4j
    graph_store = NeoGraphStore("bolt://localhost:7687", "neo4j", "password")
    graph_id = graph_store.store_narrative(narrative)
    print(f"Stored in Neo4j with ID: {graph_id}")
    
    # Store in MongoDB
    doc_store = MongoDocumentStore("mongodb://localhost:27017", "narratives")
    doc_id = doc_store.store_narrative(narrative)
    print(f"Stored in MongoDB with ID: {doc_id}")
    
    # Store in Elasticsearch
    vector_store = ElasticVectorStore(["http://localhost:9200"])
    vector_id = vector_store.store_narrative(narrative, "حكم الملك بالعدل والحكمة")
    print(f"Stored in Elasticsearch with ID: {vector_id}")
    
    # Find similar narratives
    similar = vector_store.find_similar_narratives("قصة عن ملك عادل")
    print("Similar narratives:", similar)

if __name__ == '__main__':
    main()
