# ANAR User Guide

## Installation


pip install anar


## Quick Start

### Basic Usage

from anar.pipeline import ProcessingPipeline

# Initialize pipeline
pipeline = ProcessingPipeline()

# Process text
text = "قال الملك شهريار لشهرزاد: حدثيني حديثاً"
result = await pipeline.process_text(text)

# Access results
print(f"Frames detected: {len(result.narrative.frames)}")
print(f"Cultural elements: {len(result.narrative.cultural_elements)}")


### Batch Processing

# Process multiple texts
texts = ["text1", "text2", "text3"]
results = await pipeline.process_batch(
    texts,
    batch_size=2,
    parallel=True
)


## Advanced Features

### Custom Pipeline Configuration

config = {
    'text_model_path': 'models/custom_model',
    'max_depth': 6,
    'attention_heads': 12
}
pipeline = ProcessingPipeline(config=config)


### Cultural Analysis

# Analyze cultural elements
elements = result.narrative.cultural_elements
for element in elements:
    print(f"Type: {element.type}")
    print(f"Context: {element.context}")


## Best Practices

1. Text Preparation
   - Use UTF-8 encoding
   - Maintain diacritical marks
   - Preserve original formatting

2. Performance Optimization
   - Use batch processing for multiple texts
   - Enable parallel processing when possible
   - Implement checkpointing for large datasets

3. Error Handling
   - Validate input text
   - Check confidence scores
   - Monitor resource usage

## Troubleshooting

Common issues and solutions:

1. Invalid Input
  
   # Ensure valid Arabic text
   if not Validator().is_valid_arabic(text):
       raise ValueError("Invalid Arabic text")
 

2. Memory Issues
  
   # Use memory optimization
   @Optimizer.optimize_memory
   def process_large_text(text):
       return pipeline.process_text(text)


## Examples

See `examples/` directory for complete usage examples:
- `basic_usage.py`: Simple processing examples
- `advanced_features.py`: Advanced functionality
