#!/usr/bin/env python3
"""
Log Parser – analyses log files for top error patterns.
Usage: python log_parser.py /var/log/app.log
"""

import re
import sys
from collections import Counter

ERROR_PATTERN = re.compile(r"ERROR\s+(.*)")

def parse_log(filepath):
    try:
        with open(filepath, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: file not found – {filepath}", file=sys.stderr)
        sys.exit(1)

    errors = []
    for line in lines:
        match = ERROR_PATTERN.search(line)
        if match:
            errors.append(match.group(1).strip())

    counter = Counter(errors)
    print("Top 10 Errors:")
    for error, count in counter.most_common(10):
        print(f"  {count:4d}  {error}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python log_parser.py <logfile>", file=sys.stderr)
        sys.exit(1)
    parse_log(sys.argv[1])