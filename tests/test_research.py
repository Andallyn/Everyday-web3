from __future__ import annotations

import tempfile
import unittest
from datetime import date
from pathlib import Path

from everyday_web3.engine import EverydayWeb3Engine, load_config, load_sources
from everyday_web3.research import (
    ResearchEngine,
    load_company_watchlist,
    load_source_registry,
    write_research_outputs,
)


CONFIG_PATH = Path("config/everyday_web3.json")
SOURCE_REGISTRY = Path("config/source_registry.json")
COMPANY_WATCHLIST = Path("data/company_watchlist.sample.csv")
SAMPLE_INPUT = Path("data/sources.sample.csv")


class ResearchEngineTest(unittest.TestCase):
    def setUp(self) -> None:
        content_engine = EverydayWeb3Engine(load_config(CONFIG_PATH))
        self.research_engine = ResearchEngine(content_engine)

    def test_loads_source_registry_with_x_list(self) -> None:
        registry = load_source_registry(SOURCE_REGISTRY)

        self.assertGreaterEqual(len(registry), 5)
        self.assertEqual(registry[0].source_type, "x_list")
        self.assertIn("1970082106794442856", registry[0].url)

    def test_loads_company_watchlist(self) -> None:
        companies = load_company_watchlist(COMPANY_WATCHLIST)

        self.assertGreaterEqual(len(companies), 5)
        self.assertEqual(companies[0].priority, 5)

    def test_scores_wellness_and_event_leads_highly(self) -> None:
        sources = load_sources(SAMPLE_INPUT)
        leads = self.research_engine.score_leads(sources, limit=3)

        self.assertEqual(len(leads), 3)
        self.assertGreaterEqual(leads[0].score, leads[1].score)
        self.assertTrue(any("community/wellness" in reason for reason in leads[0].reasons))

    def test_writes_research_outputs(self) -> None:
        sources = load_sources(SAMPLE_INPUT)
        registry = load_source_registry(SOURCE_REGISTRY)
        companies = load_company_watchlist(COMPANY_WATCHLIST)

        with tempfile.TemporaryDirectory() as tmp_dir:
            written = write_research_outputs(
                research_engine=self.research_engine,
                sources=sources,
                registry=registry,
                companies=companies,
                output_dir=Path(tmp_dir),
                run_date=date(2026, 6, 7),
            )

        self.assertEqual(
            {path.name for path in written},
            {"daily_research_brief.md", "source_map.md", "company_watchlist.md", "scored_leads.csv"},
        )


if __name__ == "__main__":
    unittest.main()
