# modules/personality.py

import json, os
from threading import Lock

PERSONA_FILE = "data/personality.json"
_lock = Lock()

class Personality:
    def __init__(self):
        os.makedirs(os.path.dirname(PERSONA_FILE), exist_ok=True)
        if not os.path.exists(PERSONA_FILE):
            with open(PERSONA_FILE,"w") as f:
                json.dump({"bio":[], "preferences":{}}, f)
        with open(PERSONA_FILE,"r") as f:
            self.data = json.load(f)

    def log_interaction(self, user_msg: str, ai_reply: str):
        with _lock:
            self.data["bio"].append({"user":user_msg, "ai":ai_reply})
            # keep last N exchanges
            self.data["bio"] = self.data["bio"][-50:]
            self._save()

    def _save(self):
        with open(PERSONA_FILE,"w") as f:
            json.dump(self.data, f, indent=2)

    def get_persona_prompt(self) -> str:
        # Build a system prompt from stored exchanges
        lines = ["You are J.A.R.V.I.S., a personal AI that remembers user likes/dislikes."]
        for ex in self.data["bio"]:
            lines.append(f"User said: “{ex['user']}”")
            lines.append(f"AI replied: “{ex['ai']}”")
        return "\n".join(lines)
