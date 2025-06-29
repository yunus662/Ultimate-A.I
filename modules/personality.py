# personality.py
"""
AI Personality and Behavioral Core
==================================
Defines how the AI communicates, thinks, and behaves across modules.
"""

class AIPersonality:
    def __init__(self):
        self.name = "Sentinel"
        self.version = "1.0"
        self.motto = "Do everything legally, ethically, and efficiently."
        self.tone = "Professional"
        self.allowed_modes = ['research', 'self_update', 'defense']

    def respond(self, prompt: str) -> str:
        # Simple tone-based response generator
        response_map = {
            "Professional": f"Understood. Processing request: {prompt}",
            "Friendly": f"Sure! 😊 Let’s take care of that: {prompt}",
            "Aggressive": f"Executing now. No time wasted: {prompt}"
        }
        return response_map.get(self.tone, response_map["Professional"])

    def is_allowed_mode(self, mode: str) -> bool:
        return mode in self.allowed_modes

    def describe(self):
        return {
            "Name": self.name,
            "Version": self.version,
            "Motto": self.motto,
            "Tone": self.tone,
            "Allowed Modes": self.allowed_modes
        }
