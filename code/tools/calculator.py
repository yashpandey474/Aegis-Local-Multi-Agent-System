from typing import Any
from code.tools.base import Tool
import ast
import operator

class CalculatorTool(Tool):
    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos
    }

    def __init__(self) -> None:
        super().__init__(
            name="calculator",
            description="Performs arithmetic calculations"
        )

    def execute(self, expression: str) -> float:
        expression = self._normalize_expression(expression)
        try:
            tree = ast.parse(expression, mode="eval")
            result = self._evaluate(tree.body)
            return float(result)
        except Exception as exc:
            raise ValueError(
                f"Invalid mathematical expression: {expression}"
            ) from exc

    @staticmethod
    def _normalize_expression(expression: str) -> str:
        return expression.replace("^", "**")

    def _evaluate(self, node: ast.AST) -> Any:
        # only allow specific ast node types
        # acts as a form of input validatio

        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value

            raise ValueError("Only numeric constants are allowed.")

        if isinstance(node, ast.BinOp):
            operator_fn = self.OPERATORS.get(type(node.op))

            if operator_fn is None:
                raise ValueError(f"Unsupported operator: {type(node.jp).__name__}")

            left = self._evaluate(node.left)
            right = self._evaluate(node.right)

            return operator_fn(left, right)

        if isinstance(node, ast.UnaryOp):
            operator_fn = self.OPERATORS.get(type(node.op))

            if operator_fn is None:
                raise ValueError(
                    f"Unsupported unary operator: {type(node.op).__name__}"
                )

            operand = self._evaluate(node.operand)
            return operator_fn(operand)

        raise ValueError(
            f"Unsupported expression eleemnt: {type(node).__name__}"
        )