#!/usr/bin/env bash
set -euo pipefail

export DEBIAN_FRONTEND=noninteractive

curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo gpg --batch --yes --dearmor -o /usr/share/keyrings/yarnkey.gpg
echo "deb [signed-by=/usr/share/keyrings/yarnkey.gpg] https://dl.yarnpkg.com/debian stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
sudo apt-get install -y --no-install-recommends \
  xvfb \
  x11vnc \
  novnc \
  websockify
rm -f "$apt_sources_file"

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
chmod +x start.sh
chmod +x .devcontainer/postStart.sh

echo "Codespace setup complete. Run ./start.sh and open port 6080 to view the game."
