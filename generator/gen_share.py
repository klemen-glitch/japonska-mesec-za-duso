# -*- coding: utf-8 -*-
"""Javna stran /javno/: vstavi OG oznake (Facebook) in za vsak dan ustvari »share« stran /javno/dan/<datum>/.

Podatke prebere iz javnega RPC trip_public_get (isti, ki ga uporablja stran). Brez omrežja ustvari stran brez slik.
Zagon: python3 gen_share.py [mapa_site]   (kliče ga tudi gen_site.py in GitHub Actions)
"""
import html
import json
import os
import re
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
SB = "https://clpwjvcuvpnjtkxokkqh.supabase.co"
KEY = "sb_publishable_izP9L69-Yrlc3U_uNhc29A_aoG_d8uz"
PUBLIC_URL = "https://klemen-glitch.github.io/japonska-mesec-za-duso/javno/"
TRIP_KEY = "mesec-za-dusu"
MON = ["januar", "februar", "marec", "april", "maj", "junij", "julij", "avgust", "september", "oktober", "november", "december"]


def fetch():
    try:
        req = urllib.request.Request(SB + "/rest/v1/rpc/trip_public_get", data=json.dumps({"p_key": TRIP_KEY}).encode(),
                                     headers={"apikey": KEY, "Content-Type": "application/json"})
        return json.load(urllib.request.urlopen(req, timeout=25))
    except Exception as e:  # noqa
        print("javno: podatkov ni mogoče prebrati:", e)
        return None


def img_url(path):
    from urllib.parse import quote
    return SB + "/storage/v1/object/public/trip_album/" + "/".join(quote(p) for p in path.split("/"))


def e(s):
    return html.escape(s or "", quote=True)


def excerpt(body, n=220):
    paras = [p.strip() for p in (body or "").split("\n\n") if p.strip() and not p.strip().startswith("ℹ️")]
    t = " ".join(paras).replace("\n", " ")
    t = re.sub(r"\s+", " ", t)
    return t if len(t) <= n else t[:n].rsplit(" ", 1)[0] + " …"


def dlab(iso):
    y, m, d = iso.split("-")
    return "%d. %s" % (int(d), MON[int(m) - 1])


def og(title, desc, url, image, typ="website"):
    out = ['<meta property="og:site_name" content="Mesec za dušo">',
           '<meta property="og:title" content="%s">' % e(title),
           '<meta property="og:description" content="%s">' % e(desc),
           '<meta property="og:url" content="%s">' % e(url),
           '<meta name="twitter:card" content="summary_large_image">']
    if image:
        out += ['<meta property="og:image" content="%s">' % e(image), '<meta name="twitter:image" content="%s">' % e(image)]
    return "\n".join(out)


SHARE_PAGE = """<!DOCTYPE html>
<html lang="sl"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<meta property="og:type" content="article">
<meta property="og:locale" content="sl_SI">
%(og)s
<link rel="canonical" href="%(url)s">
<script>location.replace("../../?dan=%(iso)s");</script>
<noscript><meta http-equiv="refresh" content="0; url=../../?dan=%(iso)s"></noscript>
<style>body{font:17px/1.5 -apple-system,system-ui,sans-serif;margin:0;padding:32px 20px;text-align:center;background:#f7f1e6;color:#1d2236}a{color:#c9372c;font-weight:600}</style>
</head><body>
<h1 style="font-family:Georgia,serif">%(title)s</h1>
<p>%(desc)s</p>
<p><a href="../../?dan=%(iso)s">Preberi celoten zapis →</a></p>
</body></html>
"""


def build(site_dir):
    data = fetch()
    src = os.path.join(HERE, "public", "javno.html")
    with open(src, encoding="utf-8") as f:
        tpl = f.read()
    stories = (data or {}).get("stories") or []
    latest_img = ""
    for s in reversed(stories):
        if s.get("photos"):
            latest_img = img_url(s["photos"][0])
            break
    title = "Mesec za dušo — potopis iz Japonske"
    desc = "Moja zgodba o mesecu dni na Japonskem s tremi prijateljicami. Beri, kako nam gre, dan za dnem, z utrinki in zanimivostmi o krajih."
    try:
        vj = json.load(open(os.path.join(HERE, "videos.json"), encoding="utf-8"))
        vids = {x["key"]: [{"id": v["id"], "title": v["title"]} for v in x.get("videos", [])[:3]] for x in vj}
    except Exception:  # noqa
        vids = {}
    tpl = tpl.replace("/*__VIDS__*/{}", json.dumps(vids, ensure_ascii=False))
    page = (tpl.replace("__TITLE__", e(title)).replace("__DESC__", e(desc)).replace("__OG_TYPE__", "website")
            .replace("__OG_META__", og(title, desc, PUBLIC_URL, latest_img)))
    out = os.path.join(site_dir, "javno")
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)
    n = 0
    for s in stories:
        t = "Dan %s: %s — Mesec za dušo" % (s["day"], s.get("title") or "")
        d = excerpt(s.get("body"))
        img = img_url(s["photos"][0]) if s.get("photos") else latest_img
        u = PUBLIC_URL + "dan/" + s["iso"] + "/"
        folder = os.path.join(out, "dan", s["iso"])
        os.makedirs(folder, exist_ok=True)
        with open(os.path.join(folder, "index.html"), "w", encoding="utf-8") as f:
            f.write(SHARE_PAGE % {"title": e(t), "desc": e(d), "og": og(t, d, u, img, "article"), "url": e(u), "iso": s["iso"]})
        n += 1
    print("javno: stran + %d share strani (%s)" % (n, "z slikami" if latest_img else "brez slik"))


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.abspath(os.path.join(HERE, "..")), "site"))
