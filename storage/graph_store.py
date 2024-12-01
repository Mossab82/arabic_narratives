from typing import Dict, List, Any, Optional
from dataclasses import asdict
import networkx as nx
from neo4j import GraphDatabase
from ..narrative.extractor import NarrativeStructure, Character, Event

class NeoGraphStore:
    """Storage backend for narrative graphs using Neo4j."""
    
    def __init__(self, uri: str, user: str, password: str):
        """
        Initialize Neo4j connection.
        
        Args:
            uri: Neo4j server URI
            user: Username for authentication
            password: Password for authentication
        """
        try:
            self.driver = GraphDatabase.driver(uri, auth=(user, password))
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Neo4j: {str(e)}")

    def store_narrative(self, narrative: NarrativeStructure) -> str:
        """
        Store complete narrative structure in Neo4j.
        
        Args:
            narrative: NarrativeStructure object
            
        Returns:
            ID of stored narrative
        """
        with self.driver.session() as session:
            # Create narrative node
            narrative_id = session.write_transaction(
                self._create_narrative_node,
                asdict(narrative)
            )
            
            # Store characters
            for character in narrative.characters:
                session.write_transaction(
                    self._create_character_node,
                    narrative_id,
                    asdict(character)
                )
            
            # Store events
            for event in narrative.events:
                session.write_transaction(
                    self._create_event_node,
                    narrative_id,
                    asdict(event)
                )
            
            return narrative_id

    def _create_narrative_node(self, tx, narrative_data: Dict) -> str:
        """Create narrative node in Neo4j."""
        query = """
        CREATE (n:Narrative {
            title: $title,
            frame_level: $frame_level,
            settings: $settings,
            themes: $themes
        })
        RETURN id(n) as narrative_id
        """
        result = tx.run(query, **narrative_data)
        return result.single()["narrative_id"]

    def _create_character_node(self, tx, narrative_id: str, character_data: Dict):
        """Create character node and relationships."""
        query = """
        MATCH (n:Narrative) WHERE id(n) = $narrative_id
        CREATE (c:Character {
            name: $name,
            role: $role,
            attributes: $attributes
        })-[:APPEARS_IN]->(n)
        """
        tx.run(query, narrative_id=narrative_id, **character_data)

    def _create_event_node(self, tx, narrative_id: str, event_data: Dict):
        """Create event node and relationships."""
        query = """
        MATCH (n:Narrative) WHERE id(n) = $narrative_id
        CREATE (e:Event {
            text: $text,
            type: $type,
            time_markers: $time_markers,
            location: $location
        })-[:PART_OF]->(n)
        """
        tx.run(query, narrative_id=narrative_id, **event_data)
