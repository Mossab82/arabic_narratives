"""
Tests for cultural analysis and preservation functionality.
"""

import pytest
import json
from anar.processor import CulturalAnalyzer
from anar.models import ProcessedText, CulturalElement
from anar.utils import Validator

@pytest.fixture
def analyzer():
    """Create cultural analyzer for testing."""
    return CulturalAnalyzer(
        markers_path='data/test/cultural_markers.json',
        rules_path='data/test/preservation_rules.json'
    )

@pytest.fixture
def validation_data():
    """Load validation data."""
    with open('data/validation/validation_sets.json', 'r', encoding='utf-8') as f:
        return json.load(f)

class TestCulturalAnalysis:
    """Test cultural analysis functionality."""
    
    @pytest.mark.parametrize("text,expected_type,expected_context", [
        (
            "يا أمير المؤمنين",
            "honorific",
            "royal_address"
        ),
        (
            "السلام عليكم ورحمة الله",
            "greeting",
            "formal_greeting"
        ),
        (
            "بسم الله الرحمن الرحيم",
            "religious",
            "opening_phrase"
        )
    ])
    async def test_marker_detection(
        self,
        analyzer,
        text,
        expected_type,
        expected_context
    ):
        """Test cultural marker detection."""
        processed = ProcessedText(
            original=text,
            normalized=text,
            tokens=text.split()
        )
        
        elements = await analyzer.analyze_cultural_elements(processed)
        assert elements[0].type == expected_type
        assert elements[0].context == expected_context
        
    async def test_context_relationships(self, analyzer):
        """Test cultural context relationships."""
        text = "قال الملك لوزيره: يا وزيري الأمين"
        processed = ProcessedText(
            original=text,
            normalized=text,
            tokens=text.split()
        )
        
        elements = await analyzer.analyze_cultural_elements(processed)
        relationships = analyzer.get_context_relationships(elements)
        
        assert "hierarchy" in relationships
        assert relationships["hierarchy"]["ruler_to_minister"] is True
        
    @pytest.mark.parametrize("text,expected_count", [
        (
            "يا مولاي السلطان أعز الله مقامك",
            3  # honorific, title, prayer
        ),
        (
            "بسم الله الرحمن الرحيم. السلام عليكم",
            2  # opening phrase, greeting
        )
    ])
    async def test_multiple_markers(
        self,
        analyzer,
        text,
        expected_count
    ):
        """Test detection of multiple cultural markers."""
        processed = ProcessedText(
            original=text,
            normalized=text,
            tokens=text.split()
        )
        
        elements = await analyzer.analyze_cultural_elements(processed)
        assert len(elements) == expected_count
        
    def test_preservation_rules(self, analyzer, validation_data):
        """Test cultural preservation rules."""
        for case in validation_data['cultural_validation']['honorifics']:
            text = case['text']
            expected = case['expected']
            
            processed = ProcessedText(
                original=text,
                normalized=text,
                tokens=text.split()
            )
            
            elements = await analyzer.analyze_cultural_elements(processed)
            assert elements[0].type == expected['type']
            assert elements[0].status == expected['status']
            
    async def test_confidence_thresholds(self, analyzer):
        """Test confidence threshold handling."""
        text = "ربما كان ذلك في مجلس"  # Ambiguous context
        processed = ProcessedText(
            original=text,
            normalized=text,
            tokens=text.split()
        )
        
        # Test with different thresholds
        elements_strict = await analyzer.analyze_cultural_elements(
            processed,
            confidence_threshold=0.9
        )
        elements_lenient = await analyzer.analyze_cultural_elements(
            processed,
            confidence_threshold=0.6
        )
        
        assert len(elements_strict) < len(elements_lenient)
        
    def test_cultural_attributes(self, analyzer):
        """Test cultural attribute extraction."""
        text = "في قصر السلطان في بغداد"
        processed = ProcessedText(
            original=text,
            normalized=text,
            tokens=text.split()
        )
        
        elements = await analyzer.analyze_cultural_elements(processed)
        
        # Check location attributes
        location_element = next(
            e for e in elements if e.type == "location"
        )
        assert location_element.attributes["region"] == "Baghdad"
        assert location_element.attributes["setting"] == "royal_palace"
        
    @pytest.mark.parametrize("text,expected_period", [
        (
            "في عهد هارون الرشيد",
            "Abbasid"
        ),
        (
            "في زمن الخلافة العباسية",
            "Abbasid"
        )
    ])
    async def test_historical_context(
        self,
        analyzer,
        text,
        expected_period
    ):
        """Test historical context detection."""
        processed = ProcessedText(
            original=text,
            normalized=text,
            tokens=text.split()
        )
        
        elements = await analyzer.analyze_cultural_elements(processed)
        assert elements[0].historical_context["period"] == expected_period
