# -*- coding: utf-8 -*-
"""Enkratno (in nadaljevalno) iskanje koordinat za znamenitosti in lokale (OpenStreetMap Nominatim).
Rezultat: geocache.json  {iskalni niz: {lat, lon, name, cls, type} ali null}.
Zagon: python3 geocode.py   (ob ponovnem zagonu preskoči že najdeno; ~1 poizvedba/sekundo)"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "geocache.json")
UA = "potovalni-vodnik-geocode/1.0 (osebni potopisni vodnik)"


def load():
    if os.path.exists(CACHE):
        with open(CACHE, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save(c):
    with open(CACHE, "w", encoding="utf-8") as f:
        json.dump(c, f, ensure_ascii=False, indent=0, sort_keys=True)


def lookup(q):
    url = "https://nominatim.openstreetmap.org/search?format=jsonv2&limit=1&accept-language=en&q=" + urllib.parse.quote(q)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=25) as r:
        data = json.load(r)
    if not data:
        return None
    d = data[0]
    return {"lat": float(d["lat"]), "lon": float(d["lon"]), "name": d.get("display_name", "")[:140],
            "cls": d.get("category") or d.get("class", ""), "type": d.get("type", "")}


def variants(q):
    parts = [p.strip() for p in q.split(",") if p.strip()]
    out = [q]
    for n in range(len(parts) - 1, 1, -1):          # postopoma odreži podrobnosti na koncu
        out.append(", ".join(parts[:n]))
    if len(parts) >= 2:
        out.append(", ".join([parts[0], parts[-1]]))  # ime + mesto/regija
    seen, res = set(), []
    for v in out:
        if v not in seen:
            seen.add(v)
            res.append(v)
    return res


def queries():
    sys.path.insert(0, HERE)
    import gen as G
    import lj_content as C
    qs = []
    for guide in (G.GUIDE, C.GUIDE):
        for g in guide.values():
            for s in g.get("sights", []):
                if s.get("maps"):
                    qs.append(s["maps"])
            for c in g.get("food_categories", []):
                for p in c.get("places", []):
                    if p.get("maps"):
                        qs.append(p["maps"])
    seen, res = set(), []
    for q in qs:
        if q not in seen:
            seen.add(q)
            res.append(q)
    return res


def main():
    cache = load()
    qs = queries()
    todo = [q for q in qs if q not in cache]
    print(f"{len(qs)} poizvedb, {len(todo)} še manjka", flush=True)
    for i, q in enumerate(todo, 1):
        found = None
        for v in variants(q):
            try:
                found = lookup(v)
            except Exception as e:  # omrežna napaka — poskusi naslednjo različico
                print("  napaka:", e, flush=True)
                found = None
            time.sleep(1.15)
            if found:
                found["via"] = v
                break
        cache[q] = found
        print(f"[{i}/{len(todo)}] {'OK ' if found else '-- '} {q}", flush=True)
        if i % 10 == 0:
            save(cache)
    save(cache)
    print("končano:", sum(1 for v in cache.values() if v), "/", len(cache), "najdenih", flush=True)


if __name__ == "__main__":
    main()
