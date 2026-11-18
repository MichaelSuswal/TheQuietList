#!/usr/bin/env python3
"""The Keeper's meters: WEIGHT and HEAT computed outside the narrator's view.

The narrator never sets a meter. It logs facts to state/events.jsonl, one JSON
object per line, and this script computes both meters from fixed rules and
writes state/meters.json. The narrator reads only the stage and the band.

Event line: {"day": 12, "kind": "kill", "tags": ["clean","guilt:8"], "note": "..."}

Kinds and base effects (WEIGHT w, HEAT h):
  kill         w +22  h +18   tags: clean (w -6, h -10) messy (w +8, h +14) witness (h +10)
                              guilt:N  (N 0 to 10; w += (10 - N) * 1.5, the more innocent the heavier)
  violence     w +8   h +8    a beating, a threat with a blade; tags as above
  restraint    w -6   h 0     a kill she could have made and did not
  mercy        w -10  h 0     sparing a sentenced name at the moment
  sister       w -5   h 0     real time with Sujin (max one per day)
  rest         w -3   h 0     a real sleep (the sleep turn logs this)
  evidence     h +8           something of hers left behind
  cover        h -5           tracks covered, misdirection landed
  lielow       h -4           a full day out of sight
  exposure     h +12          seen by police or hunters in the act
  day          h +1           each day the case stays open (clock adds this)
Meters are clamped 0 to 100 and HEAT stays 0 until the first kill or violence.

Stages: WEIGHT 0..19 stage 0, 20..44 stage 1, 45..69 stage 2, 70+ stage 3.
Bands:  HEAT 0 dormant, 1..24 low, 25..49 rising, 50..74 high, 75+ critical.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
EV = ROOT / "state" / "events.jsonl"
OUT = ROOT / "state" / "meters.json"

BASE = {"kill": (22, 18), "violence": (8, 8), "restraint": (-6, 0), "mercy": (-10, 0),
        "sister": (-5, 0), "rest": (-3, 0), "evidence": (0, 8), "cover": (0, -5),
        "lielow": (0, -4), "exposure": (0, 12), "day": (0, 1)}

def clamp(x):
    return max(0, min(100, x))

def main():
    w = h = 0.0
    heat_live = False
    sister_days = set()
    if EV.exists():
        for line in EV.read_text().splitlines():
            if not line.strip():
                continue
            e = json.loads(line)
            k = e.get("kind")
            if k not in BASE:
                continue
            dw, dh = BASE[k]
            tags = e.get("tags", [])
            if k == "sister":
                if e.get("day") in sister_days:
                    continue
                sister_days.add(e.get("day"))
            if k in ("kill", "violence"):
                heat_live = True
                if "clean" in tags:
                    dw -= 6; dh -= 10
                if "messy" in tags:
                    dw += 8; dh += 14
                if "witness" in tags:
                    dh += 10
                for t in tags:
                    if t.startswith("guilt:"):
                        g = int(t.split(":")[1])
                        dw += (10 - g) * 1.5
            w = clamp(w + dw)
            if heat_live or dh < 0:
                h = clamp(h + dh)
    stage = 0 if w < 20 else 1 if w < 45 else 2 if w < 70 else 3
    band = "dormant" if not heat_live else "low" if h < 25 else "rising" if h < 50 else "high" if h < 75 else "critical"
    out = {"weight_stage": stage, "heat_band": band}
    OUT.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out))

if __name__ == "__main__":
    main()
