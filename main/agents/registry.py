"""
AgentRegistry
Acts similar to the ToolRegistry
The caller shouldnt have to call or know how to call each specific agent
It should simply request an agent by name or ID
"""

from main.agents.base import Agent

"""
The orchestrator LLM can choose among capabilities that the application has explicitly registered.
It cannot create new executable capabilities simply by generating a string.
"""
class AgentRegistry:
    def __init__(self) -> None:
        self._agents: dict[str, Agent] = {}

    def register(self, agent: Agent) -> bool:
        if not agent.name:
            print(f"Agent to be registered has no name: {agent}")
            return False

        if agent.name in self._agents:
            print(f"Agent by name: {agent.name} is already registered: {self._agents[agent.name]}")
            raise ValueError(f"Agent is already registered by this name")

        self._agents[agent.name] = agent
        return True

    def get(self, name: str) -> Agent:
        if name not in self._agents:
            raise ValueError(f"Agent by the name: {name} is not registered")

        return self._agents[name]

    def list_agents(self) -> list[Agent]:
        return list(self._agents.values())

    def describe_agents(self) -> str: # used for context-injection to the planner to decide which agent to choose
        if not self._agents:
            print("There are no agents registered, returning an empty description")
            return ""
        
        descriptions = [f" - {agent_name}: {agent.description}" for agent_name, agent in self._agents.items()]
        return "\n".join(descriptions)