#!/usr/bin/env python3
"""Convert a Suno catalog CSV into tracks.json for a streaming jukebox.

Usage: python3 tools/suno_csv_to_tracks.py drylands-radio/catalog.csv drylands-radio/tracks.json

Expected columns: Title, Suno URL, Duration, Style / Genre,
Lyrics or Instrumental, Mood Tags (comma-separated).
No audio is downloaded: the player streams each song from Suno's CDN by its ID.
"""
import csv, json, re, sys

def clean_title(t):
    t = t.replace("**", "").strip()
    t = re.sub(r'^[\s"“”]+|[\s"“”]+$', "", t)
    return t

def seconds(d):
    m, s = d.strip().split(":")
    return int(m) * 60 + int(s)

def main(src, dst):
    tracks, seen = [], set()
    with open(src, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            url = (row.get("Suno URL") or "").strip()
            m = re.search(r"/song/([0-9a-f-]{36})", url)
            if not m or m.group(1) in seen:
                continue
            sid = m.group(1)
            seen.add(sid)
            tracks.append({
                "id": sid,
                "title": clean_title(row["Title"]),
                "duration": row["Duration"].strip(),
                "seconds": seconds(row["Duration"]),
                "style": row["Style / Genre"].strip(),
                "vocals": row["Lyrics or Instrumental"].strip().lower() == "lyrics",
                "moods": [x.strip() for x in row["Mood Tags"].split(",") if x.strip()],
                "suno": url,
            })
    moods = []
    for t in tracks:
        for x in t["moods"]:
            if x not in moods:
                moods.append(x)
    with open(dst, "w", encoding="utf-8") as f:
        json.dump({"moods": moods, "tracks": tracks}, f, indent=1, ensure_ascii=False)
    print(f"{len(tracks)} tracks, moods: {moods}")

if __name__ == "__main__":
    main(*sys.argv[1:3])
