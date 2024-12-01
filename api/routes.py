from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from .models import (
    NarrativeInputModel,
    NarrativeAnalysisModel,
    CharacterModel,
    EventModel
)
from ..narrative.extractor import NarrativeExtractor, NarrativeStructure
from ..narrative.analyzer import NarrativeAnalyzer
from ..narrative.classifier import NarrativeClassifier
from ..storage.graph_store import NeoGraphStore
from ..storage.document_store import MongoDocumentStore
from ..storage.vector_store import ElasticVectorStore

app = FastAPI(
    title="Arabic Narratives API",
    description="API for analyzing and storing Arabic narrative structures",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencies
def get_narrative_processor():
    """Get narrative processing components."""
    extractor = NarrativeExtractor()
    analyzer = NarrativeAnalyzer()
    classifier = NarrativeClassifier()
    return extractor, analyzer, classifier

def get_storage():
    """Get storage backends."""
    graph_store = NeoGraphStore(
        uri="bolt://localhost:7687",
        user="neo4j",
        password="password"
    )
    doc_store = MongoDocumentStore(
        uri="mongodb://localhost:27017",
        database="narratives"
    )
    vector_store = ElasticVectorStore(
        hosts=["http://localhost:9200"]
    )
    return graph_store, doc_store, vector_store

@app.post("/narratives/analyze", response_model=NarrativeAnalysisModel)
async def analyze_narrative(
    narrative: NarrativeInputModel,
    processors: tuple = Depends(get_narrative_processor),
    storage: tuple = Depends(get_storage)
):
    """
    Analyze an Arabic narrative text and store the results.
    
    Parameters:
    - narrative: Input narrative text and metadata
    
    Returns:
    - Complete narrative analysis
    """
    extractor, analyzer, classifier = processors
    graph_store, doc_store, vector_store = storage
    
    try:
        # Extract narrative structure
        structure = extractor.extract_structure(
            text=narrative.text,
            title=narrative.title
        )
        
        # Analyze and classify
        analysis = analyzer.analyze_narrative(structure)
        classifications = classifier.classify_narrative(structure, analysis)
        
        # Store results
        graph_id = graph_store.store_narrative(structure)
        doc_id = doc_store.store_narrative(structure)
        vector_id = vector_store.store_narrative(structure, narrative.text)
        
        # Prepare response
        return NarrativeAnalysisModel(
            narrative_id=doc_id,  # Use MongoDB ID as primary reference
            title=narrative.title,
            characters=[CharacterModel(**c.__dict__) for c in structure.characters],
            events=[EventModel(**e.__dict__) for e in structure.events],
            themes=structure.themes,
            complexity_score=analysis.complexity_score,
            classification=classifications,
            created_at=datetime.utcnow()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing narrative: {str(e)}"
        )

@app.get("/narratives/{narrative_id}", response_model=NarrativeAnalysisModel)
async def get_narrative(
    narrative_id: str,
    storage: tuple = Depends(get_storage)
):
    """
    Retrieve a stored narrative analysis by ID.
    
    Parameters:
    - narrative_id: ID of the stored narrative
    
    Returns:
    - Complete narrative analysis
    """
    _, doc_store, _ = storage
    
    try:
        narrative = doc_store.find_narrative(narrative_id)
        if not narrative:
            raise HTTPException(
                status_code=404,
                detail=f"Narrative {narrative_id} not found"
            )
        return NarrativeAnalysisModel(**narrative)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving narrative: {str(e)}"
        )

@app.get("/narratives/search", response_model=List[NarrativeAnalysisModel])
async def search_similar_narratives(
    query: str,
    limit: int = 5,
    storage: tuple = Depends(get_storage)
):
    """
    Search for similar narratives using semantic similarity.
    
    Parameters:
    - query: Search query text
    - limit: Maximum number of results to return
    
    Returns:
    - List of similar narratives
    """
    _, doc_store, vector_store = storage
    
    try:
        similar = vector_store.find_similar_narratives(query, limit)
        narratives = []
        
        for hit in similar:
            narrative = doc_store.find_narrative(hit["id"])
            if narrative:
                narrative["similarity_score"] = hit["score"]
                narratives.append(NarrativeAnalysisModel(**narrative))
                
        return narratives
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error searching narratives: {str(e)}"
        )

@app.get("/narratives/character/{character_name}", response_model=List[NarrativeAnalysisModel])
async def find_narratives_by_character(
    character_name: str,
    storage: tuple = Depends(get_storage)
):
    """
    Find narratives containing a specific character.
    
    Parameters:
    - character_name: Name of the character to search for
    
    Returns:
    - List of narratives featuring the character
    """
    _, doc_store, _ = storage
    
    try:
        narratives = doc_store.find_by_character(character_name)
        return [NarrativeAnalysisModel(**n) for n in narratives]
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error searching narratives: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
