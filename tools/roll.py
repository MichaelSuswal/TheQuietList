#!/usr/bin/env python3
"""Hidden dice for The Quiet List, Archive Edition.

Every roll is appended to SPOILERS_do_not_open/rolls.log so the director's cut
can show them after credits. The narrator calls this instead of inventing a number.

Usage:
  python3 tools/roll.py d20 --tn 11 --why "tailing the sedan, prepared"
  python3 tools/roll.py d20 --tn 1 --why "..."    (tn 1 or lower: no roll, auto success)
Prints: result, margin, outcome (success/failure/auto).
"""
import argparse, datetime, pathlib, secrets, sys

LOG = pathlib.Path(__file__).resolve().parent.parent / "SPOILERS_do_not_open" / "rolls.log"

def main():
    p = argparse.ArgumentParser()
    p.add_argument("die", nargs="?", default="d20")
    p.add_argument("--tn", type=int, required=True, help="effective target number after skill and preparation")
    p.add_argument("--why", default="", help="what the roll is for, one line, spoiler-safe")
    a = p.parse_args()
    sides = int(a.die.lstrip("dD"))
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    LOG.parent.mkdir(parents=True, exist_ok=True)
    if a.tn <= 1:
        line = f"{stamp} auto  tn={a.tn}  {a.why}"
        print("auto success (no roll)")
    else:
        r = secrets.randbelow(sides) + 1
        margin = r - a.tn
        outcome = "success" if r >= a.tn else "failure"
        line = f"{stamp} {a.die}={r} tn={a.tn} margin={margin:+d} {outcome}  {a.why}"
        print(f"{a.die}={r} tn={a.tn} margin={margin:+d} {outcome}")
    with LOG.open("a") as f:
        f.write(line + "\n")

if __name__ == "__main__":
    main()
