from __future__ import annotations

import unittest
from pathlib import Path

from everyday_web3.mcps import build_cursor_mcp_config, load_mcp_registry, render_mcp_markdown


MCP_REGISTRY = Path("config/mcp_registry.json")


class McpRegistryTest(unittest.TestCase):
    def test_loads_recommended_mcps_in_priority_order(self) -> None:
        mcps = load_mcp_registry(MCP_REGISTRY)

        self.assertGreaterEqual(len(mcps), 8)
        self.assertEqual(mcps[0].key, "firecrawl-mcp")
        self.assertEqual([mcp.priority for mcp in mcps], sorted(mcp.priority for mcp in mcps))

    def test_builds_cursor_config(self) -> None:
        config = build_cursor_mcp_config(load_mcp_registry(MCP_REGISTRY))

        self.assertIn("mcpServers", config)
        self.assertIn("firecrawl-mcp", config["mcpServers"])
        self.assertIn("exa", config["mcpServers"])
        self.assertIn("notion", config["mcpServers"])
        self.assertEqual(config["mcpServers"]["exa"]["url"], "https://mcp.exa.ai/mcp")

    def test_renders_markdown(self) -> None:
        markdown = render_mcp_markdown(load_mcp_registry(MCP_REGISTRY))

        self.assertIn("# Everyday Web3 MCP Stack", markdown)
        self.assertIn("Firecrawl MCP", markdown)
        self.assertIn(".cursor/mcp.example.json", markdown)


if __name__ == "__main__":
    unittest.main()
