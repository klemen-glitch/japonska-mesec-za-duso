# -*- coding: utf-8 -*-
"""Pripravi SQL za Telegram bota: dnevi, prehodi in nastavitve obeh potovanj (zagon: python3 gen_bot_seed.py > bot/seed.sql)."""
import importlib
import json
import sys

import gen as G
import lj_content as LJC


def q(v):
    if v is None:
        return "null"
    return "$$" + str(v).replace("$$", "$ $") + "$$"


def seed_trip(trip_id, tz, people, base_url):
    rows = []
    for d in G.ITINERARY.get("days", []):
        key = G.REGION_KEY.get(d["region"], "")
        loc = next((l for l in G.LOCATIONS if l["key"] == key), {})
        m = G.MAPS.get(key)
        lat, lon = (m[0], m[1]) if m else (None, None)
        rows.append(f"({q(trip_id)}, {d['day']}, {q(G.day_iso(d['day']))}, {q(d['region'])}, {q(key)}, {q(loc.get('name') or d['region'])}, "
                    f"{q(d['title'])}, {q(d['plan'])}, {lat if lat is not None else 'null'}, {lon if lon is not None else 'null'})")
    sql = ["delete from public.trip_days where trip_id = " + q(trip_id) + ";",
           "insert into public.trip_days (trip_id, day, iso, region, station, station_name, title, plan, lat, lon) values\n" + ",\n".join(rows) + ";"]
    legs = []
    for i, lg in enumerate(G.ITINERARY.get("legs", [])):
        legs.append(f"({q(trip_id)}, {i}, {q(lg['from'])}, {q(lg['to'])}, {q(lg['duration'])}, {q(lg['how'])}, {q(lg['tip'])})")
    sql.append("delete from public.trip_legs where trip_id = " + q(trip_id) + ";")
    if legs:
        sql.append("insert into public.trip_legs (trip_id, idx, from_r, to_r, dur, how, tip) values\n" + ",\n".join(legs) + ";")
    arr = "array[" + ", ".join(q(p) for p in people) + "]"
    sql.append(f"insert into public.trip_bot_settings (trip_id, tz, people) values ({q(trip_id)}, {q(tz)}, {arr}) "
               f"on conflict (trip_id) do update set tz = excluded.tz, people = excluded.people;")
    return "\n".join(sql)


def main():
    out = ["alter table public.trip_days add column if not exists station text, add column if not exists station_name text, add column if not exists lat double precision, add column if not exists lon double precision;",
           "insert into public.trip_bot_config (key, value) values ('app_base', 'https://klemen-glitch.github.io/japonska-mesec-za-duso') on conflict (key) do update set value = excluded.value;"]
    out.append(seed_trip("japonska", "Asia/Tokyo", G.CFG["people"], ""))
    # Ljubljana: preklopi globale gen.py na vsebino Ljubljane
    import gen_lj  # noqa: F401  (prepiše globale v gen)
    out.append(seed_trip("ljubljana", "Europe/Ljubljana", G.CFG["people"], ""))
    print("\n".join(out))


if __name__ == "__main__":
    main()
