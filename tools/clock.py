#!/usr/bin/env python3
"""The 49-day clock for The Quiet List, Archive Edition.

Reads state/campaign.json for the death date (day 1 of 49) and reports the
current day, weekday, rite days and days remaining. The narrator advances the
day with --set or --advance; the status line is built from this, never from memory.

Usage:
  python3 tools/clock.py                 show current day
  python3 tools/clock.py --advance 1     move one day forward
  python3 tools/clock.py --set 12        jump to day 12 (corrections only)
"""
import argparse, datetime, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
CAMP = ROOT / "state" / "campaign.json"
RITES = [7, 14, 21, 28, 35, 42, 49]

def load():
    return json.loads(CAMP.read_text()) if CAMP.exists() else {}

def save(c):
    CAMP.write_text(json.dumps(c, indent=2, ensure_ascii=False) + "\n")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--advance", type=int, default=0)
    p.add_argument("--set", type=int)
    a = p.parse_args()
    c = load()
    if "death_date" not in c:
        print("state/campaign.json has no death_date; set it at the cold open (YYYY-MM-DD).")
        return
    day = int(c.get("day", 1))
    if a.set:
        day = a.set
    day += a.advance
    c["day"] = day
    save(c)
    d0 = datetime.date.fromisoformat(c["death_date"])
    today = d0 + datetime.timedelta(days=day - 1)
    nxt = next((r for r in RITES if r >= day), None)
    print(f"Day {day} of 49 · {today.strftime('%A, %d %b %Y')}")
    print(f"Rite day: {'yes' if day in RITES else 'no'} · next rite: day {nxt} · days left: {49 - day}")

if __name__ == "__main__":
    main()
