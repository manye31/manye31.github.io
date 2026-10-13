#!/usr/bin/env python3
"""One-time helper: log in to Spotify and print a refresh token for bin/spotify_fetch.py.

1. Create an app at https://developer.spotify.com/dashboard
   - Redirect URI: http://127.0.0.1:8888/callback
   - API: Web API
2. Run:  SPOTIFY_CLIENT_ID=... SPOTIFY_CLIENT_SECRET=... python3 bin/spotify_auth.py
3. Approve in the browser. The refresh token is printed here; store it (with the client ID and secret)
   as GitHub repository secrets: SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REFRESH_TOKEN.
"""
import base64
import http.server
import json
import os
import secrets
import sys
import urllib.parse
import urllib.request
import webbrowser

REDIRECT_URI = "http://127.0.0.1:8888/callback"
SCOPE = "user-top-read"


def main():
    client_id = os.environ.get("SPOTIFY_CLIENT_ID")
    client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")
    if not client_id or not client_secret:
        sys.exit("Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET first (from your app's page on developer.spotify.com).")

    state = secrets.token_urlsafe(16)
    auth_url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode(
        {"client_id": client_id, "response_type": "code", "redirect_uri": REDIRECT_URI, "scope": SCOPE, "state": state}
    )
    result = {}

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            if query.get("state", [None])[0] != state or "code" not in query:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Login failed or was cancelled. Check the terminal.")
                result["error"] = query.get("error", ["unknown error"])[0]
                return
            result["code"] = query["code"][0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Done! You can close this tab and go back to the terminal.")

        def log_message(self, *args):
            pass

    print("Opening Spotify in your browser. If it doesn't open, visit:\n" + auth_url)
    webbrowser.open(auth_url)
    server = http.server.HTTPServer(("127.0.0.1", 8888), Handler)
    while not result:
        server.handle_request()
    if "error" in result:
        sys.exit("Spotify login failed: " + result["error"])

    basic = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    request = urllib.request.Request(
        "https://accounts.spotify.com/api/token",
        data=urllib.parse.urlencode(
            {"grant_type": "authorization_code", "code": result["code"], "redirect_uri": REDIRECT_URI}
        ).encode(),
        headers={"Authorization": "Basic " + basic, "Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(request) as response:
        tokens = json.load(response)
    print("\nYour refresh token (save it as the GitHub secret SPOTIFY_REFRESH_TOKEN):\n")
    print(tokens["refresh_token"])


if __name__ == "__main__":
    main()
