# Arabic Narrative Analysis Framework

A comprehensive framework for analyzing, extracting, and processing narrative structures from Arabic texts, with a particular focus on the 1001 Arabian Nights collection.

## 🌟 Features

- Arabic text preprocessing and normalization
- Morphological, syntactic, and semantic analysis
- Narrative structure extraction
- Character and event network analysis
- Theme classification
- Multi-backend storage (Graph, Document, Vector)
- RESTful API interface

## 🔧 Installation

### Prerequisites

```bash
# Required system dependencies
python >= 3.8
neo4j >= 4.4
mongodb >= 5.0
elasticsearch >= 7.0

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

### Install Package

```bash
pip install -r requirements.txt
```

## 📦 Dependencies

```text
camel-tools>=3.0
spacy>=3.0
transformers>=4.0
torch>=1.9
fastapi>=0.68
neo4j>=4.4
pymongo>=3.12
elasticsearch>=7.0
networkx>=2.6
numpy>=1.19
scikit-learn>=0.24
pydantic>=1.8
uvicorn>=0.15
```

## 🏗️ Project Structure

```
arabic_narratives/
├── preprocessing/
│   ├── tokenizer.py     # Arabic text tokenization
│   ├── normalizer.py    # Text normalization
│   └── cleaner.py       # Text cleaning utilities
├── nlp/
│   ├── morphology.py    # Morphological analysis
│   ├── syntax.py        # Syntactic analysis
│   └── semantics.py     # Semantic analysis
├── narrative/
│   ├── extractor.py     # Narrative structure extraction
│   ├── analyzer.py      # Narrative analysis
│   └── classifier.py    # Theme classification
├── storage/
│   ├── graph_store.py   # Neo4j storage backend
│   ├── document_store.py # MongoDB storage backend
│   └── vector_store.py  # Elasticsearch storage backend
└── api/
    ├── routes.py        # API endpoints
    └── models.py        # API data models
```

## 🚀 Usage

### Starting the Services

```bash
# Start Neo4j
neo4j start

# Start MongoDB
mongod --dbpath /path/to/data

# Start Elasticsearch
elasticsearch
```

### Running the API

```bash
uvicorn arabic_narratives.api.routes:app --reload
```

### API Endpoints

#### Analyze Narrative
```bash
curl -X POST "http://localhost:8000/narratives/analyze" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "قصة الملك العادل",
       "text": "كان يا ما كان في قديم الزمان...",
       "source": "ألف ليلة وليلة"
     }'
```

#### Retrieve Narrative
```bash
curl "http://localhost:8000/narratives/{narrative_id}"
```

#### Search Similar Narratives
```bash
curl "http://localhost:8000/narratives/search?query=قصة%20عن%20ملك%20عادل"
```

## 📊 Example Analysis

```python
from arabic_narratives.narrative.extractor import NarrativeExtractor
from arabic_narratives.narrative.analyzer import NarrativeAnalyzer

# Initialize components
extractor = NarrativeExtractor()
analyzer = NarrativeAnalyzer()

# Analyze text
text = """
وفي يوم من الأيام، قال شهريار لشهرزاد: "حدثيني عن قصة الملك العادل."
فقالت شهرزاد: "حسناً، سأحدثك عن ملك كان يحكم بالعدل والحكمة..."
"""

# Extract and analyze
narrative = extractor.extract_structure(text, "قصة الملك العادل")
analysis = analyzer.analyze_narrative(narrative)

print(analysis)
```

## 🔍 Data Model

### Narrative Structure
```python
NarrativeStructure(
    title: str,
    frame_level: int,
    characters: List[Character],
    events: List[Event],
    settings: List[str],
    themes: List[str]
)
```

### Character
```python
Character(
    name: str,
    mentions: List[str],
    role: str,
    attributes: List[str],
    relationships: Dict[str, List[str]]
)
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- The 1001 Arabian Nights corpus
- CAMeL Tools for Arabic NLP
- Arabic-BERT project

## 📧 Contact

For questions and feedback, please contact:
- Email: [mibrahim@ucm.es.com]
- GitHub Issues: [Create an issue](https://github.com/Mossab82/arabic_narratives/issues)
