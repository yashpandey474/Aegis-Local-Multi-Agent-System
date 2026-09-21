from abc import ABC, abstractmethod
from typing import Any

class Tool(ABC):
    def __init__(
        self,
        name: str,
        description: str,
    ) -> None:
        self.name = name
        self.description = description

    @abstractmethod
    def execute(self, **kwargs: Any) -> Any:
        """Execute the tool"""
        raise NotImplementedError