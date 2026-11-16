#!/usr/bin/env python3
"""Cricket scoreboard for the Ardan chase (the student's own rules, v2 of 2026-11-16).

Runs     = minutes of video (rounded up, at least 1) per item ticked. A PDF, Text or Quiz
           item is 1 run: open it, mark it complete, never study it. Target = all 301
           items (from notes/CHAPTERS.md).
Over     = one day, IST, ending at 03:00 (late study counts for the evening it started).
           Over 1 = first_over. Nothing falls before it; runs before it still count.
Par      = required run rate when the over opens: runs needed / bowled overs left.
Colour   = this over's runs against par: green >= par, orange >= 75 % of par, red below
           that or no runs. CRR is coloured the same way against the current par.
Wickets  (at most one per over, whatever the cause):
           a bowled over with 0 runs · 3 holds in one day · a hold not ended by its
           promised time + 15 min · 3 overs below par (red = 1, orange = 0.5).
Back     a beaten boss · 5 green overs in a row (partnership). Never above 10.
Rain     2 days for the whole chase, declared at least the day before: that over is
           not bowled, its par spreads over the rest, nothing falls.
All out  10 wickets: match lost and logged; follow-on at once with 10 new wickets, and
           the next over's par is 1.5 x.

Usage:  python tools/score.py [command] [--chat]
  show                     the board (default)
  tick <id> [<id> ...]     items done, e.g. tick 1.5.3 1.5.4   (untick <id> to correct)
  hold [22:00|30m|2h]      the student pauses and promises a return (default 15m)
  back                     the student is back after a hold
  rain YYYY-MM-DD          declare a rain day (tomorrow or later)
  boss M1                  a boss beaten: one wicket back
  card                     the scorecard (Sundays)
  alert [--dry|--test]     phone push via the coach's ntfy if this over is not green;
                           reads origin/main, never writes (Windows task "rcnc innings alert")

State: notes/innings.json. Every writing command also rewrites the Chapters, Pace needed
and Innings rows of notes/PROGRESS.md. Test hooks: SCORE_STATE, SCORE_PROGRESS,
SCORE_CHAPTERS, SCORE_NOW (local time, YYYY-MM-DDTHH:MM).
"""
import copy
import json
import math
import os
import re
import subprocess
import sys
import tomllib
import urllib.request
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = Path(os.environ.get("SCORE_STATE", ROOT / "notes" / "innings.json"))
PROGRESS = Path(os.environ.get("SCORE_PROGRESS", ROOT / "notes" / "PROGRESS.md"))
CHAPTERS = Path(os.environ.get("SCORE_CHAPTERS", ROOT / "notes" / "CHAPTERS.md"))
COACH_TOML = Path(r"D:/RustroverProjects/rust_learn/coach.toml")
GRACE = timedelta(minutes=15)

ANSI = {"green": "\x1b[32m", "orange": "\x1b[38;5;208m", "red": "\x1b[31m"}
DOT = {"green": "🟢", "orange": "🟠", "red": "🔴"}
RESET = "\x1b[0m"


# ---------- items ----------
def minutes(v):
    parts = [int(x) for x in v.split(":")] if re.fullmatch(r"[\d:]+", v) else []
    if len(parts) == 2:
        return parts[0] + parts[1] / 60
    if len(parts) == 3:
        return parts[0] * 60 + parts[1] + parts[2] / 60
    return 0.0


def load_items(st):
    items = {}
    for line in CHAPTERS.read_text(encoding="utf-8").splitlines():
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) < 5 or not re.fullmatch(r"\d+\.\d+\.\d+", c[0]):
            continue
        kind = c[2]
        if kind == "Video":
            runs = max(1, math.ceil(minutes(c[3])))
        elif kind == "Quiz":
            runs = st["runs_quiz"]
        else:
            runs = st["runs_page"]
        items[c[0]] = {"title": c[1], "kind": kind, "runs": runs, "done": c[4] == "done"}
    return items


def score(st, items):
    return sum(i["runs"] for k, i in items.items() if i["done"] or k in st["ticked"])


def target(items):
    return sum(i["runs"] for i in items.values())


def items_done(st, items):
    return sum(1 for k, i in items.items() if i["done"] or k in st["ticked"])


# ---------- time ----------
def d(s):
    return date.fromisoformat(s)


def tz(st):
    return timezone(timedelta(minutes=st["utc_offset_minutes"]))


def now_local(st):
    if os.environ.get("SCORE_NOW"):
        return datetime.fromisoformat(os.environ["SCORE_NOW"]).replace(tzinfo=tz(st))
    return datetime.now(tz(st))


def game_day(st, t):
    return (t - timedelta(hours=st["day_ends_hour"])).date()


def day_end(st, day):
    return datetime.combine(day + timedelta(days=1), time(st["day_ends_hour"]), tz(st))


def parse_until(now, arg):
    if not arg:
        return now + timedelta(minutes=15)
    m = re.fullmatch(r"(\d{1,2}):(\d{2})", arg)
    if m:
        t = now.replace(hour=int(m[1]), minute=int(m[2]), second=0, microsecond=0)
        return t if t > now else t + timedelta(days=1)
    m = re.fullmatch(r"(?:(\d+)h)?(?:(\d+)m?)?", arg)
    if m and (m[1] or m[2]):
        return now + timedelta(hours=int(m[1] or 0), minutes=int(m[2] or 0))
    sys.exit(f"hold: cannot read {arg!r}; use 22:00, 30m, 2h or 1h30m")


# ---------- overs ----------
def bowled(st, day):
    return day.isoformat() not in st["rain_days"]


def overs_left(st, day):
    """Bowled overs from `day` to the last over, `day` included."""
    last, n = d(st["last_over"]), 0
    while day <= last:
        n += bowled(st, day)
        day += timedelta(days=1)
    return n


def rrr(st, day, sc, tg):
    need, left = max(tg - sc, 0), overs_left(st, day)
    return need / left if left else float(need)


def colour(st, runs, par):
    if par <= 0 or runs >= par:
        return "green"
    if runs > 0 and runs >= st["orange_at"] * par:
        return "orange"
    return "red"


def wicket(st, day, how, ev):
    key = day.isoformat()
    if day < d(st["first_over"]):
        ev.append(f"No wicket before over 1: {how}")
        return
    if key in st["wicket_days"]:
        ev.append(f"Spared: {how} ({key}), one wicket already fell this over")
        return
    st["wicket_days"].append(key)
    st["wickets"].append({"date": key, "how": how})
    n = len(st["wickets"])
    ev.append(f"WICKET {n}: {how} ({key})")
    if n >= 10:
        st["matches"].append({"innings": st["innings"], "result": "all out",
                              "score": st["last_score"], "date": key})
        ev.append(f"ALL OUT. Match lost. Follow-on: innings {st['innings'] + 1}, "
                  f"10 wickets, next over's par x1.5.")
        st["innings"] += 1
        st["wickets"] = []
        st["below_par"] = 0
        st["green_run"] = 0
        st["follow_on_next"] = True


def restore(st, why, ev):
    if st["wickets"]:
        w = st["wickets"].pop()
        ev.append(f"WICKET BACK: {why} (cancels '{w['how']}' of {w['date']})")
    else:
        ev.append(f"{why}: all 10 wickets already in hand")


def open_over(st, day, sc, tg):
    st["open_day"] = day.isoformat()
    st["open_start"] = sc
    par = rrr(st, day, sc, tg)
    st["open_follow_on"] = False
    if bowled(st, day) and st["follow_on_next"]:
        par *= 1.5
        st["open_follow_on"] = True
        st["follow_on_next"] = False
    st["open_par"] = par


def finish(st, day, sc, tg, ev):
    st["finished"] = True
    res = "WON" if sc >= tg else f"LOST by {tg - sc} runs"
    st["matches"].append({"innings": st["innings"], "result": res, "score": sc,
                          "date": day.isoformat()})
    ev.append(f"MATCH {res} · {sc}/{tg}")


def close_over(st, day, sc, tg, ev):
    runs = sc - st["open_start"]
    if not bowled(st, day):
        st["overs"].append({"date": day.isoformat(), "rain": True, "runs": runs})
        ev.append(f"Rain day {day.isoformat()}: no over bowled ({runs} runs still count)")
    else:
        par = st["open_par"]
        c = colour(st, runs, par)
        st["overs"].append({"date": day.isoformat(), "par": round(par, 1), "runs": runs,
                            "colour": c, "follow_on": st["open_follow_on"]})
        ev.append(f"Over {sum(1 for o in st['overs'] if not o.get('rain'))} "
                  f"({day.isoformat()}): {runs} off par {par:.1f}, {c}")
        streak_out = False
        if c == "green":
            st["below_par"] = 0
            st["green_run"] += 1
            if st["green_run"] >= 5:
                st["green_run"] = 0
                restore(st, "partnership of 5 green overs", ev)
        else:
            st["green_run"] = 0
            st["below_par"] += 1 if c == "red" else 0.5
            if st["below_par"] >= 3:
                st["below_par"] = 0
                streak_out = True
        # Wickets last, so an all-out resets the counters for the new innings.
        if runs <= 0:
            wicket(st, day, "missed day (0 runs)", ev)
        if streak_out:
            wicket(st, day, "3 overs below par", ev)
    if day >= d(st["last_over"]):
        finish(st, day, sc, tg, ev)


def check_hold(st, now, ev):
    h = st["hold_open"]
    if h and now > datetime.fromisoformat(h["until"]) + GRACE:
        until = datetime.fromisoformat(h["until"])
        st["hold_open"] = None
        wicket(st, game_day(st, until), f"broken return (promised back at {until:%H:%M})", ev)


def advance(st, items, now, ev):
    st["last_score"] = sc = score(st, items)
    if st["finished"]:
        return
    check_hold(st, now, ev)
    today, first = game_day(st, now), d(st["first_over"])
    if today < first:
        return
    tg = target(items)
    if st["open_start"] is None:
        open_over(st, first, sc, tg)
    while not st["finished"] and d(st["open_day"]) < today:
        close_over(st, d(st["open_day"]), sc, tg, ev)
        if not st["finished"]:
            open_over(st, d(st["open_day"]) + timedelta(days=1), sc, tg)


# ---------- output ----------
def paint(text, c, chat):
    return f"{text} {DOT[c]}" if chat else f"{ANSI[c]}{text}{RESET}"


def status_tail(st, now):
    day = game_day(st, now).isoformat()
    holds = st["holds"]["count"] if st["holds"]["date"] == day else 0
    tail = (f"{10 - len(st['wickets'])} wkts · holds {holds}/3 today · "
            f"below par {st['below_par']:g}/3 · green run {st['green_run']}/5 · "
            f"rain days {st['rain_left']}")
    if st["hold_open"]:
        tail += f" · on hold, back by {datetime.fromisoformat(st['hold_open']['until']):%H:%M}"
    return tail


def board(st, items, now, chat):
    sc, tg = score(st, items), target(items)
    need = max(tg - sc, 0)
    n_items = f"{items_done(st, items)}/{len(items)} items"
    if st["finished"]:
        return [f"Match over: {st['matches'][-1]['result']} · {sc}/{tg} · {n_items}"]
    today, first = game_day(st, now), d(st["first_over"])
    if today < first:
        left = overs_left(st, first)
        return [f"Toss · over 1 starts {first.isoformat()} · {sc}/{tg} · "
                f"need {need} off {left} · RRR {rrr(st, first, sc, tg):.1f}",
                f"{n_items} · runs before over 1 count, no wicket can fall",
                status_tail(st, now)]
    inn = f"Inn {st['innings']} · " if st["innings"] > 1 else ""
    total = overs_left(st, first)
    if not bowled(st, today):
        return [f"{inn}Rain day {today.isoformat()} · {sc}/{tg} · need {need} off "
                f"{overs_left(st, today)} · nothing falls today", status_tail(st, now)]
    over_no = total - overs_left(st, today) + 1
    runs, par = sc - st["open_start"], st["open_par"]
    played = [o for o in st["overs"] if not o.get("rain")]
    if played:
        crr = sum(o["runs"] for o in played) / len(played)
        crr_txt = paint(f"CRR {crr:.1f}", colour(st, crr, par), chat)
    else:
        crr_txt = "CRR –"
    left = day_end(st, today) - now
    hh, mm = divmod(int(left.total_seconds()) // 60, 60)
    fo = " (follow-on x1.5)" if st["open_follow_on"] else ""
    return [f"{inn}Over {over_no}/{total} · {sc}/{tg} · need {need} off "
            f"{overs_left(st, today)} · RRR {rrr(st, today, sc, tg):.1f}",
            f"{paint(f'This over {runs}', colour(st, runs, par), chat)} par {par:.1f}{fo} · "
            f"{crr_txt} · {hh}h {mm:02d}m left · {n_items}",
            status_tail(st, now)]


def card(st, items, now, chat):
    sc, tg = score(st, items), target(items)
    played = [o for o in st["overs"] if not o.get("rain")]
    out = [f"Scorecard · innings {st['innings']} · {sc}/{tg} · "
           f"{items_done(st, items)}/{len(items)} items"]
    if played:
        cnt = {c: sum(1 for o in played if o["colour"] == c) for c in DOT}
        best = max(played, key=lambda o: o["runs"])
        crr = sum(o["runs"] for o in played) / len(played)
        out.append(f"Overs {len(played)} · green {cnt['green']} · orange {cnt['orange']} · "
                   f"red {cnt['red']} · best {best['runs']} on {best['date']} · CRR {crr:.1f}")
        if crr > 0:
            days = math.ceil(max(tg - sc, 0) / crr)
            eta = game_day(st, now) + timedelta(days=days)
            late = (eta - d(st["last_over"])).days
            verdict = "on time" if late <= 0 else f"{late} days after the last over"
            out.append(f"At this CRR the chase ends {eta.isoformat()}: {verdict}")
    lost = [w for w in st["wickets"]]
    out.append("Wickets: " + ("; ".join(f"{w['date']} {w['how']}" for w in lost) or "none"))
    if st["matches"]:
        out.append("Matches: " + "; ".join(f"inn {m['innings']} {m['result']} {m['date']}"
                                           for m in st["matches"]))
    if st["bosses"]:
        out.append("Bosses: " + ", ".join(st["bosses"]))
    return out


def sync_progress(st, items, now):
    if not PROGRESS.exists():
        return
    text = PROGRESS.read_text(encoding="utf-8")
    sc, tg = score(st, items), target(items)
    day = max(game_day(st, now), d(st["first_over"]))
    last = next((o["colour"] for o in reversed(st["overs"]) if not o.get("rain")), "none yet")
    rows = {
        "Chapters": (f"{items_done(st, items)} / {len(items)} items · runs {sc} / {tg} "
                     f"({round(sc * 100 / tg)} %)"),
        "Pace needed": (f"RRR {rrr(st, day, sc, tg):.1f} runs a day "
                        f"({max(tg - sc, 0)} off {overs_left(st, day)} overs; 1 run = 1 video min)"),
        "Innings": (f"innings {st['innings']} · {10 - len(st['wickets'])} wkts · "
                    f"below par {st['below_par']:g}/3 · green run {st['green_run']}/5 · "
                    f"rain days {st['rain_left']} · last over {last} (`python tools/score.py`)"),
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


# ---------- alert ----------
def remote_state():
    """The newest pushed state (a cloud session may have ticked items); local if git fails
    or the pushed file is an older format."""
    local = json.loads(STATE.read_text(encoding="utf-8"))
    try:
        subprocess.run(["git", "-C", str(ROOT), "fetch", "-q"], timeout=60, check=True,
                       capture_output=True)
        out = subprocess.run(["git", "-C", str(ROOT), "show", "origin/main:notes/innings.json"],
                             timeout=30, check=True, capture_output=True)
        remote = json.loads(out.stdout.decode("utf-8"))
    except Exception:
        return local
    if remote.get("version", 1) < local.get("version", 1):
        return local
    # Whichever side has ticked more items is the fresher one.
    return remote if len(remote.get("ticked", [])) >= len(local.get("ticked", [])) else local


def push_phone(title, body):
    cfg = tomllib.loads(COACH_TOML.read_text(encoding="utf-8"))
    server = cfg["phone_server"].rstrip("/")
    if not server.startswith("http"):
        server = "http://" + server
    req = urllib.request.Request(f"{server}/{cfg['phone_topic']}", data=body.encode("utf-8"),
                                 headers={"Title": title.encode("utf-8"), "Priority": "high",
                                          "Tags": "cricket"})
    urllib.request.urlopen(req, timeout=20).read()


def alert(argv):
    st = remote_state()
    items = load_items(st)
    now = now_local(st)
    ev = []
    advance(st, items, now, ev)  # in memory only
    lines = board(st, items, now, chat=True)
    today = game_day(st, now)
    on_field = not st["finished"] and today >= d(st["first_over"]) and bowled(st, today)
    runs = score(st, items) - (st["open_start"] or 0)
    red = on_field and colour(st, runs, st["open_par"]) != "green"
    if "--test" in argv or red or any(e.startswith("WICKET") for e in ev):
        body = "\n".join(ev + lines)
        if "--dry" in argv:
            print("would send:\n" + body)
        else:
            push_phone("rcnc innings", body)
            print("sent")
    else:
        print("no alert: " + (lines[1] if len(lines) > 1 else lines[0]))


# ---------- main ----------
def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    chat = "--chat" in argv
    args = [a for a in argv if a != "--chat"]
    cmd = args[0] if args else "show"
    if cmd == "alert":
        return alert(args[1:])
    st = json.loads(STATE.read_text(encoding="utf-8"))
    items = load_items(st)
    now = now_local(st)
    ev = []
    advance(st, items, now, ev)
    today = game_day(st, now)
    if cmd in ("tick", "untick"):
        if len(args) < 2:
            sys.exit(f"{cmd}: give item ids, e.g. {cmd} 1.5.3")
        for k in args[1:]:
            if k not in items:
                sys.exit(f"no item {k} in CHAPTERS.md")
            i = items[k]
            if cmd == "tick":
                if i["done"] or k in st["ticked"]:
                    ev.append(f"{k} already counted")
                else:
                    st["ticked"].append(k)
                    ev.append(f"+{i['runs']} · {k} {i['title']}")
            elif k in st["ticked"]:
                st["ticked"].remove(k)
                ev.append(f"-{i['runs']} · {k} untick")
        sc, tg = score(st, items), target(items)
        st["last_score"] = sc
        if sc >= tg and not st["finished"]:
            finish(st, today, sc, tg, ev)
    elif cmd == "hold":
        key = today.isoformat()
        if st["holds"]["date"] != key:
            st["holds"] = {"date": key, "count": 0}
        st["holds"]["count"] += 1
        until = parse_until(now, args[1] if len(args) > 1 else "")
        st["hold_open"] = {"at": now.isoformat(timespec="minutes"),
                           "until": until.isoformat(timespec="minutes")}
        ev.append(f"Hold {st['holds']['count']}/3 today · back by {until:%H:%M} "
                  f"(+15 min grace) or it is a wicket")
        if st["holds"]["count"] >= 3:
            wicket(st, today, "3 holds in one day", ev)
    elif cmd == "back":
        h = st["hold_open"]
        if not h:
            ev.append("No open hold")
        else:
            st["hold_open"] = None
            ev.append(f"Back at {now:%H:%M}, promised {datetime.fromisoformat(h['until']):%H:%M}: "
                      f"hold is free")
    elif cmd == "rain":
        day = d(args[1]) if len(args) > 1 else None
        if day is None or day <= today or day > d(st["last_over"]) or day < d(st["first_over"]):
            sys.exit("rain: give a date from tomorrow up to the last over (declare it the day before)")
        if day.isoformat() in st["rain_days"]:
            sys.exit(f"rain: {day} is already a rain day")
        if st["rain_left"] <= 0:
            sys.exit("rain: no rain days left")
        st["rain_days"].append(day.isoformat())
        st["rain_left"] -= 1
        ev.append(f"Rain day declared: {day.isoformat()} · {st['rain_left']} left")
    elif cmd == "boss":
        name = args[1].upper() if len(args) > 1 else ""
        if not re.fullmatch(r"M[1-9]", name) or name in st["bosses"]:
            sys.exit("boss: give M1..M9, each once")
        st["bosses"].append(name)
        restore(st, f"boss {name} beaten", ev)
    elif cmd not in ("show", "card"):
        sys.exit(f"unknown command {cmd!r} (see the top of tools/score.py)")
    STATE.write_text(json.dumps(st, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    sync_progress(st, items, now)
    for e in ev:
        print(e)
    for line in (card if cmd == "card" else board)(st, items, now, chat):
        print(line)


if __name__ == "__main__":
    main(sys.argv[1:])
