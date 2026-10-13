# -*- coding: utf-8 -*-
"""Koledar potovanja (.ics): dnevi poti, nastanitve, prevozi in (če so podane ure) časovni dogodki."""
import datetime as dt
import hashlib
import re

CRLF = "\r\n"


def _esc(t):
    return (t or "").replace("\\", "\\\\").replace(";", "\;").replace(",", "\\,").replace("\r", "").replace("\n", "\\n")


def _fold(line):
    out, cur = [], b""
    for ch in line:
        b = ch.encode("utf-8")
        if len(cur) + len(b) > 74:
            out.append(cur.decode("utf-8"))
            cur = b" " + b
        else:
            cur += b
    out.append(cur.decode("utf-8"))
    return CRLF.join(out)


def _d(iso):
    return iso.replace("-", "")


def _uid(*parts):
    return hashlib.sha1("|".join(parts).encode("utf-8")).hexdigest()[:20] + "@potovanja"


def build(G, base_url):
    """G = modul gen (z nastavitvami potovanja)."""
    ev = []
    stamp = dt.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    trip = G.CFG["title"]
    days = G.ITINERARY.get("days", [])
    stations = {l["key"]: l for l in G.LOCATIONS}

    def add(summary, start, end=None, desc="", loc="", timed=False, alarm=None, uid=None, url=None):
        lines = ["BEGIN:VEVENT", f"UID:{uid or _uid(summary, start)}", f"DTSTAMP:{stamp}"]
        if timed:
            lines += [f"DTSTART:{start}", f"DTEND:{end}"]
        else:
            lines += [f"DTSTART;VALUE=DATE:{start}", f"DTEND;VALUE=DATE:{end}"]
        lines.append(f"SUMMARY:{_esc(summary)}")
        if desc:
            lines.append(f"DESCRIPTION:{_esc(desc)}")
        if loc:
            lines.append(f"LOCATION:{_esc(loc)}")
        if url:
            lines.append(f"URL:{url}")
        if alarm:
            lines += ["BEGIN:VALARM", "ACTION:DISPLAY", f"DESCRIPTION:{_esc(summary)}", f"TRIGGER:{alarm}", "END:VALARM"]
        lines.append("END:VEVENT")
        ev.append(lines)

    last_region = None
    for d in days:
        iso = G.day_iso(d["day"])
        nxt = (dt.date.fromisoformat(iso) + dt.timedelta(days=1)).isoformat()
        key = G.REGION_KEY.get(d["region"], "")
        st = stations.get(key, {})
        name = st.get("name", d["region"])
        page = f"{base_url}/{key}.html" if key else base_url + "/"
        add(f'{st.get("emoji", "📅")} Dan {d["day"]} · {name}', _d(iso), _d(nxt),
            f'{d["title"]}\n\n{d["plan"]}\n\nVodnik: {page}', loc=name, url=page, uid=_uid(trip, "dan", str(d["day"])))
        # prehod med kraji
        if last_region is not None and d["region"] != last_region:
            leg = next((lg for lg in G.ITINERARY.get("legs", []) if lg["from"] == last_region and lg["to"] == d["region"]), None) \
                or next((lg for lg in G.ITINERARY.get("legs", []) if lg["to"] == d["region"]), None)
            if leg:
                links = "\n".join(f"{a}: {b}" for a, b in G.LEG_LINKS.get((leg["from"], leg["to"]), []))
                add(f'🚉 Premik: {leg["from"]} → {leg["to"]}', _d(iso), _d(nxt),
                    f'{leg["how"]}\nČas: {leg["duration"]}\n💡 {leg["tip"]}' + (f"\n\n{links}" if links else ""),
                    uid=_uid(trip, "premik", str(d["day"])), alarm="-PT15H")
        last_region = d["region"]
    # prihod in odhod (prvi/zadnji prehod)
    legs = G.ITINERARY.get("legs", [])
    if legs and days:
        first = legs[0]
        if first["from"].lower().startswith(("letališče", "letalisce")):
            iso = G.day_iso(days[0]["day"]); nxt = (dt.date.fromisoformat(iso) + dt.timedelta(days=1)).isoformat()
            add(f'✈️ Prihod: {first["from"]} → {first["to"]}', _d(iso), _d(nxt), f'{first["how"]}\nČas: {first["duration"]}\n💡 {first["tip"]}',
                uid=_uid(trip, "prihod"))
        lastl = legs[-1]
        if "letališče" in lastl["to"].lower() or "kansai" in lastl["to"].lower():
            iso = G.day_iso(days[-1]["day"]); nxt = (dt.date.fromisoformat(iso) + dt.timedelta(days=1)).isoformat()
            add(f'✈️ Odhod: {lastl["from"]} → {lastl["to"]}', _d(iso), _d(nxt), f'{lastl["how"]}\nČas: {lastl["duration"]}\n💡 {lastl["tip"]}',
                uid=_uid(trip, "odhod"), alarm="-PT15H")
    # nastanitve
    for key, lod in G.LODGING.items():
        if lod.get("optional"):
            continue
        dates = G.stay_dates(key)
        if not dates:
            continue
        ci, co = dates
        st = stations.get(key, {})
        body = lod.get("booked") or lod.get("where") or ""
        add(f'🏨 Nastanitev: {st.get("name", key)}', _d(ci), _d(co), f'{body}\n\nPodrobnosti: {base_url}/{key}.html#prespati',
            loc=st.get("name", ""), uid=_uid(trip, "nastanitev", key))
    # časovni dogodki iz predloga dneva (pri postajah, kjer so ure oblike 9.00)
    for key, g in G.GUIDE.items():
        plan = g.get("day_plan", [])
        times = [(p, re.match(r"^(\d{1,2})[.:](\d{2})$", p["time"].strip())) for p in plan]
        if not times or not all(m for _, m in times):
            continue
        dayrow = next((d for d in days if G.REGION_KEY.get(d["region"]) == key), None)
        if not dayrow:
            continue
        iso = G.day_iso(dayrow["day"])
        for i, (p, m) in enumerate(times):
            h, mi = int(m.group(1)), int(m.group(2))
            start = dt.datetime.fromisoformat(iso) + dt.timedelta(hours=h, minutes=mi)
            if i + 1 < len(times):
                m2 = times[i + 1][1]
                end = dt.datetime.fromisoformat(iso) + dt.timedelta(hours=int(m2.group(1)), minutes=int(m2.group(2)))
            else:
                end = start + dt.timedelta(hours=1)
            add(f'⏱️ {stations.get(key, {}).get("name", key)}: {p["time"]}', start.strftime("%Y%m%dT%H%M%S"), end.strftime("%Y%m%dT%H%M%S"),
                p["what"], timed=True, alarm="-PT15M", uid=_uid(trip, "ura", key, str(i)))
    out = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Potovalni vodniki//SL", "CALSCALE:GREGORIAN",
           f"X-WR-CALNAME:{_esc(trip)}"]
    for lines in ev:
        out += lines
    out.append("END:VCALENDAR")
    return CRLF.join(_fold(l) for l in out) + CRLF
