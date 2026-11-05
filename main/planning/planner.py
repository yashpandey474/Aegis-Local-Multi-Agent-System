from main.llm.ollama import LocalLLM
from main.planning.constants import PLANNER_PROMPT
from main.planning.models import Plan, PlanStep
import json

import logging

from main.planning.validator import PlanValidator
logger = logging.getLogger(__name__)

class Planner:
    """Separation from other agents is important when we have multiple agents
    I have a complex task. What work needs to happen to solve it?
    
    Planner has constrained autonomy - it can decide "the task requires calculation" 
    but we don't want it to control everything

    LLM -proposes-> Plan -validation-> Execution
    The LLM has decision authority, but the application retains execution authority.
    """
    def __init__(self, llm: LocalLLM) -> None:
        self.llm = llm

    def create_plan(
            self,
            task: str, 
            available_agents: str # loose coupling, it does not need the entire registry to be passed
        ) -> Plan:
        try:
            prompt = PLANNER_PROMPT.format(
                task=task, 
                available_agents=available_agents
            )
            
            response = self.llm.generate(prompt)
            data = json.loads(response.content)

            plan_steps = tuple(
                PlanStep( 
                    step_id=step["step_id"],
                    description=step["description"],
                    agent_name=step["agent_name"]
                )
                for step in data
            )

            plan = Plan(
                task=task,
                steps=plan_steps,
            )
            
        except Exception as e:
            raise Exception(f"Failed to create plan: {e}")

        PlanValidator.validate(plan)
        return plan


            