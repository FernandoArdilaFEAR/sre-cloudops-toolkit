#!/usr/bin/env bash
set -euo pipefail

# System Health Report – displays CPU, memory, disk usage and top processes.
# Usage: ./system_health.sh

echo "=== CPU Usage ==="
top -bn1 | grep "Cpu(s)" | awk '{print "User: "$2"% System: "$4"% Idle: "$8"%"}'

echo -e "\n=== Memory Usage ==="
free -h | awk '/^Mem:/ {print "Used: "$3" / Total: "$2" ("$3/$2*100"%)"}'

echo -e "\n=== Disk Usage ==="
df -h / | awk 'NR==2 {print "Used: "$3" / Total: "$2" ("$5" used)"}'

echo -e "\n=== Top 5 CPU Processes ==="
ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%cpu | head -6