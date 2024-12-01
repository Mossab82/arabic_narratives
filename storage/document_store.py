from typing import Dict, List, Any, Optional
from datetime import datetime
import pymongo
from bson import ObjectId
from ..narrative.extractor import NarrativeStructure

class MongoDocumentStore:
    """Storage backend for narrative documents using MongoDB."""
    
    def __init__(self, uri: str, database: str):
        """
        Initialize MongoDB connection.
        
        Args:
            uri: MongoDB connection URI
            database: Database name
        """
        try:
            self.client = pymongo.MongoClient(uri)
            self.db = self.client[database]
            self.narratives = self.db.narratives
            self.create_indexes()
        except Exception as e:
            raise ConnectionError(f"Failed to connect to MongoDB: {str(e)}")

    def create_indexes(self):
        """Create necessary indexes for efficient querying."""
        self.narratives.create_index([("title", pymongo.TEXT)])
        self.narratives.create_index([("frame_level", pymongo.ASCENDING)])
        self.narratives.create_index([("characters.name", pymongo.ASCENDING)])

    def store_narrative(self, narrative: NarrativeStructure) -> str:
        """
        Store narrative document in MongoDB.
        
        Args:
            narrative: NarrativeStructure object
            
        Returns:
            ID of stored document
        """
        doc = {
            "title": narrative.title,
            "frame_level": narrative.frame_level,
            "characters": [asdict(c) for c in narrative.characters],
            "events": [asdict(e) for e in narrative.events],
            "settings": narrative.settings,
            "themes": narrative.themes,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = self.narratives.insert_one(doc)
        return str(result.inserted_id)

    def find_narrative(self, narrative_id: str) -> Optional[Dict]:
        """Retrieve narrative by ID."""
        return self.narratives.find_one({"_id": ObjectId(narrative_id)})

    def find_by_character(self, character_name: str) -> List[Dict]:
        """Find narratives containing a specific character."""
        return list(self.narratives.find({"characters.name": character_name}))

    def update_narrative(self, narrative_id: str, update_data: Dict) -> bool:
        """Update narrative document."""
        update_data["updated_at"] = datetime.utcnow()
        result = self.narratives.update_one(
            {"_id": ObjectId(narrative_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0
