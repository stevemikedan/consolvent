"""Command-line entry point for the falsification harness."""

from __future__ import annotations

import argparse
import json

from harness.run import default_specs, run_default_suite, run_spec


def main() -> None:
    parser = argparse.ArgumentParser(description="Run pre-registered falsification tests.")
    parser.add_argument(
        "--test",
        choices=["all"] + [spec.test_id for spec in default_specs()],
        default="all",
        help="Discriminator test to run.",
    )
    args = parser.parse_args()

    if args.test == "all":
        records = run_default_suite()
    else:
        spec = next(spec for spec in default_specs() if spec.test_id == args.test)
        records = [run_spec(spec)]

    print(json.dumps(records, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

