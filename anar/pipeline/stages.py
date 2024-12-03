"""
Pipeline stage definitions for the ANAR system.
"""

from typing import Any, Callable, Dict, Optional
from dataclasses import dataclass

@dataclass
class PipelineStage:
    """Pipeline stage configuration."""
    name: str
    processor: Callable
    validator: Callable
    recovery: Optional[Callable] = None
    config: Optional[Dict] = None

class StageExecutor:
    """
    Pipeline stage executor.
    
    Features:
    - Stage execution
    - Error handling
    - Performance monitoring
    - Result validation
    """
    
    def __init__(self, stage: PipelineStage):
        self.stage = stage
        
    async def execute(
        self,
        data: Any,
        context: Optional[Dict] = None
    ) -> Any:
        """
        Execute pipeline stage.
        
        Args:
            data: Input data
            context: Execution context
            
        Returns:
            Stage processing results
        """
        try:
            # Execute processor
            result = await self.stage.processor(data)
            
            # Validate result
            if not self.stage.validator(result):
                if self.stage.recovery:
                    result = await self.stage.recovery(
                        result,
                        context
                    )
                else:
                    raise ValueError(
                        f"Stage {self.stage.name} validation failed"
                    )
                    
            return result
            
        except Exception as e:
            raise PipelineStageError(
                f"Stage {self.stage.name} failed: {str(e)}"
            )

class StageManager:
    """
    Manager for pipeline stages.
    
    Features:
    - Stage registration
    - Dependency management
    - Execution ordering
    """
    
    def __init__(self):
        self.stages: Dict[str, PipelineStage] = {}
        self.dependencies: Dict[str, List[str]] = {}
        
    def register_stage(
        self,
        stage: PipelineStage,
        dependencies: Optional[List[str]] = None
    ):
        """Register pipeline stage."""
        self.stages[stage.name] = stage
        if dependencies:
            self.dependencies[stage.name] = dependencies
            
    def get_execution_order(self) -> List[str]:
        """Get stage execution order."""
        visited = set()
        order = []
        
        def visit(stage_name: str):
            if stage_name in visited:
                return
            visited.add(stage_name)
            
            for dep in self.dependencies.get(stage_name, []):
                if dep not in self.stages:
                    raise ValueError(
                        f"Unknown dependency: {dep}"
                    )
                visit(dep)
                
            order.append(stage_name)
            
        for stage_name in self.stages:
            visit(stage_name)
            
        return order
        
    async def execute_stages(
        self,
        data: Any,
        context: Optional[Dict] = None
    ) -> Any:
        """Execute all stages in order."""
        result = data
        
        for stage_name in self.get_execution_order():
            stage = self.stages[stage_name]
            executor = StageExecutor(stage)
            result = await executor.execute(
                result,
                context
            )
            
        return result

class PipelineStageError(Exception):
    """Pipeline stage execution error."""
    pass
