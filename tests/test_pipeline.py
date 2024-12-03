"""
Integration tests for the ANAR pipeline system.
"""

import pytest
import json
from pathlib import Path
from anar.pipeline import ProcessingPipeline
from anar.models import NarrativeStructure
from anar.utils import Validator

@pytest.fixture
def pipeline():
    """Create pipeline instance for testing."""
    config = {
        'text_model_path': 'models/test/text_model',
        'frame_model_path': 'models/test/frame_model',
        'markers_path': 'data/test/cultural_markers.json',
        'rules_path': 'data/test/preservation_rules.json'
    }
    return ProcessingPipeline(config=config)

@pytest.fixture
def test_data():
    """Load test data."""
    with open('data/test/test_cases.json', 'r', encoding='utf-8') as f:
        return json.load(f)

class TestProcessingPipeline:
    """Test complete processing pipeline."""
    
    async def test_end_to_end_processing(self, pipeline, test_data):
        """Test complete pipeline processing."""
        # Test basic story processing
        text = test_data['text_processing']['basic_cases'][0]['input']
        result = await pipeline.process_text(text)
        
        assert isinstance(result.narrative, NarrativeStructure)
        assert result.processing_time > 0
        assert len(result.metrics) > 0
        
    async def test_batch_processing(self, pipeline, test_data):
        """Test batch processing capability."""
        texts = [
            case['input']
            for case in test_data['text_processing']['basic_cases']
        ]
        
        results = await pipeline.process_batch(
            texts,
            batch_size=2,
            parallel=True
        )
        
        assert len(results) == len(texts)
        assert all(isinstance(r, NarrativeStructure) for r in results)
        
    async def test_checkpoint_recovery(self, pipeline, test_data):
        """Test checkpoint and recovery functionality."""
        texts = [
            case['input']
            for case in test_data['text_processing']['basic_cases']
        ]
        
        # Process with checkpoints
        results = await pipeline.process_batch(
            texts,
            checkpoint_dir='data/test/checkpoints'
        )
        
        # Verify checkpoint files
        checkpoint_files = list(Path('data/test/checkpoints').glob('*.pkl'))
        assert len(checkpoint_files) > 0
        
        # Test recovery
        recovered = pipeline._load_checkpoint(0)
        assert recovered is not None
        assert len(recovered) > 0
        
    @pytest.mark.parametrize("stage", [
        "text_processing",
        "frame_detection",
        "cultural_analysis"
    ])
    async def test_stage_validation(self, pipeline, test_data, stage):
        """Test validation at each pipeline stage."""
        text = test_data['text_processing']['basic_cases'][0]['input']
        
        # Process with specific stage validation
        result = await pipeline.process_text(
            text,
            validate_stages=[stage]
        )
        
        assert result.metrics[stage]['validation_passed']
        
    def test_error_handling(self, pipeline):
        """Test pipeline error handling."""
        # Test with invalid input
        with pytest.raises(ValueError):
            await pipeline.process_text("")
            
        # Test with non-Arabic text
        with pytest.raises(ValueError):
            await pipeline.process_text("Hello World")
            
    async def test_resource_monitoring(self, pipeline, test_data):
        """Test resource monitoring during processing."""
        text = test_data['text_processing']['basic_cases'][0]['input']
        
        # Process with resource monitoring
        result = await pipeline.process_text(
            text,
            monitor_resources=True
        )
        
        assert 'memory_usage' in result.metrics
        assert 'processing_time' in result.metrics
        
    async def test_cultural_preservation(self, pipeline, test_data):
        """Test cultural preservation in pipeline."""
        # Test with cultural markers
        text = test_data['cultural_markers'][0]['input']
        result = await pipeline.process_text(text)
        
        assert len(result.narrative.cultural_elements) > 0
        assert result.narrative.cultural_elements[0].confidence > 0.8
        
    async def test_frame_structure(self, pipeline, test_data):
        """Test frame structure detection in pipeline."""
        # Test with nested frames
        text = test_data['frame_detection']['nested_frames'][0]['text']
        result = await pipeline.process_text(text)
        
        expected_levels = test_data['frame_detection']['nested_frames'][0]['expected']['levels']
        assert len(result.narrative.frames) == expected_levels
        
    @pytest.mark.parametrize("config_override", [
        {"max_depth": 3},
        {"batch_size": 5},
        {"parallel": False}
    ])
    async def test_configuration(self, pipeline, test_data, config_override):
        """Test pipeline configuration options."""
        pipeline.config.update(config_override)
        text = test_data['text_processing']['basic_cases'][0]['input']
        result = await pipeline.process_text(text)
        
        assert result is not None
