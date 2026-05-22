#!/usr/bin/env python3
"""
Endpoint Health Checker – monitors a predefined list of URLs.
Just run: python health_check.py
Edit the ENDPOINTS list below to change the targets.
"""

import logging
import sys
import time
import requests

# ====== CONFIGURE YOUR ENDPOINTS HERE ======
ENDPOINTS = [
    "https://www.google.com",
    "https://api.github.com",
    "https://jsonplaceholder.typicode.com/todos/1",
    # Add more URLs as needed
]
# ==========================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def check_endpoint(url, timeout=5):
    """Ping a single URL and log the result."""
    try:
        start = time.time()
        resp = requests.get(url, timeout=timeout)
        elapsed = (time.time() - start) * 1000  # milliseconds
        status = "UP" if resp.status_code == 200 else f"DOWN ({resp.status_code})"
        logger.info(f"{url}: {status} | {elapsed:.0f}ms")
        return resp.status_code == 200
    except requests.RequestException as e:
        logger.error(f"{url}: DOWN - {str(e)}")
        return False

def main():
    if not ENDPOINTS:
        logger.warning("No endpoints configured. Exiting.")
        sys.exit(0)

    all_healthy = True
    for url in ENDPOINTS:
        if not check_endpoint(url):
            all_healthy = False

    sys.exit(0 if all_healthy else 1)

if __name__ == "__main__":
    main()