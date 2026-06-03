#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

# Make sure startup script is executable even if post-create did not complete.
chmod +x start.sh

# Avoid restarting the stack if it is already running.
if pgrep -f "novnc_proxy --vnc localhost:5900 --listen 6080|websockify.*6080" >/dev/null 2>&1; then
	echo "noVNC already running on port 6080."
	exit 0
fi

echo "Starting pygame + noVNC stack in background..."
nohup bash ./start.sh > /tmp/pygame-novnc.log 2>&1 &

echo "Startup launched. Log file: /tmp/pygame-novnc.log"
