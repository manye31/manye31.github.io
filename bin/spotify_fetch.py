#!/usr/bin/env python3
"""Fetch my Spotify top artists and write them to _data/spotify.json for the site.

Needs SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET and SPOTIFY_REFRESH_TOKEN (see bin/spotify_auth.py).
Runs daily in .github/workflows/hobby-data.yml; can also be run locally.
"""
import base64
import datetime
import json
import os
import sys
import urllib.parse
import urllib.request

OUT = os.path.join(os.path.dirname(__file__), "..", "_data", "spotify.json")
LIMIT = 10
# Spotify's three windows for "top" items
RANGES = [
    ("short_term", "Last month"),
    ("medium_term", "Last 6 months"),
    ("long_term", "Last year"),
]


def access_token():
    client_id = os.environ["SPOTIFY_CLIENT_ID"]
    client_secret = os.environ["SPOTIFY_CLIENT_SECRET"]
    basic = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    request = urllib.request.Request(
        "https://accounts.spotify.com/api/token",
        data=urllib.parse.urlencode(
            {"grant_type": "refresh_token", "refresh_token": os.environ["SPOTIFY_REFRESH_TOKEN"]}
        ).encode(),
        headers={"Authorization": "Basic " + basic, "Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(request) as response:
        return json.load(response)["access_token"]


def get(path, token):
    request = urllib.request.Request("https://api.spotify.com/v1" + path, headers={"Authorization": "Bearer " + token})
    with urllib.request.urlopen(request) as response:
        return json.load(response)


def image(images, smallest_over=300):
    """Pick the smallest image that's still at least ~300px, so the page stays light."""
    if not images:
        return None
    usable = [i for i in images if (i.get("width") or 0) >= smallest_over] or images
    return min(usable, key=lambda i: i.get("width") or 0)["url"]


def main():
    token = access_token()
    data = {"sample": False, "updated": datetime.date.today().isoformat(), "ranges": []}
    for key, label in RANGES:
        artists = get(f"/me/top/artists?time_range={key}&limit={LIMIT}", token)["items"]

        # Top genres, weighted so higher-ranked artists count more (Spotify may return no genres for some artists)
        weights = {}
        for rank, artist in enumerate(artists):
            for genre in artist.get("genres") or []:
                weights[genre] = weights.get(genre, 0) + (LIMIT - rank)
        genres = [g for g, _ in sorted(weights.items(), key=lambda kv: -kv[1])][:5]

        data["ranges"].append(
            {
                "key": key,
                "label": label,
                "genres": genres,
                "artists": [
                    {"name": a["name"], "url": a["external_urls"]["spotify"], "image": image(a.get("images"))}
                    for a in artists
                ],
            }
        )

    # Only rewrite the file when the top lists changed, so the daily job doesn't commit just to bump the date
    try:
        with open(OUT) as f:
            previous = json.load(f)
        if not previous.get("sample") and previous.get("ranges") == data["ranges"]:
            print("No changes")
            return
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    with open(OUT, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    try:
        main()
    except KeyError as e:
        sys.exit(f"Missing environment variable {e}. See bin/spotify_auth.py.")
