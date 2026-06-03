#!/bin/bash
set -euo pipefail

# Starts Xvfb, x11vnc, noVNC, and the game in one command.
# View the game at the forwarded port 6080 in VS Code's Ports tab.

install_vnc_deps_if_missing() {
	local missing=0
	command -v Xvfb >/dev/null 2>&1 || missing=1
	command -v x11vnc >/dev/null 2>&1 || missing=1
	command -v websockify >/dev/null 2>&1 || missing=1
	[[ -x /usr/share/novnc/utils/novnc_proxy ]] || missing=1

	if [[ "$missing" -eq 1 ]]; then
		echo "Installing missing VNC dependencies..."
		export DEBIAN_FRONTEND=noninteractive
		apt_sources_file="$(mktemp)"
		cat > "$apt_sources_file" << 'EOF'
deb http://deb.debian.org/debian bookworm main
deb http://deb.debian.org/debian bookworm-updates main
deb http://deb.debian.org/debian-security bookworm-security main
EOF

		sudo apt-get update \
			-o Dir::Etc::sourcelist="$apt_sources_file" \
			-o Dir::Etc::sourceparts=/dev/null
		sudo apt-get install -y --no-install-recommends \
			-o Dir::Etc::sourcelist="$apt_sources_file" \
			-o Dir::Etc::sourceparts=/dev/null \
			xvfb x11vnc novnc websockify
		rm -f "$apt_sources_file"
	fi
}

install_python_deps_if_missing() {
	if ! python -c "import pygame" >/dev/null 2>&1; then
		echo "Installing missing Python dependencies..."
		python -m pip install -r requirements.txt
	fi
}

install_vnc_deps_if_missing
install_python_deps_if_missing

# Set up XDG runtime dir
mkdir -p /tmp/runtime-$USER
chmod 700 /tmp/runtime-$USER
export XDG_RUNTIME_DIR=/tmp/runtime-$USER

# Kill only this project's existing instances.
pkill -9 -f "python game/main.py" 2>/dev/null || true
pkill -9 -f "x11vnc -display :99" 2>/dev/null || true
pkill -9 -f "novnc_proxy --vnc localhost:5900 --listen 6080" 2>/dev/null || true
pkill -9 -f "websockify --web /usr/share/novnc/ 6080 localhost:5900" 2>/dev/null || true
pkill -9 -f "Xvfb :99" 2>/dev/null || true
sleep 2

# Start VNC stack
echo "Starting Xvfb..."
Xvfb :99 -screen 0 1920x1080x24 &
sleep 1

echo "Starting x11vnc..."
x11vnc -display :99 -nopw -listen localhost -xkb -forever -quiet -rfbport 5900 &
sleep 1

echo "Starting noVNC..."
if [[ -x /usr/share/novnc/utils/novnc_proxy ]]; then
	/usr/share/novnc/utils/novnc_proxy --vnc localhost:5900 --listen 6080 &
else
	websockify --web /usr/share/novnc/ 6080 localhost:5900 &
fi
sleep 1

# Run the game
DISPLAY=:99 python game/main.py
