#!/usr/bin/env python3
"""Seah's sketchbook: pencil portraits and the occasional painted scene. Optional.

Needs an OPENAI_API_KEY (a repository secret, or an environment variable when
run locally). Without a key the script says so and exits cleanly; the game
plays on without pictures.

Requests go in player/sketches/requests/<name>.json:
  {"kind": "portrait" | "scene", "subject": "the scar man",
   "card": "fifty-ish, heavyset, flat wide face, drinker's flush, white scar splitting the left eyebrow,
            half-lidded eyes that pretend to be slow", "shape": "square" | "wide"}
Output lands in player/sketches/<name>.png.

Rules: every recurring subject is drawn from its appearance card word for word; only what
Seah has actually seen; invented faces only, never a real person.
"""
import base64, json, os, pathlib, sys, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
REQ = ROOT / "player" / "sketches" / "requests"
OUT = ROOT / "player" / "sketches"
MODEL = os.environ.get("SKETCH_MODEL", "chatgpt-image-latest")

PORTRAIT = ("Graphite pencil portrait on cream paper, drawn from memory by a trained portraitist, 1990s Seoul. "
            "Loose confident strokes, cross-hatching in the shadows, unfinished edges, a few smudges, "
            "no color, no text, no border. Head and shoulders, three-quarter view, direct and unsentimental. Subject: ")
SCENE = ("Oil on canvas, late 1990s Seoul at night, rain-wet streets, sodium light and neon reflected on asphalt, "
         "grounded realism, muted umber and slate with one warm light source, no text, no border, no faces of real people. Scene: ")

def main():
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        print("No OPENAI_API_KEY; the sketchbook is off. The game plays without pictures.")
        return
    REQ.mkdir(parents=True, exist_ok=True)
    done = 0
    for f in sorted(REQ.glob("*.json")):
        r = json.loads(f.read_text())
        prompt = (PORTRAIT if r.get("kind", "portrait") == "portrait" else SCENE) + r.get("card", r.get("subject", ""))
        size = "1024x1024" if r.get("shape", "square") == "square" else "1536x1024"
        body = json.dumps({"model": MODEL, "prompt": prompt, "size": size, "n": 1}).encode()
        req = urllib.request.Request("https://api.openai.com/v1/images/generations", data=body,
                                     headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.load(resp)
        item = data["data"][0]
        if "b64_json" in item:
            png = base64.b64decode(item["b64_json"])
        else:
            with urllib.request.urlopen(item["url"], timeout=120) as img:
                png = img.read()
        (OUT / (f.stem + ".png")).write_bytes(png)
        f.unlink()
        done += 1
        print("drew", f.stem)
    print(f"{done} picture(s)")

if __name__ == "__main__":
    main()
