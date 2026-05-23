#!/usr/bin/env python3
"""
Log Parser – analyses a log file for top ERROR patterns.
Default file: app.log
Usage:
    python log_parser.py                    # uses app.log
    python log_parser.py /path/to/other.log # uses a different file
"""

import re
import sys
from collections import Counter

# Default log file location
DEFAULT_LOG = "app.log"

ERROR_PATTERN = re.compile(r"ERROR\s+(.*)")

def parse_log(filepath):
    try:
        with open(filepath, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: file not found – {filepath}", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Error: permission denied – {filepath}", file=sys.stderr)
        sys.exit(1)

    errors = []
    for line in lines:
        match = ERROR_PATTERN.search(line)
        if match:
            errors.append(match.group(1).strip())

    if not errors:
        print("No ERROR entries found.")
        return

    counter = Counter(errors)
    print("Top 10 Errors:")
        
    for i, (error, count) in enumerate(counter.most_common(10), start=1):
        print(f"{i:2d}.  {error}")

if __name__ == "__main__":
    # Use argument if provided, otherwise default
    filepath = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_LOG
    parse_log(filepath)