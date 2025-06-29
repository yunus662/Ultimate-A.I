# app.py
"""
AI Backend API Server
=====================
Flask server to bridge frontend (admin_ui.html) with backend AI modules.
Handles:
  - Command execution
  - GitHub file updates
  - Optional file fetch
"""

from flask import Flask, request, jsonify
from modules.github_connecter import GitHubConnecter
from modules.personality import AIPersonality
from modules.web_surfer import WebSurfer
from core import AICore
from security import security_check
import os

app = Flask(__name__)

# === Configuration ===
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN") or "your-github-token"
GITHUB_REPO = os.getenv("GITHUB_REPO") or "your-username/your-repo"
ADMIN_KEY = os.getenv("ADMIN_KEY") or "secret-key"  # simple API auth

# === Initialize AI Core ===
ai = AICore(GITHUB_TOKEN, GITHUB_REPO)


# === Helper: Simple API Key Authentication ===
def require_auth(req):
    key = req.headers.get("X-Admin-Key")
    return key == ADMIN_KEY


# === API Routes ===

@app.route("/api/execute", methods=["POST"])
def api_execute():
    if not require_auth(request):
        return jsonify({"result": "[Unauthorized] Invalid admin key."}), 401

    data = request.get_json()
    command = data.get("command", "")
    args = command.split()[1:]  # simple splitting
    base_cmd = command.split()[0]

    result = ai.execute(base_cmd, *args)
    return jsonify({"result": result})


@app.route("/api/update_file", methods=["POST"])
def api_update_file():
    if not require_auth(request):
        return jsonify({"message": "[Unauthorized] Invalid admin key."}), 401

    data = request.get_json()
    path = data.get("path")
    content = data.get("content")

    if not path or not content:
        return jsonify({"message": "[Error] Missing path or content."}), 400

    result = ai.github.update_file(path, content)
    return jsonify({"message": result})


@app.route("/api/fetch_file", methods=["POST"])
def api_fetch_file():
    if not require_auth(request):
        return jsonify({"message": "[Unauthorized] Invalid admin key."}), 401

    data = request.get_json()
    path = data.get("path")

    if not path:
        return jsonify({"message": "[Error] Missing path."}), 400

    result = ai.github.fetch_file(path)
    return jsonify({"content": result})


# === Optional: Health Check ===
@app.route("/api/status")
def api_status():
    return jsonify({
        "ai": "online",
        "modules": ["GitHub", "WebSurfer", "Personality", "Security"],
        "version": ai.personality.version
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
