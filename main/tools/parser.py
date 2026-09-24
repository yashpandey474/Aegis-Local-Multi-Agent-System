import json
from typing import Any
from main.tools.protocol import ToolCall
import logging

logger = logging.getLogger(__name__)

class ToolCallParser:

    @staticmethod
    def parse(content: str) -> ToolCall:
        """
        Convert untrusted LLM output into our internal ToolCall representation.
        """
        try:
            # The output should be a json
            data: dict[str, any] = json.loads(content)
            logger.debug("Successfully parsed LLM response as json")
        except json.JSONDecodeError as e:
            raise ValueError("LLM Returned invalid JSON.")

        if not isinstance(data, dict):
            raise ValueError("Tool call must be a JSON object")

        tool_name = data.get("tool")
        arguments = data.get("arguments")

        if not isinstance(tool_name, str) or not tool_name:
                raise ValueError("Tool call must contain a valid 'tool' field.")

        if not isinstance(arguments, dict):
            raise ValueError("Tool call must contain an 'arguments' object.")

        logger.debug("Successfully constructued tool call object from LLM response")
        return ToolCall(
             tool_name=tool_name,
             arguments=arguments
        )
