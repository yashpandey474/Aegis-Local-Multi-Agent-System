from main.llm.ollama import LocalLLM
from main.planning.constants import PLANNER_PROMPT
from main.planning.models import PlanStep
import json

import logging
logger = logging.getLogger(__name__)

class Planner:
    """Separation from other agents is important when we have multiple agents"""
    """I have a complex task. What work needs to happen to solve it?"""
    def __init__(self, llm: LocalLLM) -> None:
        self.llm = llm

    def create_plan(self, task: str) -> list[PlanStep]:
        prompt = PLANNER_PROMPT.format(task=task)
        print(f"Prompt sent to planner: {prompt}")
        response = self.llm.generate(prompt)
        data = json.loads(response.content)

        return [
            PlanStep(
                step_id=step["step_id"],
                description=step["description"]
            )
            for step in data
        ]