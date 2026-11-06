from __future__ import annotations

import argparse

from .core import calculate_life_path, calculate_report


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute numerology values for a person.")
    parser.add_argument("name", nargs="?", default="", help="Full name to analyze")
    parser.add_argument("birth_date", nargs="?", default="", help="Birth date, such as 1990-08-15")
    args = parser.parse_args()

    if not args.name or not args.birth_date:
        parser.error("name and birth_date are required")

    report = calculate_report(args.name, args.birth_date)
    print(report)


if __name__ == "__main__":
    main()
