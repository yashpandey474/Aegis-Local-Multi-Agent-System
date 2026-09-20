from code.llm import LocalLLM
from code.agents.analyst import AnalystAgent
import logging


def main() -> None:
    llm = LocalLLM()
    analyst = AnalystAgent(llm)
    response = analyst.run(
        "What are the main advantages and limitations of retrieval-augmented generation?"
    )
    print(f"Agent: {analyst.name}")
    print(f"Model: {response.model}")
    print(f"\n{response.content}")

if __name__ == "__main__":
    main()
