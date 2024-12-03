"""
Core pipeline implementation for the ANAR system.
Orchestrates the complete narrative analysis workflow.
"""

import logging
from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from datetime import datetime

from ..processor import ArabicProcessor, FrameDetector, CulturalAnalyzer
from ..models import (
    NarrativeStructure,
    ProcessedText,
    Frame,
    CulturalElement
)
from ..utils import Validator, Optimizer, ErrorHandler

@dataclass
class PipelineResult:
    """Container for pipeline processing results."""
    narrative: NarrativeStructure
    processing_time: float
    metrics: Dict
    timestamp: datetime = datetime.now()

class ProcessingPipeline:
    """
    Main processing pipeline for narrative analysis.
    
    Features:
    - Multi-stage processing
    - Progress tracking
    - Performance monitoring
    - Error recovery
    """
    
    def __init__(
        self,
        config: Optional[Dict] = None
    ):
        self.logger = logging.getLogger(__name__)
        self.validator = Validator()
        self.optimizer = Optimizer()
        self.error_handler = ErrorHandler()
        
        # Initialize processors
        self.text_processor = ArabicProcessor()
        self.frame_detector = FrameDetector()
        self.cultural_analyzer = CulturalAnalyzer()
        
        self.config = config or {}
        
    @Optimizer.optimize_memory
    async def process_text(
        self,
        text: str,
        metadata: Optional[Dict] = None
    ) -> PipelineResult:
        """
        Process text through complete pipeline.
        
        Args:
            text: Input Arabic text
            metadata: Additional metadata
            
        Returns:
            Complete processing results
        """
        start_time = datetime.now()
        
        try:
            # Stage 1: Text Processing
            self.logger.info("Starting text processing")
            processed_text = await self._process_text(text)
            
            # Stage 2: Frame Detection
            self.logger.info("Starting frame detection")
            frames = await self._detect_frames(processed_text)
            
            # Stage 3: Cultural Analysis
            self.logger.info("Starting cultural analysis")
            cultural_elements = await self._analyze_cultural(
                processed_text,
                frames
            )
            
            # Stage 4: Network Construction
            self.logger.info("Starting network construction")
            network = self._build_network(
                frames,
                cultural_elements
            )
            
            # Create narrative structure
            narrative = NarrativeStructure(
                id=self._generate_id(),
                title=self._extract_title(processed_text),
                frame_level=len(frames),
                metadata=metadata or {},
                frames=frames,
                cultural_elements=cultural_elements,
                network=network
            )
            
            # Validate results
            if not self.validator.validate_narrative_structure(
                narrative
            ):
                raise ValueError("Invalid narrative structure")
                
            processing_time = (
                datetime.now() - start_time
            ).total_seconds()
            
            return PipelineResult(
                narrative=narrative,
                processing_time=processing_time,
                metrics=self._collect_metrics()
            )
            
        except Exception as e:
            self.logger.error(f"Pipeline error: {e}")
            return self.error_handler.handle_pipeline_error(e)
            
    async def _process_text(
        self,
        text: str
    ) -> ProcessedText:
        """Process raw text."""
        return await self.text_processor.process_text(text)
        
    async def _detect_frames(
        self,
        text: ProcessedText
    ) -> List[Frame]:
        """Detect frame stories."""
        return await self.frame_detector.detect_frames(text)
        
    async def _analyze_cultural(
        self,
        text: ProcessedText,
        frames: List[Frame]
    ) -> List[CulturalElement]:
        """Analyze cultural elements."""
        return await self.cultural_analyzer.analyze_cultural_elements(
            text,
            frames
        )
        
    def _build_network(
        self,
        frames: List[Frame],
        cultural_elements: List[CulturalElement]
    ) -> Dict:
        """Build narrative network."""
        network = {
            'nodes': [],
            'edges': []
        }
        
        # Add frame nodes
        for frame in frames:
            network['nodes'].append({
                'id': frame.id,
                'type': 'frame',
                'level': frame.level
            })
            
            # Add frame relationships
            if frame.parent:
                network['edges'].append({
                    'source': frame.parent.id,
                    'target': frame.id,
                    'type': 'contains'
                })
                
        # Add cultural element nodes
        for element in cultural_elements:
            network['nodes'].append({
                'id': element.id,
                'type': 'cultural',
                'element_type': element.type
            })
            
        return network
        
    def _collect_metrics(self) -> Dict:
        """Collect processing metrics."""
        return {
            'text_processor': self.text_processor.get_metrics(),
            'frame_detector': self.frame_detector.get_metrics(),
            'cultural_analyzer': self.cultural_analyzer.get_metrics()
        }
        
    @staticmethod
    def _generate_id() -> str:
        """Generate unique narrative ID."""
        import uuid
        return f"NAR-{uuid.uuid4().hex[:8]}"
        
    @staticmethod
    def _extract_title(
        text: ProcessedText
    ) -> Dict[str, str]:
        """Extract narrative title."""
        # Implementation for title extraction
        pass
