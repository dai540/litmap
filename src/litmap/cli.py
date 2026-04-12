"""Minimal CLI for litmap."""

from __future__ import annotations

import sys

from .core import package_overview, recommended_run_layout
from .version import __version__


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    command = args[0] if args else "about"

    if command == "version":
        print(__version__)
        return 0

    if command == "about":
        info = package_overview()
        for key, value in info.items():
            print(f"{key}: {value}")
        return 0

    if command == "layout":
        for line in recommended_run_layout():
            print(line)
        return 0

    print("usage: litmap [about|layout|version]", file=sys.stderr)
    return 1
