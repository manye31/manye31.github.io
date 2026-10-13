#!/usr/bin/env python3
"""Save my recent Letterboxd diary (from the public RSS feed) to _data/letterboxd.json for the site.

Letterboxd has no public API and its feed can't be read from the browser, so this runs daily in
.github/workflows/hobby-data.yml. No login needed. Run locally with:  python3 bin/letterboxd_fetch.py
"""
import datetime
import html
import json
import os
import re
import urllib.request
import xml.etree.ElementTree as ET

USERNAME = "manye31"
OUT = os.path.join(os.path.dirname(__file__), "..", "_data", "letterboxd.json")
NS = {"letterboxd": "https://letterboxd.com", "tmdb": "https://themoviedb.org"}


def text(item, tag):
    node = item.find(tag, NS)
    return node.text.strip() if node is not None and node.text else ""


def main():
    request = urllib.request.Request(
        f"https://letterboxd.com/{USERNAME}/rss/", headers={"User-Agent": "manye31.github.io hobby page"}
    )
    with urllib.request.urlopen(request) as response:
        root = ET.fromstring(response.read())

    films = []
    for item in root.iter("item"):
        title = text(item, "letterboxd:filmTitle")
        if not title:  # lists and other non-diary posts
            continue
        description = text(item, "description")
        poster = re.search(r'<img src="([^"]+)"', description)
        poster = poster.group(1) if poster else None
        # Review text: every paragraph except the poster and Letterboxd's spoiler notice
        paragraphs = [html.unescape(re.sub(r"<[^>]+>", "", p)).strip() for p in re.findall(r"<p>(.*?)</p>", description, re.S)]
        review = "\n\n".join(p for p in paragraphs if p and "contain spoilers" not in p)
        rating = text(item, "letterboxd:memberRating")
        films.append(
            {
                "title": title,
                "year": text(item, "letterboxd:filmYear"),
                "rating": float(rating) if rating else None,
                "liked": text(item, "letterboxd:memberLike") == "Yes",
                "rewatch": text(item, "letterboxd:rewatch") == "Yes",
                "watched": text(item, "letterboxd:watchedDate"),
                "spoilers": "(contains spoilers)" in text(item, "title"),
                "review": review,
                "url": text(item, "link"),
                # Letterboxd serves several poster sizes from the same address; the grid uses the small one
                "poster": poster.replace("-0-600-0-900-", "-0-230-0-345-") if poster else None,
                "poster_large": poster,
            }
        )
    films.sort(key=lambda f: f["watched"], reverse=True)

    data = {"username": USERNAME, "updated": datetime.date.today().isoformat(), "films": films}

    # Only rewrite the file when the diary changed, so the daily job doesn't commit just to bump the date
    try:
        with open(OUT) as f:
            if json.load(f).get("films") == films:
                print("No changes")
                return
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    with open(OUT, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"Wrote {len(films)} films to {OUT}")


if __name__ == "__main__":
    main()
