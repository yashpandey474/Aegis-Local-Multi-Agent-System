from main.tools.calculator import CalculatorTool

test_expression = "(18 / 10) ** (1 / 5) - 1"

def main() -> None:
    calculator = CalculatorTool()
    expressions = [
        "2 + 3",
        "10 / 4",
        "2^3",
        "(18 / 10)^(1/5) - 1",
        "-5 + 10"
    ]

    for expression in expressions:
        result = calculator.execute(expression)
        print(f"{expression:30} -> {result}")

if __name__ == "__main__":
    main()