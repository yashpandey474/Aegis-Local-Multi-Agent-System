from typing import Any
from code.tools.base import Tool

class CalculatorTool(Tool):
    def __init__(self) -> None:
        super().__init__(
            name="calculator",
            description="Performs arithmetic calculations"
        )

    def execute(self, expression: str) -> float:
        try:
            #TODO: Replace with math parser
            return float(eval(expression, {"__builtins__": {}}, {}))
        except Exception as exc:
            raise ValueError(
                f"Invalid mathematical expression: {expression}"
            ) from exc