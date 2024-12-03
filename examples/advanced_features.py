"""
Advanced features examples for the ANAR system.
Demonstrates complex functionality and advanced usage patterns.
"""

import asyncio
from pathlib import Path
from anar.pipeline import ProcessingPipeline, PipelineStage
from anar.utils import Optimizer, Validator
from anar.models import NarrativeStructure

async def batch_processing_example():
    """Example of batch processing with checkpoints."""
    # Initialize pipeline with configuration
    config = {
        'batch_size': 5,
        'checkpoint_dir': 'data/checkpoints',
        'parallel': True
    }
    pipeline = ProcessingPipeline(config=config)
    
    # Load multiple stories
    stories = []
    story_dir = Path('data/samples/stories')
    for story_file in story_dir.glob('*.txt'):
        with open(story_file, 'r', encoding='utf-8') as f:
            stories.append(f.read())
    
    # Process batch with progress tracking
    results = await pipeline.process_batch(
        stories,
        show_progress=True
    )
    
    print("\nBatch Processing Results:")
    print(f"Total stories processed: {len(results)}")
    print(f"Average processing time: {sum(r.processing_time for r in results)/len(results):.2f}s")

async def custom_pipeline_example():
    """Example of custom pipeline configuration."""
    # Define custom pipeline stages
    stages = [
        PipelineStage(
            name="preprocessing",
            processor=lambda x: x.lower(),
            validator=lambda x: len(x) > 0
        ),
        PipelineStage(
            name="analysis",
            processor=lambda x: x.split(),
            validator=lambda x: isinstance(x, list)
        )
    ]
    
    # Create pipeline with custom stages
    pipeline = ProcessingPipeline()
    for stage in stages:
        pipeline.add_stage(stage)
    
    # Process with custom pipeline
    text = "قصة الصياد والجني"
    result = await pipeline.process_text(text)
    
    print("\nCustom Pipeline Results:")
    print(f"Stages executed: {list(result.metrics.keys())}")

async def network_analysis_example():
    """Example of narrative network analysis."""
    pipeline = ProcessingPipeline()
    
    text = """
    فقال الملك شهريار: حدثني الوزير قائلاً
    سمعت من التاجر في سوق بغداد
    عن قصة الصياد والجني
    """
    
    result = await pipeline.process_text(text)
    network = result.narrative.get_character_network()
    
    print("\nNetwork Analysis:")
    print("Character Relationships:")
    for node, edges in network.items():
        print(f"{node}:")
        for edge in edges:
            print(f"  -> {edge['target']} ({edge['type']})")

async def cultural_context_analysis():
    """Example of detailed cultural context analysis."""
    pipeline = ProcessingPipeline()
    
    text = """
    في عهد الخليفة هارون الرشيد
    في قصره ببغداد، اجتمع مجلس الوزراء
    وقال الوزير: يا أمير المؤمنين
    """
    
    result = await pipeline.process_text(text)
    
    print("\nCultural Context Analysis:")
    print("Historical Context:")
    for element in result.narrative.cultural_elements:
        if element.type == "historical":
            print(f"Period: {element.context}")
            print(f"Location: {element.attributes.get('location')}")
            print(f"Significance: {element.significance}")

async def performance_optimization_example():
    """Example of performance optimization."""
    # Create optimizer
    optimizer = Optimizer(
        cache_size=1000,
        memory_threshold=0.85
    )
    
    # Initialize pipeline with optimization
    pipeline = ProcessingPipeline()
    
    @optimizer.optimize_processing
    async def process_with_optimization(text):
        return await pipeline.process_text(text)
    
    # Process with optimization
    text = "قصة طويلة عن الصياد والجني"
    result = await process_with_optimization(text)
    
    print("\nOptimization Results:")
    print(f"Processing time: {result.processing_time:.2f}s")
    print(f"Memory usage: {result.metrics['memory_usage']}MB")

def main():
    """Run advanced features examples."""
    print("ANAR System - Advanced Features Examples")
    print("=======================================")
    
    # Run examples
    asyncio.run(batch_processing_example())
    asyncio.run(custom_pipeline_example())
    asyncio.run(network_analysis_example())
    asyncio.run(cultural_context_analysis())
    asyncio.run(performance_optimization_example())

if __name__ == "__main__":
    main()
