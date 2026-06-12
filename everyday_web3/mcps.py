"""MCP recommendations for the Everyday Web3 research engine."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


DEFAULT_MCP_REGISTRY = Path("config/mcp_registry.json")


@dataclass(frozen=True)
class RecommendedMcp:
    """One MCP server recommendation with setup metadata."""

    name: str
    key: str
    priority: int
    status: str
    purpose: str
    best_for: list[str] = field(default_factory=list)
    cursor_config: dict[str, Any] = field(default_factory=dict)
    secrets: list[str] = field(default_factory=list)
    source: str = ""

    @classmethod
    def from_mapping(cls, row: dict[str, Any]) -> "RecommendedMcp":
        return cls(
            name=str(row.get("name") or "").strip(),
            key=str(row.get("key") or "").strip(),
            priority=int(row.get("priority") or 999),
            status=str(row.get("status") or "").strip(),
            purpose=str(row.get("purpose") or "").strip(),
            best_for=[str(item) for item in row.get("best_for", [])],
            cursor_config=dict(row.get("cursor_config", {})),
            secrets=[str(item) for item in row.get("secrets", [])],
            source=str(row.get("source") or "").strip(),
        )


def load_mcp_registry(path: Path = DEFAULT_MCP_REGISTRY) -> list[RecommendedMcp]:
    with path.open(encoding="utf-8") as file:
        payload = json.load(file)

    raw_mcps = payload.get("mcps", payload if isinstance(payload, list) else [])
    if not isinstance(raw_mcps, list):
        raise ValueError("MCP registry must be a list or an object with an mcps list")

    return sorted((RecommendedMcp.from_mapping(row) for row in raw_mcps), key=lambda item: item.priority)


def build_cursor_mcp_config(mcps: list[RecommendedMcp]) -> dict[str, dict[str, Any]]:
    return {"mcpServers": {mcp.key: mcp.cursor_config for mcp in mcps if mcp.cursor_config}}


def render_mcp_markdown(mcps: list[RecommendedMcp]) -> str:
    lines = [
        "# Everyday Web3 MCP Stack",
        "",
        "Use these MCPs to turn the generator into a stronger research desk. Add only the MCPs you are ready to authenticate and actively use.",
        "",
    ]

    for mcp in mcps:
        best_for = ", ".join(mcp.best_for) if mcp.best_for else "general workflow support"
        secrets = ", ".join(mcp.secrets) if mcp.secrets else "none or OAuth flow"
        lines.extend(
            [
                f"## {mcp.priority}. {mcp.name}",
                f"- Key: `{mcp.key}`",
                f"- Status: {mcp.status.replace('_', ' ')}",
                f"- Purpose: {mcp.purpose}",
                f"- Best for: {best_for}",
                f"- Secrets needed: {secrets}",
                f"- Source: {mcp.source}",
                "",
            ]
        )

    lines.extend(
        [
            "## Cursor config template",
            "",
            "Copy `.cursor/mcp.example.json` to `.cursor/mcp.json`, then replace placeholders with your own keys. Do not commit real secrets.",
            "",
        ]
    )
    return "\n".join(lines)
