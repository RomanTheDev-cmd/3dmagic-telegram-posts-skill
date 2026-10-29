#!/usr/bin/env python3
"""Validate an exact plain-text 3D Magic caption; no network or writes."""

import argparse
import json
from pathlib import Path
import sys

MAX_LENGTH = 1024


def caption_limit(value):
    try:
        result = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("limit must be an integer") from exc
    if not 1 <= result <= MAX_LENGTH:
        raise argparse.ArgumentTypeError("limit must be between 1 and 1024")
    return result


def measure(text, limit=MAX_LENGTH):
    characters = len(text)
    utf16_units = len(text.encode("utf-16-le")) // 2
    return {
        "characters": characters,
        "utf16_units": utf16_units,
        "limit": limit,
        "fits": 0 < characters <= limit and utf16_units <= limit,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("text_file", help="UTF-8 file with exact post, or - for stdin")
    parser.add_argument("--limit", type=caption_limit, default=MAX_LENGTH)
    args = parser.parse_args()
    try:
        data = sys.stdin.buffer.read() if args.text_file == "-" else Path(args.text_file).read_bytes()
        text = data.decode("utf-8")
        result = measure(text, args.limit)
    except (OSError, UnicodeError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["fits"] else 1


if __name__ == "__main__":
    sys.exit(main())
