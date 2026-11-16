#!/usr/bin/env bash
# Puts the 20:00 innings alert on home-pi (always on), so the push comes with the PC off.
# Installed 2026-11-16. Run from the PC (Git Bash):  bash tools/pi-alert-setup.sh
# On the Pi: a clone of this public repo in ~/learn_rust and one crontab line that pulls
# it and runs `score.py alert` against the local ntfy (topic rust-coach). Other crontab
# lines are kept. Log: ~/learn_rust-alert.log on the Pi.
# The phone gets it anywhere: ntfy app subscribed via Tailscale (100.124.176.27:8093).
set -euo pipefail
PI="dinesh@192.168.0.12"
ssh -i ~/.ssh/id_pi -o BatchMode=yes "$PI" 'bash -s' <<'EOF'
set -e
[ -d ~/learn_rust ] || git clone -q https://github.com/Dinesh417G/learn_rust.git ~/learn_rust
LINE="0 20 * * * cd /home/dinesh/learn_rust && git pull -q --ff-only && SCORE_NTFY=http://127.0.0.1:8093/rust-coach python3 tools/score.py alert >> /home/dinesh/learn_rust-alert.log 2>&1"
(crontab -l 2>/dev/null | grep -v "learn_rust && git pull"; echo "$LINE") | crontab -
crontab -l | grep learn_rust
EOF
