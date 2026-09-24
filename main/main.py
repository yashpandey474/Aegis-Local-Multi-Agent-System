from main.llm import LocalLLM
from main.agents.analyst import AnalystAgent
import logging
from main.tools import CalculatorTool, ToolRegistry
from main.tools.string_length import StringLengthTool

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)

def main() -> None:
    llm = LocalLLM()

    tools = ToolRegistry()

    # register all tools
    tools.register(CalculatorTool())
    tools.register(StringLengthTool())

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

    response = analyst.run(
        "How many characters are in mississippi?"
    )

    logger.info(f"Agent: {analyst.name}")
    logger.info(f"Model: {response.model}")
    logger.info(f"\n{response.content}")

if __name__ == "__main__":
    main()
