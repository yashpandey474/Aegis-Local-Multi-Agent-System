from code.llm import LocalLLM
from code.agents.analyst import AnalystAgent
import logging
from code.tools.calculator import CalculatorTool, ToolRegistry

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)

def main() -> None:
    llm = LocalLLM()
    calculator = CalculatorTool()

    tools = ToolRegistry()
    tools.register(CalculatorTool())

    analyst = AnalystAgent(
        llm=llm,
        tools=tools
    )


    response = analyst.run(
        "Revenue increased from 10 billion to 18 billion "
        "over a period of 5 years. What was the CAGR?"
    )

    logger.info(f"Agent: {analyst.name}")
    logger.info(f"Model: {response.model}")
    logger.info(f"\n{response.content}")

if __name__ == "__main__":
    main()
