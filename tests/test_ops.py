from __future__ import annotations

import tempfile
import unittest
from datetime import date
from pathlib import Path

from everyday_web3.cli import main
from everyday_web3.engine import EverydayWeb3Engine, load_config
from everyday_web3.models import GenerationContext, SourceItem
from everyday_web3.ops import (
    build_scheduler_csv,
    dedupe_sources,
    freshness_label,
    lint_ideas,
)


class OpsWorkflowTest(unittest.TestCase):
    def test_dedupe_keeps_highest_priority_url(self) -> None:
        sources = [
            SourceItem.from_mapping(
                {"title": "Low", "url": "https://example.com/a", "priority": 1}
            ),
            SourceItem.from_mapping(
                {"title": "High", "url": "https://example.com/a", "priority": 5}
            ),
        ]

        deduped = dedupe_sources(sources)

        self.assertEqual(len(deduped), 1)
        self.assertEqual(deduped[0].title, "High")

    def test_freshness_labels_this_week(self) -> None:
        source = SourceItem.from_mapping({"title": "Event", "event_date": "2026-07-18"})

        self.assertEqual(freshness_label(source, date(2026, 7, 15)), "this_week")

    def test_lint_and_scheduler_export(self) -> None:
        engine = EverydayWeb3Engine(load_config(Path("config/everyday_web3.json")))
        source = SourceItem.from_mapping(
            {
                "title": "Community meetup",
                "source_type": "event",
                "summary": "Useful local meetup.",
            }
        )
        ideas = engine.generate(
            [source],
            GenerationContext(
                date(2026, 7, 15), "Everyday Web3", "practical", ["x", "pinterest"]
            ),
            limit=1,
        )

        issues = lint_ideas(ideas)
        scheduler_csv = build_scheduler_csv(ideas, date(2026, 7, 15), "buffer")

        self.assertTrue(any("missing source link" in issue.message for issue in issues))
        self.assertIn("buffer", scheduler_csv)
        self.assertIn("Twitter/X", scheduler_csv)

    def test_daily_command_writes_dashboard(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            args = [
                "everyday-web3",
                "daily",
                "--input",
                "data/sources.sample.csv",
                "--output",
                tmp_dir,
                "--date",
                "2026-06-07",
                "--limit",
                "2",
            ]
            import sys

            original = sys.argv
            try:
                sys.argv = args
                result = main()
            finally:
                sys.argv = original

            self.assertEqual(result, 0)
            self.assertTrue(
                (Path(tmp_dir) / "2026-06-07" / "editorial_dashboard.md").exists()
            )
            self.assertTrue(
                (Path(tmp_dir) / "2026-06-07" / "scheduler_export.csv").exists()
            )


if __name__ == "__main__":
    unittest.main()
