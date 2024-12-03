"""
ANAR: Arabic Narrative Analysis and Recognition System
A comprehensive framework for analyzing and extracting narrative structures 
from the 1001 Arabian Nights.

Version: 1.0.0
Authors: Mossab Ibrahim, Pablo Gervás, Gonzalo Méndez
License: MIT
"""

from .processor import ArabicProcessor, FrameDetector, CulturalAnalyzer
from .models import NarrativeStructure, NetworkBuilder
from .pipeline import ProcessingPipeline, PipelineStage
from .utils import Validator, Optimizer, ErrorHandler

__version__ = '1.0.0'
__author__ = 'Mossab Ibrahim, Pablo Gervás, Gonzalo Méndez'
__email__ = 'mibrahim@ucm.es'

__all__ = [
    'ArabicProcessor',
    'FrameDetector',
    'CulturalAnalyzer',
    'NarrativeStructure',
    'NetworkBuilder',
    'ProcessingPipeline',
    'PipelineStage',
    'Validator',
    'Optimizer',
    'ErrorHandler'
]
