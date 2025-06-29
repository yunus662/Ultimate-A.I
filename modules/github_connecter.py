# github_connecter.py
"""
GitHub Connecter Module
=======================
Handles all GitHub interactions: fetching, committing, and pushing code.
Used by the AI to update its own repository within security constraints.
"""

import os
from github import Github
from security import is_operation_safe

class GitHubConnecter:
    def __init__(self, token: str, repo_name: str):
        self.token = token
        self.repo_name = repo_name
        self.client = Github(self.token)
        self.repo = self.client.get_repo(self.repo_name)

    def fetch_file(self, path: str):
        try:
            file_content = self.repo.get_contents(path)
            return file_content.decoded_content.decode('utf-8')
        except Exception as e:
            return f"[Error] Failed to fetch {path}: {e}"


        try:
            file = self.repo.get_contents(path)
            self.repo.update_file(path, commit_message, new_content, file.sha)
            return f"[Success] {path} updated."
        except Exception as e:
            return f"[Error] Update failed: {e}"

    def create_file(self, path: str, content: str, message="Create via AI"):
        if not is_operation_safe('create_file', path, content):
            return "[Security] Operation blocked by policy."

        try:
            self.repo.create_file(path, message, content)
            return f"[Success] {path} created."
        except Exception as e:
            return f"[Error] Creation failed: {e}"
