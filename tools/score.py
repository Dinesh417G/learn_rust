#!/usr/bin/env python3
"""Cricket scoreboard for the Ardan chase (the student's own rules, 2026-11-16).

Runs   = Ardan items ticked (target 301). One over = one day (IST).
Par    = required run rate when the over starts: runs needed / overs left.
Colour = this over's runs against par: green >= par, orange >= 75 % of par, red below
         that or no runs.
Wicket = a day with 0 runs · every 3rd hold · 3 overs in a row not green.
10 wickets = all out: match lost, logged, follow-on with 10 new wickets next ball.

Usage:
  python tools/score.py            show the board
  python tools/score.py run [N]    N items ticked now (default 1; negative to correct)
  python tools/score.py hold       the student asked to hold / pause
  add --chat for the emoji version to paste into chat

State: notes/innings.json. Also rewrites the Chapters, Pace needed and Innings rows of
notes/PROGRESS.md so the scoreboard never drifts.
"""
import json
import os
import re
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# Overridable for tests: SCORE_STATE, SCORE_PROGRESS, SCORE_TODAY (YYYY-MM-DD).
STATE = Path(os.environ.get("SCORE_STATE", ROOT / "notes" / "innings.json"))
PROGRESS = Path(os.environ.get("SCORE_PROGRESS", ROOT / "notes" / "PROGRESS.md"))

ANSI = {"green": "\x1b[32m", "orange": "\x1b[38;5;208m", "red": "\x1b[31m"}
DOT = {"green": "🟢", "orange": "🟠", "red": "🔴"}
RESET = "\x1b[0m"


def d(s):
    return date.fromisoformat(s)


def today(st):
    if os.environ.get("SCORE_TODAY"):
        return d(os.environ["SCORE_TODAY"])
    tz = timezone(timedelta(minutes=st["utc_offset_minutes"]))
    return datetime.now(tz).date()


def overs_total(st):
    return (d(st["last_over"]) - d(st["first_over"])).days + 1


def overs_left(st, day):
    """Overs left including `day` itself."""
    return max((d(st["last_over"]) - day).days + 1, 0)


def rrr(st, day, score):
    need = max(st["target"] - score, 0)
    left = overs_left(st, day)
    return need / left if left else float(need)


def colour(st, runs, par):
    if par <= 0 or runs >= par:
        return "green"
    if runs > 0 and runs >= st["orange_at"] * par:
        return "orange"
    return "red"


def wicket(st, day, how, events):
    st["wickets"].append({"date": day.isoformat(), "how": how})
    n = len(st["wickets"])
    events.append(f"WICKET {n}: {how} ({day.isoformat()})")
    if n >= 10:
        st["matches"].append({"innings": st["innings"], "result": "all out",
                              "score": st["score"], "date": day.isoformat()})
        events.append(f"ALL OUT at {st['score']}/{st['target']}. Match lost. "
                      f"Follow-on: innings {st['innings'] + 1}, 10 wickets.")
        st["innings"] += 1
        st["wickets"] = []
        st["holds"] = 0
        st["below_par_run"] = 0


def finish(st, day, events):
    st["finished"] = True
    won = st["score"] >= st["target"]
    res = "WON" if won else f"LOST by {st['target'] - st['score']} runs"
    st["matches"].append({"innings": st["innings"], "result": res,
                          "score": st["score"], "date": day.isoformat()})
    events.append(f"MATCH {res} · {st['score']}/{st['target']}")


def advance(st, now, events):
    """Open the first over when it is due and close every finished over."""
    if st["finished"] or now < d(st["first_over"]):
        return
    if st["open_start"] is None:
        st["open_start"] = st["score"]
        st["open_par"] = rrr(st, d(st["open_day"]), st["score"])
    while not st["finished"] and d(st["open_day"]) < now:
        day = d(st["open_day"])
        runs = st["score"] - st["open_start"]
        par = st["open_par"]
        c = colour(st, runs, par)
        st["overs"].append({"date": day.isoformat(), "par": round(par, 2),
                            "runs": runs, "colour": c})
        events.append(f"Over {len(st['overs'])} ({day.isoformat()}): "
                      f"{runs} off par {par:.2f}, {c}")
        if runs <= 0:
            wicket(st, day, "missed day (0 runs)", events)
        if c == "green":
            st["below_par_run"] = 0
        else:
            st["below_par_run"] += 1
            if st["below_par_run"] >= 3:
                st["below_par_run"] = 0
                wicket(st, day, "3 overs in a row below par", events)
        if day >= d(st["last_over"]):
            finish(st, day, events)
            break
        nxt = day + timedelta(days=1)
        st["open_day"] = nxt.isoformat()
        st["open_start"] = st["score"]
        st["open_par"] = rrr(st, nxt, st["score"])


def paint(text, c, chat):
    return f"{text} {DOT[c]}" if chat else f"{ANSI[c]}{text}{RESET}"


def board(st, now, chat):
    score, target = st["score"], st["target"]
    need = max(target - score, 0)
    wk = 10 - len(st["wickets"])
    tail = (f"{wk} wkts in hand · hold {st['holds'] % 3}/3 · "
            f"below par {st['below_par_run']}/3")
    if st["finished"]:
        last = st["matches"][-1]
        return [f"Match over: {last['result']} · {score}/{target}"]
    if now < d(st["first_over"]):
        left = overs_left(st, d(st["first_over"]))
        r = rrr(st, d(st["first_over"]), score)
        return [f"Toss · over 1 starts {st['first_over']} · {score}/{target} · "
                f"need {need} off {left} · RRR {r:.2f}",
                f"Runs tonight count, no over is bowled yet · {tail}"]
    over_no = (now - d(st["first_over"])).days + 1
    this_runs = score - st["open_start"]
    par = st["open_par"]
    live_rrr = rrr(st, now, score)
    closed = st["overs"]
    if closed:
        crr = sum(o["runs"] for o in closed) / len(closed)
        crr_txt = paint(f"CRR {crr:.2f}", colour(st, crr, par), chat)
    else:
        crr_txt = "CRR –"
    inn = f"Inn {st['innings']} · " if st["innings"] > 1 else ""
    return [f"{inn}Over {over_no}/{overs_total(st)} · {score}/{target} · need {need} · "
            f"RRR {live_rrr:.2f}",
            f"{paint(f'This over {this_runs}', colour(st, this_runs, par), chat)} "
            f"par {par:.2f} · {crr_txt} · {tail}"]


def sync_progress(st, now):
    if not PROGRESS.exists():
        return
    text = PROGRESS.read_text(encoding="utf-8")
    score, target = st["score"], st["target"]
    day = max(now, d(st["first_over"]))
    left = overs_left(st, day)
    r = rrr(st, day, score)
    last = st["overs"][-1]["colour"] if st["overs"] else "none yet"
    rows = {
        "Chapters": f"{score} / {target} ({round(score * 100 / target)} %)",
        "Pace needed": f"RRR {r:.2f} items a day ({max(target - score, 0)} off {left} overs)",
        "Innings": (f"{10 - len(st['wickets'])} wkts in hand · hold {st['holds'] % 3}/3 · "
                    f"below par {st['below_par_run']}/3 · last over {last} "
                    f"(`python tools/score.py`)"),
    }
    for key, val in rows.items():
        pat = re.compile(rf"^\| {re.escape(key)} \|.*\|$", re.M)
        line = f"| {key} | {val} |"
        if pat.search(text):
            text = pat.sub(lambda _: line, text, count=1)
        else:
            text = re.sub(r"^(\| Streak \|.*\|)$", lambda m: m.group(1) + "\n" + line,
                          text, count=1, flags=re.M)
    PROGRESS.write_text(text, encoding="utf-8")


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    chat = "--chat" in argv
    args = [a for a in argv if a != "--chat"]
    st = json.loads(STATE.read_text(encoding="utf-8"))
    now = today(st)
    events = []
    advance(st, now, events)
    cmd = args[0] if args else "show"
    if cmd == "run":
        n = int(args[1]) if len(args) > 1 else 1
        st["score"] = min(max(st["score"] + n, 0), st["target"])
        if st["score"] >= st["target"] and not st["finished"]:
            finish(st, now, events)
    elif cmd == "hold":
        st["holds"] += 1
        if st["holds"] % 3 == 0:
            wicket(st, now, "3 holds", events)
    elif cmd != "show":
        sys.exit(f"unknown command {cmd!r}: use show, run [N] or hold")
    STATE.write_text(json.dumps(st, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    sync_progress(st, now)
    for e in events:
        print(e)
    for line in board(st, now, chat):
        print(line)


if __name__ == "__main__":
    main(sys.argv[1:])
