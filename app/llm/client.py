from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

_CONFIG_DIR = Path.home() / ".config" / "examforge"
_CONFIG_FILE = _CONFIG_DIR / "llm.json"

@dataclass(frozen=True)
class LLMConfig:
    provider: str
    endpoint: str
    model: str
    api_key_env: str | None = None

    @property
    def api_key(self) -> str | None:
        return os.getenv(self.api_key_env) if self.api_key_env else None

def save_config(config: LLMConfig) -> Path:
    _CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    _CONFIG_FILE.write_text(
        json.dumps(
            {
                "provider": config.provider,
                "endpoint": config.endpoint,
                "model": config.model,
                "api_key_env": config.api_key_env,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return _CONFIG_FILE

def load_config() -> LLMConfig | None:
    if not _CONFIG_FILE.exists():
        return None
    data = json.loads(_CONFIG_FILE.read_text(encoding="utf-8"))
    return LLMConfig(
        provider=data["provider"],
        endpoint=data["endpoint"],
        model=data["model"],
        api_key_env=data.get("api_key_env"),
    )

class LLMClient:
    """Small dependency-free client for Ollama and OpenAI-compatible APIs."""

    def __init__(self, config: LLMConfig):
        self.config = config

    def _post(self, url: str, payload: dict[str, object], headers: dict[str, str] | None = None) -> dict[str, object]:
        body = json.dumps(payload).encode("utf-8")
        request = Request(url, data=body, method="POST")
        request.add_header("Content-Type", "application/json")
        for key, value in (headers or {}).items():
            request.add_header(key, value)
        try:
            with urlopen(request, timeout=120) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"LLM request failed ({exc.code}): {detail}") from exc
        except URLError as exc:
            raise RuntimeError(f"Could not reach LLM at {url}: {exc.reason}") from exc

    def chat(self, prompt: str, system: str | None = None) -> str:
        messages: list[dict[str, str]] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        if self.config.provider == "ollama":
            payload = {"model": self.config.model, "messages": messages, "stream": False}
            result = self._post(self.config.endpoint.rstrip("/") + "/api/chat", payload)
            return str(result["message"]["content"])

        headers = {}
        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"
        payload = {"model": self.config.model, "messages": messages, "stream": False}
        result = self._post(self.config.endpoint.rstrip("/") + "/chat/completions", payload, headers)
        return str(result["choices"][0]["message"]["content"])

def config_path() -> Path:
    return _CONFIG_FILE
