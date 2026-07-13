from __future__ import annotations

import argparse
from pathlib import Path

from .experiment import run_matrix


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="ivcslm")
    subcommands = root.add_subparsers(dest="command", required=True)
    run = subcommands.add_parser("run-matrix", help="Run the complete from-scratch model/control/comparator matrix")
    run.add_argument("--config", type=Path, required=True)
    run.add_argument("--scope", choices=("full", "transfer-only"), default="full")
    return root


def main() -> None:
    arguments = parser().parse_args()
    if arguments.command == "run-matrix":
        output = run_matrix(arguments.config, arguments.scope)
        print(output)


if __name__ == "__main__":
    main()
