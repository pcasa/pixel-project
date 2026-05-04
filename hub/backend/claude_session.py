"""
Per-device Claude conversation session.
Manages message history, calls anthropic.messages.create(), and dispatches tool calls.
"""

from __future__ import annotations

import asyncio
import json
import logging
from typing import Any, Awaitable, Callable, Optional

import anthropic

logger = logging.getLogger(__name__)

DEFAULT_MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 1024
MAX_HISTORY_TURNS = 20

_sessions: dict[str, "ClaudeSession"] = {}


def get_session(device_id: str) -> "ClaudeSession":
    if device_id not in _sessions:
        _sessions[device_id] = ClaudeSession(device_id=device_id)
    return _sessions[device_id]


def clear_session(device_id: str) -> None:
    _sessions.pop(device_id, None)


def _build_tool_schemas(declarations: list[dict]) -> list[dict]:
    """Convert OmniBot-style OpenAPI function declarations to Anthropic tool format."""
    tools = []
    for decl in declarations:
        tools.append({
            "name": decl["name"],
            "description": decl.get("description", ""),
            "input_schema": decl.get("parameters", {"type": "object", "properties": {}}),
        })
    return tools


class ClaudeSession:
    def __init__(self, *, device_id: str):
        self.device_id = device_id
        self._history: list[dict[str, Any]] = []
        self._lock = asyncio.Lock()

    def clear_history(self) -> None:
        self._history.clear()

    def get_history(self) -> list[dict[str, Any]]:
        return list(self._history)

    def append_history(self, role: str, content: Any) -> None:
        self._history.append({"role": role, "content": content})
        # Trim to keep last MAX_HISTORY_TURNS exchanges (pairs)
        while len(self._history) > MAX_HISTORY_TURNS * 2:
            self._history.pop(0)
            if self._history:
                self._history.pop(0)

    async def send_message(
        self,
        user_text: str,
        *,
        system_prompt: str,
        model: str,
        api_key: str,
        tool_declarations: Optional[list[dict]] = None,
        on_tool_call: Optional[Callable[[str, str, dict], Awaitable[Any]]] = None,
        max_tool_rounds: int = 6,
        on_first_token: Optional[Callable[[], Awaitable[None]]] = None,
    ) -> str:
        """
        Send a user message. Returns the final assistant text.
        Handles multi-round tool use automatically via on_tool_call callback.
        on_tool_call(device_id, tool_name, tool_input) -> result
        """
        async with self._lock:
            client = anthropic.AsyncAnthropic(api_key=api_key)
            tools = _build_tool_schemas(tool_declarations or [])

            # Build messages: history + new user turn
            messages = list(self._history)
            messages.append({"role": "user", "content": user_text})

            full_text = ""
            first_token_fired = False

            for _round in range(max(1, max_tool_rounds)):
                kwargs: dict[str, Any] = {
                    "model": model,
                    "max_tokens": MAX_TOKENS,
                    "system": system_prompt,
                    "messages": messages,
                }
                if tools:
                    kwargs["tools"] = tools

                try:
                    response = await client.messages.create(**kwargs)
                except anthropic.APIError as e:
                    logger.error("[claude] API error device=%s: %s", self.device_id, e)
                    raise

                # Fire first-token callback once (for ESP32 "thinking" animation)
                if not first_token_fired:
                    first_token_fired = True
                    if on_first_token:
                        try:
                            await on_first_token()
                        except Exception:
                            pass

                text_blocks = [b for b in response.content if b.type == "text"]
                tool_use_blocks = [b for b in response.content if b.type == "tool_use"]

                if text_blocks:
                    full_text = " ".join(b.text for b in text_blocks).strip()

                if response.stop_reason != "tool_use" or not tool_use_blocks:
                    break

                # Execute tool calls and continue
                messages.append({"role": "assistant", "content": response.content})
                tool_results = []
                for tu in tool_use_blocks:
                    result: Any = {"result": "ok"}
                    if on_tool_call:
                        try:
                            result = await on_tool_call(self.device_id, tu.name, tu.input)
                        except Exception as e:
                            result = {"error": str(e)}
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": tu.id,
                        "content": json.dumps(result) if not isinstance(result, str) else result,
                    })
                messages.append({"role": "user", "content": tool_results})

            # Persist the exchange to history
            self.append_history("user", user_text)
            self.append_history("assistant", full_text)

            return full_text
