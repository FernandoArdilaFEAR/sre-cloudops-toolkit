#!/usr/bin/env bash
set -euo pipefail

# SSL Certificate Expiry Checker – warns if a domain's cert expires soon.
# Usage: ./check_ssl.sh example.com

DOMAIN="${1:?Usage: $0 <domain>}"
DAYS_WARN=30

enddate=$(echo | openssl s_client -servername "$DOMAIN" -connect "$DOMAIN":443 2>/dev/null \
          | openssl x509 -noout -enddate | cut -d= -f2)
expiry_epoch=$(date -d "$enddate" +%s)
now_epoch=$(date +%s)
days_left=$(( ($expiry_epoch - $now_epoch) / 86400 ))

echo "Domain: $DOMAIN"
echo "Expires: $enddate ($days_left days)"

if [ "$days_left" -lt "$DAYS_WARN" ]; then
    echo "WARNING: Certificate expires soon!"
    exit 1
else
    echo "OK"
fi