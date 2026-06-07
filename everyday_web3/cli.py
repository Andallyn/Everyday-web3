"""Command line interface for the Everyday Web3 content engine."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from . import __version__
from .engine import EverydayWeb3Engine, load_config, load_sources, write_generation_outputs
from .models import GenerationContext
from .plugins import recommended_plugins


DEFAULT_CONFIG = Path("config/everyday_web3.json")
DEFAULT_INPUT = Path("data/sources.sample.csv")
DEFAULT_OUTPUT = Path("output")


def parse_platforms(value: str) -> list[str]:
    platforms = [platform.strip().lower() for platform in value.split(",") if platform.strip()]
    if not platforms:
        raise argparse.ArgumentTypeError("at least one platform is required")
    return platforms


def parse_date(value: str | None) -> date:
    if not value:
        return date.today()
    return date.fromisoformat(value)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="everyday-web3",
        description="Generate Everyday Web3 content from curated sources.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    subparsers = parser.add_subparsers(dest="command", required=True)

    generate = subparsers.add_parser("generate", help="Generate drafts and a content calendar.")
    generate.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="Path to JSON config.")
    generate.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="CSV or JSON source input.")
    generate.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Output directory.")
    generate.add_argument(
        "--platforms",
        type=parse_platforms,
        default=parse_platforms("x,linkedin,pinterest,telegram,blog"),
        help="Comma-separated platform keys, e.g. x,linkedin,pinterest,telegram,blog.",
    )
    generate.add_argument("--date", dest="run_date", help="Run date in YYYY-MM-DD format.")
    generate.add_argument("--limit", type=int, default=8, help="Maximum source items to convert.")
    generate.add_argument("--no-weekly", action="store_true", help="Skip weekly roundup output.")

    subparsers.add_parser("plugins", help="Show useful source, workflow, and publishing plugins.")

    return parser


def handle_generate(args: argparse.Namespace) -> int:
    config = load_config(args.config)
    sources = load_sources(args.input)
    engine = EverydayWeb3Engine(config)
    run_date = parse_date(args.run_date)
    brand = config.get("brand", {})
    context = GenerationContext(
        run_date=run_date,
        brand_name=brand.get("name", "Everyday Web3"),
        voice=brand.get("voice", "clear, practical, curious, and useful"),
        platforms=args.platforms,
    )

    ideas = engine.generate(sources=sources, context=context, limit=max(1, args.limit))
    written = write_generation_outputs(
        engine=engine,
        sources=sources,
        ideas=ideas,
        output_dir=args.output,
        run_date=run_date,
        include_weekly=not args.no_weekly,
    )

    print(f"Generated {len(ideas)} content drafts from {len(sources)} sources.")
    for path in written:
        print(f"- {path}")
    return 0


def handle_plugins() -> int:
    print("# Recommended Everyday Web3 plugins and integrations")
    print("")
    for plugin in recommended_plugins():
        print(f"## {plugin['name']}")
        print(plugin["use"])
        print(f"Setup: {plugin['setup']}")
        print("")
    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "generate":
        return handle_generate(args)
    if args.command == "plugins":
        return handle_plugins()

    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
