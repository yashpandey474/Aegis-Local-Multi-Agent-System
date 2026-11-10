import pytest
from main.tools.parser import ToolCallParser


def test_parse_valid_tool_call():
    test_tool_name = "tool_name"
    test_argument_exp = "arguments_expression"
    content = """
    {
        "tool": "tool_name",
        "arguments": {
            "expression": "arguments_expression"
        }
    }
    """

    call = ToolCallParser.parse(content)

    assert call.tool_name == test_tool_name
    assert call.arguments == {"expression": test_argument_exp}

def test_reject_invalid_json():
    with pytest.raises(ValueError, match="invalid JSON"):
        ToolCallParser.parse("not valid json")

