# modules/github_connector.py

import os, json
from urllib.parse import urlencode
from flask import session, redirect, request
import requests

CLIENT_ID     = os.getenv("GITHUB_CLIENT_ID")
CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
REDIRECT_URI  = os.getenv("GITHUB_REDIRECT_URI")
SCOPES        = "repo"

class GitHubConnector:

    @staticmethod
    def oauth_login():
        params = {
          "client_id": CLIENT_ID,
          "redirect_uri": REDIRECT_URI,
          "scope": SCOPES,
        }
        url = f"https://github.com/login/oauth/authorize?{urlencode(params)}"
        return redirect(url)

    @staticmethod
    def oauth_callback():
        code = request.args.get("code")
        resp = requests.post("https://github.com/login/oauth/access_token", {
            "client_id":CLIENT_ID,
            "client_secret":CLIENT_SECRET,
            "code":code
        }, headers={"Accept":"application/json"})
        data = resp.json()
        session["gh_token"] = data["access_token"]
        return redirect("/")

    @staticmethod
    def commit_file(path: str, content: str, message: str):
        token = session.get("gh_token")
        if not token:
            raise Exception("Not authenticated")
        owner, repo = os.getenv("GITHUB_REPO").split("/")
        api = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
        # Fetch SHA if exists
        get = requests.get(api, headers={"Authorization":f"token {token}"})
        sha = get.json().get("sha")
        payload = {
          "message": message,
          "content": content.encode("utf-8").decode("ascii"),
          "sha": sha
        }
        r = requests.put(api, json=payload, headers={"Authorization":f"token {token}"})
        return r.json()
