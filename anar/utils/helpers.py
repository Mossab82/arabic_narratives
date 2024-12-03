"""
Additional utility functions and classes for the ANAR system.
"""

import re
import json
from typing import Any, Dict, List, Optional
from pathlib import Path
import numpy as np

class TextCleaner:
    """Text cleaning and normalization utilities."""
    
    @staticmethod
    def clean_arabic_text(text: str) -> str:
        """Clean and normalize Arabic text."""
        # Remove tatweel
        text = re.sub('[ـ]', '', text)
        
        # Normalize hamza
        text = re.sub('[إأٱآا]', 'ا', text)
        text = re.sub('[ىئ]', 'ي', text)
        text = re.sub('ؤ', 'و', text)
        
        # Remove non-Arabic characters
        text = re.sub('[^؀-ۿ\s]', '', text)
        
        return text.strip()

class ConfigManager:
    """Configuration management utilities."""
    
    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        
    def _load_config(self) -> Dict:
        """Load configuration from file."""
        if not self.config_path.exists():
            raise FileNotFoundError(
                f"Config file not found: {self.config_path}"
            )
            
        with open(self.config_path, 'r') as f:
            return json.load(f)
            
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return self.config.get(key, default)
        
    def update(self, key: str, value: Any):
        """Update configuration."""
        self.config[key] = value
        self._save_config()
        
    def _save_config(self):
        """Save configuration to file."""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)

class MetricsCalculator:
    """Performance metrics calculation utilities."""
    
    @staticmethod
    def calculate_accuracy(
        predictions: np.ndarray,
        ground_truth: np.ndarray
    ) -> float:
        """Calculate accuracy metric."""
        return np.mean(predictions == ground_truth)
        
    @staticmethod
    def calculate_f1_score(
        precision: float,
        recall: float
    ) -> float:
        """Calculate F1 score."""
        if precision + recall == 0:
            return 0.0
        return 2 * (precision * recall) / (precision + recall)

class DatasetHandler:
    """Dataset management utilities."""
    
    def __init__(self, data_dir: str):
        self.data_dir = Path(data_dir)
        
    def load_dataset(
        self,
        split: str = 'train'
    ) -> Dict:
        """Load dataset split."""
        file_path = self.data_dir / f'{split}.json'
        
        if not file_path.exists():
            raise FileNotFoundError(
                f"Dataset file not found: {file_path}"
            )
            
        with open(file_path, 'r') as f:
            return json.load(f)
            
    def save_results(
        self,
        results: Dict,
        filename: str
    ):
        """Save processing results."""
        output_path = self.data_dir / filename
        
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)

class Logger:
    """Enhanced logging utilities."""
    
    def __init__(
        self,
        name: str,
        log_file: Optional[str] = None
    ):
        self.logger = logging.getLogger(name)
        
        if log_file:
            handler = logging.FileHandler(log_file)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            
    def log_processing_step(
        self,
        step: str,
        details: Dict
    ):
        """Log processing step details."""
        self.logger.info(
            f"Processing step: {step}",
            extra={'details': details}
        )
        
    def log_performance_metrics(
        self,
        metrics: Dict
    ):
        """Log performance metrics."""
        self.logger.info(
            "Performance metrics",
            extra={'metrics': metrics}
        )
