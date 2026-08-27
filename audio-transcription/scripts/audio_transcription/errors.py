from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class CliError(RuntimeError):
    code: str
    message: str
    next_actions: list[dict[str, Any]] = field(default_factory=list)
    requires_user_decision: bool = False

    def __str__(self) -> str:
        return self.message

    def envelope(self) -> dict[str, Any]:
        return {
            "status": "error",
            "error_code": self.code,
            "message": self.message,
            "requires_user_decision": self.requires_user_decision,
            "next_actions": self.next_actions,
        }


def setup_required(
    message: str = "The local transcription runtime is not installed.",
) -> CliError:
    return CliError(
        "SETUP_REQUIRED",
        message,
        [
            {
                "kind": "invoke_skill",
                "instruction": "Invoke $audio-transcription and request setup.",
            }
        ],
    )
