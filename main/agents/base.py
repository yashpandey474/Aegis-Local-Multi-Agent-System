from abc import ABC, abstractmethod
from main.agents.results import AgentResult
from main.llm.ollama import LLMResponse

class Agent(ABC):
    def __init__(
        self,
        name: str,
        description: str,
    ) -> None:
        self.name = name
        self.description = description

    @abstractmethod
    def run(self, task: str) -> AgentResult: # Not just an LLM response, contains metadata, artifacts
        raise NotImplementedError