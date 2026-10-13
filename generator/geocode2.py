# -*- coding: utf-8 -*-
"""Drugi krog: poišče koordinate, ki jih Nominatim ni našel, prek Photon (OSM, mehkejše iskanje z vplivom lokacije).
Zagon: python3 geocode2.py  (dopolni geocache.json)"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen as G
import lj_content as C
import geocode as GC

UA = "potovalni-vodnik-geocode/1.0 (osebni potopisni vodnik)"


def photon(q, lat, lon):
    url = "https://photon.komoot.io/api/?limit=3&lang=en&lat=%s&lon=%s&q=%s" % (lat, lon, urllib.parse.quote(q))
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=25) as r:
        data = json.load(r)
    out = []
    for f in data.get("features", []):
        lo, la = f["geometry"]["coordinates"]
        p = f.get("properties", {})
        out.append({"lat": la, "lon": lo, "name": ", ".join(x for x in [p.get("name"), p.get("city") or p.get("county"), p.get("state")] if x),
                    "cls": p.get("osm_key", ""), "type": p.get("osm_value", ""), "via": "photon"})
    return out


def main():
    cache = GC.load()
    items = []
    for label, guide, maps in (("jp", G.GUIDE, G.MAPS), ("lj", C.GUIDE, C.MAPS)):
        for key, g in guide.items():
            m = maps.get(key) or (maps.get("center") if label == "lj" else None)
            if not m:
                continue
            rad = 60 if label == "jp" else 12
            for s in g.get("sights", []):
                if s.get("maps"):
                    items.append((s["maps"], s["name"], m, rad, False))
            for c in g.get("food_categories", []):
                for p in c.get("places", []):
                    if p.get("maps"):
                        items.append((p["maps"], p["name"], m, rad, True))
    todo = [it for it in items if not cache.get(it[0])]
    print(len(todo), "manjka", flush=True)
    for i, (q, name, m, rad, food) in enumerate(todo, 1):
        first = q.split(",")[0].strip()
        found = None
        for term in (first, name, first + " " + q.split(",")[-1].strip()):
            try:
                res = photon(term, m[0], m[1])
            except Exception as e:
                print("  napaka", e, flush=True)
                res = []
            time.sleep(1.0)
            for r in res:
                if GC and G._dist_km(m[0], m[1], r["lat"], r["lon"]) <= rad:
                    found = r
                    break
            if found:
                break
        cache[q] = found
        print(f"[{i}/{len(todo)}] {'OK ' if found else '-- '} {q}  ->  {(found or {}).get('name','')}", flush=True)
        if i % 10 == 0:
            GC.save(cache)
    GC.save(cache)
    print("končano", flush=True)


if __name__ == "__main__":
    main()
