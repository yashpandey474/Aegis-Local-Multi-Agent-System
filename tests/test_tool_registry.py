
from main.tools.calculator import CalculatorTool
from main.tools.protocol import ToolCall
from main.tools.registry import ToolRegistry

def test_tool_registry_execute():
    tools = ToolRegistry()
    tools.register(CalculatorTool())
    tool_name = "calculator"

    call = ToolCall(
        tool_name=tool_name,
        arguments={
            "expression": "(18/10)^(1/5)-1"
        }
    )

    result = tools.execute(call)

    assert result.success == True
    assert result.error is None
    assert result.tool_name == tool_name