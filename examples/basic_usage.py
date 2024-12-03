"""
Basic usage examples for the ANAR system.
Demonstrates core functionality and simple workflows.
"""

import asyncio
from anar.pipeline import ProcessingPipeline
from anar.utils import Logger

async def basic_text_processing():
    """Example of basic text processing."""
    # Initialize pipeline
    pipeline = ProcessingPipeline()
    logger = Logger('basic_example')
    
    # Simple text example
    text = """
    قال الملك شهريار لشهرزاد: حدثيني حديثاً
    فقالت: بلغني أيها الملك السعيد أنه كان في قديم الزمان تاجر
    """
    
    logger.info("Processing simple text example...")
    result = await pipeline.process_text(text)
    
    # Display results
    print("\nProcessing Results:")
    print(f"Frames detected: {len(result.narrative.frames)}")
    print(f"Cultural elements: {len(result.narrative.cultural_elements)}")
    print(f"Processing time: {result.processing_time:.2f} seconds")

async def process_story_file():
    """Example of processing a story file."""
    pipeline = ProcessingPipeline()
    
    # Read story from file
    with open('data/samples/story.txt', 'r', encoding='utf-8') as f:
        story_text = f.read()
    
    # Process story
    result = await pipeline.process_text(story_text)
    
    # Print structure
    print("\nStory Structure:")
    for frame in result.narrative.frames:
        print(f"Level {frame.level}: {frame.type}")
        print(f"Characters: {[char.name_ar for char in frame.characters]}")

async def extract_cultural_elements():
    """Example of cultural element extraction."""
    pipeline = ProcessingPipeline()
    
    text = """
    يا أمير المؤمنين، في مجلس السلطان
    بمدينة بغداد في عهد هارون الرشيد
    """
    
    result = await pipeline.process_text(text)
    
    print("\nCultural Elements:")
    for element in result.narrative.cultural_elements:
        print(f"Type: {element.type}")
        print(f"Text: {element.text}")
        print(f"Context: {element.context}")
        print(f"Confidence: {element.confidence:.2f}")
        print()

def main():
    """Run basic usage examples."""
    print("ANAR System - Basic Usage Examples")
    print("==================================")
    
    # Run examples
    asyncio.run(basic_text_processing())
    asyncio.run(process_story_file())
    asyncio.run(extract_cultural_elements())

if __name__ == "__main__":
    main()
