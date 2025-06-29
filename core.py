# core.py
"""
AI Core Controller
==================
Orchestrates internal modules like GitHub, Web Surfer, Personality, and Security.
"""

from github_connecter import GitHubConnecter
from web_surfer import WebSurfer
from personality import AIPersonality


class AICore:
    def __init__(self, github_token, github_repo):
        self.personality = AIPersonality()
        self.github = GitHubConnecter(github_token, github_repo)
        self.web = WebSurfer()

    def execute(self, command: str, *args) -> str:
        if not security_check(command, args):
            return "[Security] This action is not permitted."

        if command == "describe":
            return str(self.personality.describe())

        elif command == "search_web":
            query = args[0]
            return "\n".join(self.web.search(query))

        elif command == "fetch_code":
            path = args[0]
            return self.github.fetch_file(path)

        elif command == "update_code":
            path, content = args
            return self.github.update_file(path, content)

        else:
            return f"[Unknown] Command '{command}' not recognized."
