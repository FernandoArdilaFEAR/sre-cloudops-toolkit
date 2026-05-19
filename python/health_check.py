#!/usr/bin/env python3
"""
Endpoint Health Checker
Pings a list of URLs, reports HTTP status and response time.
Usage: python health_check.py --endpoints https://example.com,https://api.example.com
"""

import argparse
import logging
import sys
import time
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def check_endpoint(url, timeout=5):
    try:
        start = time.time()
        resp = requests.get(url, timeout=timeout)
        elapsed = (time.time() - start) * 1000  # ms
        status = "UP" if resp.status_code == 200 else f"DOWN ({resp.status_code})"
        logger.info(f"{url}: {status} | {elapsed:.0f}ms")
        return resp.status_code == 200
    except requests.RequestException as e:
        logger.error(f"{url}: DOWN - {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description="HTTP endpoint health checker")
    parser.add_argument("--endpoints", required=True, help="Comma‑separated list of URLs")
    args = parser.parse_args()

    urls = [u.strip() for u in args.endpoints.split(",")]
    all_healthy = True
    for url in urls:
        if not check_endpoint(url):
            all_healthy = False

    sys.exit(0 if all_healthy else 1)

if __name__ == "__main__":
    main()