from main.tools.base import Tool


class StringLengthTool(Tool):
    def __init__(self) -> None:
        super().__init__(
            name="string_length",
            description="""
            - Returns the number of characters in a string.
            - Arguments: text
            """,
        )

    def execute(self, text: str) -> int:
        return len(text)
        