# -*- coding: utf-8 -*-
"""Graditelji povezav za rezervacije, prevoz in vstopnice (vsi URL-ji so javne iskalne/uradne strani)."""
import datetime as dt
from urllib.parse import quote, urlencode

_MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def _d(iso):
    y, m, d = (int(x) for x in iso.split("-"))
    return dt.date(y, m, d)


def en_date(iso):
    d = _d(iso)
    return f"{_MON[d.month - 1]} {d.day} {d.year}"


def nights(ci, co):
    return (_d(co) - _d(ci)).days


def booking(q, ci=None, co=None, adults=4, rooms=2, filters=True):
    """Booking.com iskanje: datumi, osebe in sobe vnaprej; neobvezno brezplačen preklic + ocena 8+."""
    p = {"ss": q, "group_adults": adults, "no_rooms": rooms, "group_children": 0,
         "selected_currency": "EUR", "lang": "en-gb"}
    if ci and co:
        p.update({"checkin": ci, "checkout": co})
    if filters:
        p["nflt"] = "fc=2;review_score=80"
    return "https://www.booking.com/searchresults.html?" + urlencode(p)


def airbnb(slug, ci=None, co=None, adults=4, bedrooms=2):
    """Airbnb: cela nastanitev, vsaj 2 spalnici, 4 gostje."""
    p = [("adults", adults), ("room_types[]", "Entire home/apt"), ("min_bedrooms", bedrooms)]
    if ci and co:
        p = [("checkin", ci), ("checkout", co)] + p
    return f"https://www.airbnb.com/s/{quote(slug, safe='-')}/homes?" + urlencode(p, quote_via=quote)


def google_hotels(q, ci=None, co=None, adults=4):
    """Google Hotels (primerja Booking, Agodo, Expedio in spletne strani hotelov)."""
    text = f"hotels in {q}"
    if ci and co:
        text += f" {en_date(ci)} to {en_date(co)} {adults} guests"
    return "https://www.google.com/travel/search?" + urlencode({"q": text, "hl": "en", "curr": "EUR"}, quote_via=quote)


def gdir(frm, to, mode="transit"):
    """Google Zemljevidi: pot med dvema krajema (vozni red javnega prevoza)."""
    return "https://www.google.com/maps/dir/?" + urlencode(
        {"api": 1, "origin": frm, "destination": to, "travelmode": mode}, quote_via=quote)


def gsearch(q):
    return "https://www.google.com/search?" + urlencode({"q": q}, quote_via=quote)


def klook(q):
    return "https://www.klook.com/en-US/search/result/?" + urlencode({"query": q}, quote_via=quote)


def gyg(q):
    return "https://www.getyourguide.com/s/?" + urlencode({"q": q}, quote_via=quote)


def viator(q):
    return "https://www.viator.com/searchResults/all?" + urlencode({"text": q}, quote_via=quote)
