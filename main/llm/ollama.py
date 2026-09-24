from dataclasses import dataclass
from ollama import Client

DEFAULT_OLLAMA_MODEL = "qwen3:0.6b"
@dataclass(frozen=True)
class OllamaConfig:
    model: str = DEFAULT_OLLAMA_MODEL
    host: str = "http://localhost:11434"

@dataclass(frozen=True)
class LLMResponse:
    content: str
    model: str

class LocalLLM:
    def __init__(self, config: OllamaConfig | None = None) -> None:
        self.config = config or OllamaConfig()
        self.client = Client(host=self.config.host)

    def generate(self, prompt: str) -> str:
        response = self.client.chat(
            model = self.config.model,
            messages = [
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        )
        return LLMResponse(
            content=response.message.content,
            model=self.config.model
        )
