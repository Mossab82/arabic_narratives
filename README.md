ANAR: # ANAR: Arabic Narrative Analysis and Recognition System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## Overview

ANAR (Arabic Narrative Analysis and Recognition) is a comprehensive framework for analyzing and extracting narrative structures from classical Arabic texts, with a specific focus on the 1001 Arabian Nights. The system combines traditional narratological approaches with modern computational methods to preserve both structural and cultural elements of Arabic storytelling.

## Features

- **Advanced Text Processing**: Specialized morphological analysis for classical Arabic
- **Frame Story Detection**: Automated detection of narrative structures and hierarchies
- **Cultural Preservation**: Context-aware processing maintaining cultural elements
- **Network Analysis**: Character and event relationship mapping
- **Batch Processing**: Efficient processing of multiple texts
- **Performance Optimization**: Memory and processing optimizations

## Installation


pip install anar


## Quick Start


from anar.pipeline import ProcessingPipeline

# Initialize pipeline
pipeline = ProcessingPipeline()

# Process text
text = "قال الملك شهريار لشهرزاد: حدثيني حديثاً"
result = await pipeline.process_text(text)

# Access results
print(f"Frames detected: {len(result.narrative.frames)}")
print(f"Cultural elements: {len(result.narrative.cultural_elements)}")


## Documentation

- [User Guide](docs/user_guide.md)
- [API Reference](docs/api_reference.md)
- [Examples](examples/)

## Citation


@article{ibrahim2024anar,
    title={ANAR: Arabic Narrative Analysis and Recognition System with Application to the 1001 Arabian Nights},
    author={Ibrahim, Mossab and Gervás, Pablo and Méndez, Gonzalo},
    journal={LREC-COLING},
    year={2024}
}


## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Faculty of Informatics - Universidad Complutense de Madrid
- Institute of Knowledge Technology - Universidad Complutense de Madrid

## Contact

- Mossab Ibrahim - mibrahim@ucm.es

## Project Status

Under active development. See [Issues](https://github.com/Mossab82/arabic_narratives/issues) for current tasks and plans. Narrative Analysis and Recognition System
