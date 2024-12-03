"""
Unit tests for Arabic text processor.
"""

import pytest
from anar.processor import ArabicProcessor
from anar.models import ProcessedText
from anar.utils import Validator

@pytest.fixture
def processor():
    """Create processor instance for testing."""
    return ArabicProcessor(
        model_path='models/test_model',
        vocab_size=1000,
        embedding_dim=128
    )

@pytest.fixture
def validator():
    """Create validator instance for testing."""
    return Validator()

class TestArabicProcessor:
    """Test Arabic text processing functionality."""
    
    @pytest.mark.parametrize("text,expected", [
        (
            "قال الملك شهريار",
            ["قال", "الملك", "شهريار"]
        ),
        (
            "يا أمير المؤمنين",
            ["يا", "أمير", "المؤمنين"]
        )
    ])
    async def test_tokenization(self, processor, text, expected):
        """Test text tokenization."""
        result = await processor.process_text(text)
        assert result.tokens == expected
        
    @pytest.mark.parametrize("text,expected_root", [
        ("مكتوب", "كتب"),
        ("يستغفر", "غفر")
    ])
    async def test_morphological_analysis(self, processor, text, expected_root):
        """Test morphological analysis."""
        result = await processor.process_text(text)
        assert result.morphemes[0]['root'] == expected_root
        
    def test_invalid_input(self, processor):
        """Test handling of invalid input."""
        with pytest.raises(ValueError):
            await processor.process_text("")
            
    def test_non_arabic_input(self, processor):
        """Test handling of non-Arabic input."""
        with pytest.raises(ValueError):
            await processor.process_text("Hello World")
            
    @pytest.mark.parametrize("text,expected_features", [
        (
            "السلام عليكم",
            {
                'type': 'greeting',
                'formality': 'high'
            }
        )
    ])
    async def test_feature_extraction(self, processor, text, expected_features):
        """Test feature extraction."""
        result = await processor.process_text(text)
        for key, value in expected_features.items():
            assert result.features[key] == value
```

Let's add tests for frame detection:


```python
"""
Unit tests for frame story detection.
"""

import pytest
from anar.processor import FrameDetector
from anar.models import Frame, ProcessedText

@pytest.fixture
def detector():
    """Create detector instance for testing."""
    return FrameDetector(
        model_path='models/test_frame',
        max_depth=6,
        attention_heads=8
    )

class TestFrameDetector:
    """Test frame story detection functionality."""
    
    @pytest.mark.parametrize("text,expected_level", [
        (
            "وحكت شهرزاد قائلةً: كان يا ما كان",
            1
        ),
        (
            "فقال التاجر: وفي ذلك اليوم",
            2
        )
    ])
    async def test_frame_level_detection(
        self,
        detector,
        text,
        expected_level
    ):
        """Test frame level detection."""
        processed = ProcessedText(
            original=text,
            normalized=text,
            tokens=text.split()
        )
        frames = await detector.detect_frames(processed)
        assert frames[0].level == expected_level
        
    def test_nested_frames(self, detector):
        """Test nested frame detection."""
        text = "فقال الملك: حدثني الوزير قائلاً: سمعت من التاجر"
        processed = ProcessedText(
            original=text,
            normalized=text,
            tokens=text.split()
        )
        frames = await detector.detect_frames(processed)
        assert len(frames) == 3  # Three levels of nesting
        assert [frame.level for frame in frames] == [0, 1, 2]
        
    def test_frame_relationships(self, detector):
        """Test frame relationship detection."""
        text = "قال الملك: وحكى الوزير"
        processed = ProcessedText(
            original=text,
            normalized=text,
            tokens=text.split()
        )
        frames = await detector.detect_frames(processed)
        assert frames[1].parent == frames[0]
        assert frames[0].children == [frames[1]]
        
    @pytest.mark.parametrize("text,expected_narrator", [
        (
            "قالت شهرزاد:",
            "شهرزاد"
        ),
        (
            "فحكى الوزير قائلاً:",
            "الوزير"
        )
    ])
    async def test_narrator_detection(
        self,
        detector,
        text,
        expected_narrator
    ):
        """Test narrator detection."""
        processed = ProcessedText(
            original=text,
            normalized=text,
            tokens=text.split()
        )
        frames = await detector.detect_frames(processed)
        assert frames[0].narrator == expected_narrator
```

Let's add tests for cultural analysis:


```python
"""
Unit tests for cultural element analysis.
"""

import pytest
from anar.processor import CulturalAnalyzer
from anar.models import CulturalElement, ProcessedText

@pytest.fixture
def analyzer():
    """Create analyzer instance for testing."""
    return CulturalAnalyzer(
        markers_path='data/test/cultural_markers.json',
        rules_path='data/test/preservation_rules.json'
    )

class TestCulturalAnalyzer:
    """Test cultural analysis functionality."""
    
    @pytest.mark.parametrize("text,expected_type,expected_significance", [
        (
            "يا أمير المؤمنين",
            "honorific",
            "high"
        ),
        (
            "السلام عليكم",
            "greeting",
            "high"
        )
    ])
    async def test_cultural_marker_detection(
        self,
        analyzer,
        text,
        expected_type,
        expected_significance
    ):
        """Test cultural marker detection."""
        processed = ProcessedText(
            original=text,
            normalized=text,
            tokens=text.split()
        )
        elements = await analyzer.analyze_cultural_elements(processed)
        assert elements[0].type == expected_type
        assert elements[0].significance == expected_significance
        
    def test_context_preservation(self, analyzer):
        """Test context preservation."""
        text = "مجلس السلطان"
        processed = ProcessedText(
            original=text,
            normalized=text,
            tokens=text.split()
        )
        elements = await analyzer.analyze_cultural_elements(processed)
        assert elements[0].context == "royal_court"
        assert "formal_setting" in elements[0].attributes
        
    def test_multiple_elements(self, analyzer):
        """Test multiple cultural element detection."""
        text = "يا مولاي السلطان أعز الله مقامك"
        processed = ProcessedText(
            original=text,
            normalized=text,
            tokens=text.split()
        )
        elements = await analyzer.analyze_cultural_elements(processed)
        assert len(elements) == 2  # Honorific and prayer
        assert {elem.type for elem in elements} == {
            "honorific",
            "prayer"
        }
        
    @pytest.mark.parametrize("text,expected_confidence", [
        (
            "بسم الله الرحمن الرحيم",
            0.95
        ),
        (
            "يا سيدي",
            0.90
        )
    ])
    async def test_confidence_scores(
        self,
        analyzer,
        text,
        expected_confidence
    ):
        """Test confidence score calculation."""
        processed = ProcessedText(
            original=text,
            normalized=text,
            tokens=text.split()
        )
        elements = await analyzer.analyze_cultural_elements(processed)
        assert elements[0].confidence >= expected_confidence
