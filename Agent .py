import os
import google.generativeai as genai

class Agent:
    def __init__(self, name: str, persona: str, location: str, system_prompt: str = ""):
        self.name = name
        self.persona = persona
        self.location = location
        self.system_prompt = system_prompt
        self.emotion = "Calm"
        self.memory = []

        api_key = os.environ.get("GEMINI_API_KEY", "YOUR_API_KEY")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def remember(self, observation: str, action: str):
        self.memory.append({"observation": observation, "action": action})

    def act(self, observation: str) -> str:
        prompt = f"""
System Directive: {self.system_prompt}
Role / Persona: You are {self.name}. {self.persona}
Current Location: {self.location}
Current Emotional State: {self.emotion}

Language Constraint: Respond strictly in English. However, reflect Arabic cultural nuances, concepts, logic, and phrasing directly through the English expression where relevant.

Recent Memory:
{self.memory[-5:]}

Current Observation: {observation}

Task: Decide on your next action or response as {self.name}:
"""
        response = self.model.generate_content(prompt)
        action_text = response.text.strip()
        self.remember(observation, action_text)
        return action_text

