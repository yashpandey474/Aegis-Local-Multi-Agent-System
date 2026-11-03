"""
AgentRegistry
Acts similar to the ToolRegistry
The caller shouldnt have to call or know how to call each specific agent
It should simply request an agent by name or ID
"""

from main.agents.base import Agent

class AgentRegistry:
    def __init__(self) -> None:
        self.agents: dict[str, Agent] = {}

    def register(self, agent: Agent) -> bool:
        if not agent.name:
            print(f"Agent to be registered has no name: {agent}")
            return False

        if agent.name in self.agents:
            print(f"Agent by name: {agent.name} is already registered: {self.agents[agent.name]}")
            return False

        self.agents[agent.name] = agent

    def get(self, name: str) -> Agent:
        if name not in self.agents:
            raise ValueError(f"Agent by the name: {name} is not registered")

        return self.agents[name]

    def list_agents(self) -> list[Agent]:
        return list(self.agents.values)

    def describe_agents(self) -> str: # used for context-injection to the orchestrator to decide which agent to choose
        if not self.agents:
            print("There are no agents registered, returning an empty description")
            return ""
        
        descriptions = [f"{agent_name}:{agent.description}" for agent_name, agent in self.agents.items()]
        return "\n".join(descriptions)