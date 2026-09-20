from code.agents.base import Agent
from code.llm.ollama import LLMResponse, LocalLLM

class AnalystAgent(Agent):
    def __init__(self, llm: LocalLLM) -> None:
        super().__init__(
            name="analyst",
            description="Ananlyzes questions and produces structured reasoning and conclusions."
        )
        self.llm = llm

    def run(self, task: str) -> LLMResponse:
        prompt = f"""
            You are the Analyst Agent in our multi-agent AI system
            Your responsibility is to analyze the user's task carefully and provide
            a clear, evidence-conscious answer.

            Task:
            {task}

            Provide:
            1. A concise analysis
            2. Key findings
            3. Any assumptions or limitations
        """

        return self.llm.generate(prompt)