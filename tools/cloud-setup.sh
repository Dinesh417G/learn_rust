#!/usr/bin/env bash
# Make sure a Rust toolchain exists. For Claude Code cloud sessions (Linux) or any fresh box.
# Usage: bash tools/cloud-setup.sh   then, in every later shell call:  . "$HOME/.cargo/env"
set -u
[ -f "$HOME/.cargo/env" ] && . "$HOME/.cargo/env"

if ! command -v cargo >/dev/null 2>&1; then
  echo "cargo not found: installing rustup (minimal profile + clippy + rustfmt)"
  if curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs \
      | sh -s -- -y --profile minimal -c clippy -c rustfmt; then
    . "$HOME/.cargo/env"
  else
    echo "NO COMPILER: the rustup install failed (network policy of this environment?)."
    echo "Teacher: do not invent compiler output. Predict-only steps, verify on the PC later."
    exit 0
  fi
fi

rustc --version && cargo --version && echo "compiler ready"
