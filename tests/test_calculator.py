from code.tools.calculator import CalculatorTool

test_expression = "(18 / 10) ** (1 / 5) - 1"

def main() -> None:
    calculator = CalculatorTool()

    result = calculator.execute(
        expression=test_expression
    )

    print(f"Result: {result}")


if __name__ == "__main__":
    main()