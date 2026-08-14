"""Command-line front door for the harness.

There is one job to launch: the run matrix, which is every combination of
corpus, model size, control, transfer arm, and seed described by a config file.
This module only parses arguments and hands them to `run_matrix`, so the
research logic stays in `experiment` where it can be read in one place.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from .experiment import run_matrix


def parser() -> argparse.ArgumentParser:
    """Build the argument parser.

    `--scope` picks how much of the matrix to run: `full` runs everything,
    `transfer-only` runs just the transfer tournament and reads its IVC
    baselines from a previously executed matrix summary.
    """
    root = argparse.ArgumentParser(prog="ivcslm")
    subcommands = root.add_subparsers(dest="command", required=True)
    run = subcommands.add_parser("run-matrix", help="Run the complete from-scratch model/control/comparator matrix")
    run.add_argument("--config", type=Path, required=True)
    run.add_argument("--scope", choices=("full", "transfer-only"), default="full")
    return root


def main() -> None:
    """Run the requested command and print the run directory it produced."""
    arguments = parser().parse_args()
    if arguments.command == "run-matrix":
        output = run_matrix(arguments.config, arguments.scope)
        print(output)


if __name__ == "__main__":
    main()
