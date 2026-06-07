from __future__ import annotations

import tempfile
import unittest
from datetime import date
from pathlib import Path

from everyday_web3.engine import (
    EVENING_SHIFT,
    MORNING_SHIFT,
    EverydayWeb3Engine,
    load_config,
    load_sources,
    write_generation_outputs,
)
from everyday_web3.models import GenerationContext, SourceItem


CONFIG_PATH = Path("config/everyday_web3.json")
SAMPLE_INPUT = Path("data/sources.sample.csv")


class EverydayWeb3EngineTest(unittest.TestCase):
    def setUp(self) -> None:
        self.config = load_config(CONFIG_PATH)
        self.engine = EverydayWeb3Engine(self.config)

    def test_loads_sample_sources(self) -> None:
        sources = load_sources(SAMPLE_INPUT)

        self.assertGreaterEqual(len(sources), 5)
        self.assertEqual(sources[0].priority, 5)

    def test_classifies_wellness_source(self) -> None:
        source = SourceItem.from_mapping(
            {
                "title": "Creator burnout recovery circle",
                "summary": "Meditation and yoga for Web3 builders",
                "tags": "burnout,yoga,creator wellness",
            }
        )

        self.assertEqual(self.engine.classify_category(source), "Health and Wellness")
        self.assertEqual(self.engine.detect_shift(source), EVENING_SHIFT)
        self.assertEqual(
            self.engine.pick_format(source, "Health and Wellness", EVENING_SHIFT),
            "Burnout Prevention",
        )

    def test_defaults_to_morning_for_product_news(self) -> None:
        source = SourceItem.from_mapping(
            {
                "title": "Wallet app launches merchant checkout",
                "summary": "A mobile wallet added payments for local stores.",
                "source_type": "post",
                "tags": "mobile,payment,shopping",
            }
        )

        self.assertEqual(self.engine.detect_shift(source), MORNING_SHIFT)
        self.assertIn(self.engine.classify_category(source), {"Shopping", "Mobile"})

    def test_generates_and_writes_outputs(self) -> None:
        sources = load_sources(SAMPLE_INPUT)[:2]
        context = GenerationContext(
            run_date=date(2026, 6, 7),
            brand_name="Everyday Web3",
            voice="practical",
            platforms=["x", "linkedin"],
        )

        ideas = self.engine.generate(sources, context=context, limit=2)

        self.assertEqual(len(ideas), 4)
        with tempfile.TemporaryDirectory() as tmp_dir:
            written = write_generation_outputs(
                engine=self.engine,
                sources=sources,
                ideas=ideas,
                output_dir=Path(tmp_dir),
                run_date=context.run_date,
            )
            written_names = {path.name for path in written}

        self.assertIn("content_calendar.md", written_names)
        self.assertIn("weekly_roundup.md", written_names)


if __name__ == "__main__":
    unittest.main()
