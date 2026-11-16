#!/usr/bin/env python3
"""SessionStart hook for learn_rust: sync before the first word of any lesson.

Why: on 2026-11-16 a PC session skipped the manual sync because the first message was
only "pause". A whole evening then ran on a Hook line that a cloud session had already
moved past (S1 steps 1-3 sat unmerged on a cloud branch). The sync is a hook now, so it
cannot be skipped.

What it does: git fetch; fast-forward the current branch; merge every remote branch that
is not merged yet (aborts and reports on a conflict); then prints the innings board.
Everything it prints lands in the teacher's context. It never pushes and always exits 0.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def git(*args, timeout=90):
    try:
        return subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True,
                              text=True, encoding="utf-8", errors="replace", timeout=timeout)
    except Exception as e:  # git missing, timeout
        return subprocess.CompletedProcess(args, 1, "", str(e))


def main():
    out = ["SESSION SYNC (hook, ran before this session's first message):"]
    f = git("fetch", "--prune", "-q")
    if f.returncode:
        out.append(f"- fetch FAILED: {f.stderr.strip()[:200]} -> state may be stale; say so")
    branch = git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    dirty = git("status", "--porcelain", "--untracked-files=no").stdout.strip()
    if dirty:
        out.append(f"- working tree not clean, pull and merges skipped:\n{dirty[:400]}")
    else:
        upstream = git("rev-parse", "--abbrev-ref", "@{u}")
        if upstream.returncode == 0:
            p = git("pull", "--ff-only", "-q")
            out.append(f"- {branch}: up to date with {upstream.stdout.strip()}" if p.returncode == 0
                       else f"- {branch}: pull --ff-only FAILED ({p.stderr.strip()[:200]})")
    unmerged = [b.strip() for b in git("branch", "-r", "--no-merged", "HEAD").stdout.splitlines()
                if b.strip() and "->" not in b]
    merged_any = False
    for b in unmerged:
        log = git("log", "--format=%ad %s", "--date=format:%m-%d %H:%M", f"HEAD..{b}").stdout
        lines = log.strip().splitlines()
        newest = lines[0] if lines else "?"
        if dirty:
            out.append(f"- UNMERGED {b}: {len(lines)} commits, newest {newest}. Merge by hand first.")
            continue
        m = git("merge", "--no-ff", "--no-edit", "-m", f"Merge {b} (session start hook)", b)
        if m.returncode == 0:
            merged_any = True
            out.append(f"- MERGED {b}: {len(lines)} commits, newest {newest}")
        else:
            git("merge", "--abort")
            out.append(f"- UNMERGED {b}: CONFLICT, merge by hand before teaching "
                       f"(CLAUDE.md step 0). Newest: {newest}")
    if not unmerged:
        out.append("- no unmerged remote branches")
    if merged_any:
        out.append("- merges are local only: push the branch after the open "
                   "(PC: main; cloud: the session's own branch)")
    out.append("- Read notes/PROGRESS.md (Hook) only now: it is current.")
    board = subprocess.run([sys.executable, str(ROOT / "tools" / "score.py"), "--chat"],
                           capture_output=True, text=True, encoding="utf-8", errors="replace",
                           timeout=60, cwd=ROOT)
    if board.returncode == 0 and board.stdout.strip():
        out.append("BOARD (show these lines at the open, copied exactly):")
        out.append(board.stdout.rstrip())
    else:
        out.append(f"BOARD failed: {(board.stderr or board.stdout).strip()[:300]}")
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    print("\n".join(out))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"SESSION SYNC hook crashed: {e}. Run CLAUDE.md step 0 by hand.")
    sys.exit(0)
