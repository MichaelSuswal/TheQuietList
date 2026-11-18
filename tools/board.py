#!/usr/bin/env python3
"""Draws the evidence board and the Seoul map from the record, as SVG.

Input: player/board.json, maintained by the narrator from what Seah knows.
Output: player/board.svg and player/map.svg. Both are redrawn from the record
every time, so ground and leads cannot be lost.

board.json shape:
{
  "people": [{"id":"park","name":"Detective Park","tag":"tired decent face","role":"the Javert",
              "list": false, "grade":"seen"}],
  "evidence": [{"id":"watch","name":"the watch","grade":"seen","note":"effects list disproved"}],
  "places": [{"id":"sagori","name":"Sagori Tea Room","district":"Cheongnyangni","grade":"seen"}],
  "links": [{"from":"park","to":"watch","label":"never shown"}],
  "next_rung": "Read box #15 in Junho's hand"
}
grade: seen (solid), reported (dashed, with its source in note), rumored (faint).
list: true draws the person as a sentenced name (dark card).
"""
import json, math, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "player" / "board.json"

GRADE = {"seen": ("#2b2b2b", "none", 1.0), "reported": ("#555", "6,4", 0.9), "rumored": ("#888", "2,4", 0.55)}

# 1997 Seoul districts on a schematic grid (x, y), north at top, river as a band.
DIST = {"Mapo": (120, 260), "Yeongdeungpo": (150, 420), "Yongsan": (300, 330), "Jongno": (330, 170),
        "Jung": (360, 240), "Euljiro": (400, 230), "Dongdaemun": (470, 190), "Cheongnyangni": (560, 180),
        "Seongdong": (530, 290), "Seocho": (420, 470), "Gangnam": (520, 450), "Yeoksam": (560, 470),
        "Dogok": (600, 520)}

def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def card(x, y, w, h, title, sub, grade, dark=False):
    stroke, dash, op = GRADE.get(grade, GRADE["seen"])
    fill = "#1f1f1f" if dark else "#fbf7ee"
    fg = "#f4ecd8" if dark else "#222"
    return (f'<g opacity="{op}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="1.5" stroke-dasharray="{dash}"/>'
            f'<text x="{x+8}" y="{y+18}" font-family="Georgia,serif" font-size="13" fill="{fg}">{esc(title)}</text>'
            f'<text x="{x+8}" y="{y+34}" font-family="Georgia,serif" font-size="10" fill="{fg}" opacity="0.8">{esc(sub)}</text></g>')

def draw_board(d):
    W, H = 900, 640
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
           f'<rect width="{W}" height="{H}" fill="#e9e1cf"/>',
           '<text x="20" y="30" font-family="Georgia,serif" font-size="18" fill="#222">The board</text>']
    pos = {}
    people = d.get("people", [])
    ev = d.get("evidence", [])
    places = d.get("places", [])
    cols = [(people, 40, "people"), (ev, 340, "evidence"), (places, 640, "places")]
    for items, x, _ in cols:
        for i, it in enumerate(items):
            y = 60 + i * 62
            pos[it["id"]] = (x + 110, y + 24)
            sub = it.get("tag") or it.get("note") or it.get("district") or ""
            out.append(card(x, y, 220, 48, it["name"], sub, it.get("grade", "seen"), it.get("list", False)))
    for l in d.get("links", []):
        a, b = pos.get(l["from"]), pos.get(l["to"])
        if not a or not b:
            continue
        out.append(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="#8b1e1e" stroke-width="1" opacity="0.7"/>')
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        if l.get("label"):
            out.append(f'<text x="{mx}" y="{my-3}" font-family="Georgia,serif" font-size="9" fill="#8b1e1e" text-anchor="middle">{esc(l["label"])}</text>')
    if d.get("next_rung"):
        out.append(f'<rect x="20" y="{H-50}" width="{W-40}" height="34" fill="#1f1f1f"/>'
                   f'<text x="30" y="{H-28}" font-family="Georgia,serif" font-size="13" fill="#f4ecd8">Next: {esc(d["next_rung"])}</text>')
    out.append("</svg>")
    return "\n".join(out)

def draw_map(d):
    W, H = 720, 600
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
           f'<rect width="{W}" height="{H}" fill="#efe8d6"/>',
           '<path d="M0,370 C150,340 300,400 450,380 S650,360 720,390 L720,420 C600,400 450,420 300,440 S120,380 0,410 Z" fill="#b9c7cf" opacity="0.8"/>',
           '<text x="20" y="28" font-family="Georgia,serif" font-size="18" fill="#222">Seoul, as she knows it</text>']
    for name, (x, y) in DIST.items():
        out.append(f'<text x="{x}" y="{y}" font-family="Georgia,serif" font-size="11" fill="#666" text-anchor="middle">{name}</text>')
    by = {}
    for p in d.get("places", []):
        by.setdefault(p.get("district"), []).append(p)
    for dist, items in by.items():
        if dist not in DIST:
            continue
        x0, y0 = DIST[dist]
        for i, p in enumerate(items):
            ang = i * 2 * math.pi / max(1, len(items))
            x, y = x0 + 26 * math.cos(ang), y0 + 18 + 22 * math.sin(ang)
            stroke, dash, op = GRADE.get(p.get("grade", "seen"), GRADE["seen"])
            out.append(f'<g opacity="{op}"><circle cx="{x:.0f}" cy="{y:.0f}" r="5" fill="#8b1e1e" stroke="{stroke}" stroke-dasharray="{dash}"/>'
                       f'<text x="{x+8:.0f}" y="{y+4:.0f}" font-family="Georgia,serif" font-size="10" fill="#222">{esc(p["name"])}</text></g>')
    out.append("</svg>")
    return "\n".join(out)

def main():
    d = json.loads(SRC.read_text()) if SRC.exists() else {}
    (ROOT / "player" / "board.svg").write_text(draw_board(d))
    (ROOT / "player" / "map.svg").write_text(draw_map(d))
    print("wrote player/board.svg and player/map.svg")

if __name__ == "__main__":
    main()
