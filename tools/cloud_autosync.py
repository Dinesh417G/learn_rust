#!/usr/bin/env python3
"""Stop hook for learn_rust: in a cloud session, commit and push the lesson files after
every reply.

Why: on 2026-11-18 a whole traits lesson (the vehicle example: trait Controls, Car, Truck,
the inspect bay) existed only in a cloud chat. Nothing was written or pushed, so the PC
session could not continue from it and the student had to paste it back. The student's
rule since then: "in claude code cloud session only explain me concepts and find a way to
sync with it". The teacher writes each concept to notes/chat_examples.md (CLAUDE.md); this
hook makes sure it reaches GitHub even when the teacher forgets to push. The PC's
SessionStart hook (tools/session_sync.py) merges the cloud branch before the next lesson.

Runs only in a cloud session: CLAUDE_CODE_REMOTE=true, or any non-Windows box (the PC is
Windows, cloud sessions are Linux). Stages only notes/, exercises/, rcnc/. Pushes the
current branch (a cloud session may push only its own branch). Never fails the turn:
always exits 0 and prints nothing on success.

Test without committing: CLAUDE_CODE_REMOTE=true CLOUD_AUTOSYNC_DRY=1 python tools/cloud_autosync.py < /dev/null
"""
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PATHS = ["notes", "exercises", "rcnc"]


def git(*args, timeout=60):
    try:
        return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True,
                              text=True, encoding="utf-8", errors="replace", timeout=timeout)
    except Exception as e:  # git missing, timeout
        return subprocess.CompletedProcess(args, 1, "", str(e))


def is_cloud():
    if os.environ.get("CLAUDE_CODE_REMOTE", "").lower() == "true":
        return True
    return not sys.platform.startswith("win")


def main():
    try:
        sys.stdin.read()  # the hook's JSON input; not needed
    except Exception:
        pass
    if not is_cloud():
        return
    dry = os.environ.get("CLOUD_AUTOSYNC_DRY") == "1"
    branch = git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    if dry:
        pending = git("status", "--porcelain", "--", *PATHS).stdout.strip()
        print(f"DRY cloud autosync on branch {branch!r}; would commit:\n{pending or '(nothing)'}")
        return
    git("add", "-A", "--", *PATHS)
    if git("diff", "--cached", "--quiet").returncode == 0:
        return  # nothing new to sync
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    git("commit", "-q", "-m", f"Cloud auto-sync {stamp} (Stop hook)")
    git("push", "-q", "-u", "origin", branch, timeout=90)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
