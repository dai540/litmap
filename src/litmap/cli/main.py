from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from litmap import __version__
from litmap.config.loader import load_config
from litmap.pipeline.runner import describe_pipeline
from litmap.storage.layout import render_layout_tree


DEFAULT_CONFIG_TEMPLATE = """project:
  name: "demo-run"
  run_dir: "./runs"

source:
  type: "csv"
  params:
    path: "./data/papers.csv"

corpus:
  text_fields: ["title", "abstract"]
  text_separator: " [SEP] "

embedding:
  provider: "specter2"

analysis:
  pca_cluster:
    n_components: 50
  pca_plot:
    n_components: 2

visualization:
  backend: "plotly"
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="litmap", description="Literature mapping toolkit scaffold.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("version", help="Print package version.")
    subparsers.add_parser("describe-layout", help="Print the recommended run directory layout.")

    init_config = subparsers.add_parser("init-config", help="Write a starter YAML config.")
    init_config.add_argument("--output", required=True, help="Path to write the config file.")

    show_plan = subparsers.add_parser("show-plan", help="Print the pipeline blueprint for a config.")
    show_plan.add_argument("--config", required=True, help="Path to YAML or JSON config.")
    show_plan.add_argument("--json", action="store_true", help="Emit JSON instead of plain text.")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "version":
        print(__version__)
        return 0

    if args.command == "describe-layout":
        print(render_layout_tree())
        return 0

    if args.command == "init-config":
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(DEFAULT_CONFIG_TEMPLATE, encoding="utf-8")
        print(f"Wrote starter config to {output}")
        return 0

    if args.command == "show-plan":
        config = load_config(args.config)
        steps = describe_pipeline(config)
        if args.json:
            print(json.dumps([asdict(step) for step in steps], indent=2))
        else:
            for index, step in enumerate(steps, start=1):
                outputs = ", ".join(step.outputs) if step.outputs else "-"
                print(f"{index}. {step.name}")
                print(f"   purpose: {step.purpose}")
                print(f"   outputs: {outputs}")
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
