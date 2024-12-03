# ANAR API Reference

## Core Components

### ProcessingPipeline
Main processing pipeline for narrative analysis.


class ProcessingPipeline:
    def __init__(self, config: Optional[Dict] = None)
    
    async def process_text(
        self,
        text: str,
        metadata: Optional[Dict] = None
    ) -> PipelineResult
    
    async def process_batch(
        self,
        texts: List[str],
        batch_size: int = 5,
        parallel: bool = True
    ) -> List[NarrativeStructure]


### ArabicProcessor
Core processor for Arabic text analysis.


class ArabicProcessor:
    def __init__(
        self,
        model_path: str = 'models/morphological',
        vocab_size: int = 42_567,
        embedding_dim: int = 768,
        config: Optional[Dict] = None
    )
    
    async def process_text(
        self,
        text: str,
        preserve_diacritics: bool = True
    ) -> ProcessedText


### CulturalAnalyzer
Analyzer for cultural elements and context preservation.


class CulturalAnalyzer:
    def __init__(
        self,
        markers_path: str = 'data/cultural_markers.json',
        rules_path: str = 'data/preservation_rules.json'
    )
    
    async def analyze_cultural_elements(
        self,
        text: ProcessedText
    ) -> List[CulturalElement]


## Data Models

### NarrativeStructure

@dataclass
class NarrativeStructure:
    id: str
    title: Dict[str, str]  # Arabic/English
    frame_level: int
    metadata: StoryMetadata
    frames: List[Frame]
    cultural_elements: List[CulturalElement]


### ProcessedText

@dataclass
class ProcessedText:
    original: str
    normalized: str
    morphemes: List[Dict]
    features: np.ndarray
    metadata: Dict


## Utility Functions

### Validator

class Validator:
    def is_valid_arabic(self, text: str) -> bool
    def validate_network(self, G: nx.MultiDiGraph) -> bool
    def validate_frames(self, frames: List[Frame]) -> bool


### Optimizer

class Optimizer:
    @staticmethod
    def optimize_memory(func: Callable) -> Callable
    @staticmethod
    def optimize_processing(func: Callable) -> Callable
