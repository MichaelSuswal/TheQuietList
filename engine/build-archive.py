#!/usr/bin/env python3
"""Regenerates the_quiet_list_v2_1_archive.md from the Standard file plus the two
archive parts, so the core rules never drift between editions.

Run from the repository root: python3 engine/build-archive.py
"""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
std = sorted(ROOT.glob("the_quiet_list_v*_standard.md"))[-1]
src = std.read_text()
setup = (ROOT / "engine" / "archive-setup.md").read_text()
layer = (ROOT / "engine" / "archive-layer.md").read_text()

src = src.replace("Standard Edition.", "Archive Edition.", 1)
note = [l for l in src.splitlines() if l.startswith("*Two editions exist.")][0]
src = src.replace(note, ("*Two editions exist. This is the Archive Edition: the same game, kept in a private GitHub repository that Claude "
    "manages for the player, with a sealed case written fresh for each campaign, independent character agents that "
    "think while she sleeps, a continuity checker, a drawn evidence board and map, and an optional sketchbook. "
    "Setup takes about fifteen minutes. The Standard Edition is one file with none of that machinery; players choose which to download.*"), 1)
src = src.replace("## ‼️ STARTUP SEQUENCE (in order, before anything else)",
                  setup + "\n## ‼️ STARTUP SEQUENCE (in order, before anything else)", 1)
src = re.sub(r"- \*\*Save block:\*\*[^\n]*", "- **Saves:** in this edition the repository is the save; see § THE RECORD below. No save blocks.", src, count=1)
src = src.replace("=== END ENGINE ===", layer + "\n=== END ENGINE ===", 1)
out = ROOT / std.name.replace("_standard", "_archive")
out.write_text(src)
print("wrote", out.name, len(src.splitlines()), "lines")
