"""
Error handling utilities for the ANAR system.
Provides comprehensive error handling and logging.
"""

import logging
import traceback
from typing import Any, Dict, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ErrorResponse:
    """Error response container."""
    error_type: str
    message: str
    timestamp: datetime
    trace: str
    context: Dict
    recovery_action: Optional[str] = None

class ErrorHandler:
    """
    Error handler for ANAR system components.
    
    Features:
    - Error categorization
    - Recovery strategies
    - Detailed logging
    - Error tracking
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.error_counts = {}
        
    def handle_processing_error(
        self,
        error: Exception,
        context: Optional[Dict] = None
    ) -> ErrorResponse:
        """
        Handle text processing errors.
        
        Args:
            error: Encountered error
            context: Error context
            
        Returns:
            Error response
        """
        error_type = type(error).__name__
        self._increment_error_count(error_type)
        
        response = ErrorResponse(
            error_type=error_type,
            message=str(error),
            timestamp=datetime.now(),
            trace=traceback.format_exc(),
            context=context or {},
            recovery_action=self._get_recovery_action(error_type)
        )
        
        self.logger.error(
            f"Processing error: {response.error_type} - {response.message}",
            extra={'context': response.context}
        )
        
        return response
        
    def handle_network_error(
        self,
        error: Exception,
        context: Optional[Dict] = None
    ) -> ErrorResponse:
        """
        Handle network construction errors.
        
        Args:
            error: Encountered error
            context: Error context
            
        Returns:
            Error response
        """
        error_type = type(error).__name__
        self._increment_error_count(error_type)
        
        response = ErrorResponse(
            error_type=error_type,
            message=str(error),
            timestamp=datetime.now(),
            trace=traceback.format_exc(),
            context=context or {},
            recovery_action=self._get_recovery_action(error_type)
        )
        
        self.logger.error(
            f"Network error: {response.error_type} - {response.message}",
            extra={'context': response.context}
        )
        
        return response
        
    def handle_validation_error(
        self,
        error: Exception,
        context: Optional[Dict] = None
    ) -> ErrorResponse:
        """
        Handle validation errors.
        
        Args:
            error: Encountered error
            context: Error context
            
        Returns:
            Error response
        """
        error_type = type(error).__name__
        self._increment_error_count(error_type)
        
        response = ErrorResponse(
            error_type=error_type,
            message=str(error),
            timestamp=datetime.now(),
            trace=traceback.format_exc(),
            context=context or {},
            recovery_action=self._get_recovery_action(error_type)
        )
        
        self.logger.error(
            f"Validation error: {response.error_type} - {response.message}",
            extra={'context': response.context}
        )
        
        return response
        
    def _increment_error_count(self, error_type: str):
        """Track error occurrences."""
        if error_type not in self.error_counts:
            self.error_counts[error_type] = 0
        self.error_counts[error_type] += 1
        
    def _get_recovery_action(
        self,
        error_type: str
    ) -> Optional[str]:
        """Get appropriate recovery action for error type."""
        recovery_actions = {
            'ValueError': 'Validate input parameters',
            'KeyError': 'Check required dictionary keys',
            'IndexError': 'Verify array indices',
            'TypeError': 'Check type compatibility',
            'AttributeError': 'Verify object attributes'
        }
        return recovery_actions.get(error_type)
        
    def get_error_statistics(self) -> Dict:
        """Get error occurrence statistics."""
        return {
            'total_errors': sum(self.error_counts.values()),
            'error_types': self.error_counts,
            'most_common': max(
                self.error_counts.items(),
                key=lambda x: x[1]
            ) if self.error_counts else None
        }
