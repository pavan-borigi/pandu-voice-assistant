import google.generativeai as genai
from skills.base_skill import BaseSkill
from utils.config import config
from utils.logger import logger

class ConversationalSkill(BaseSkill):
    def __init__(self):
        super().__init__()
        self.api_key = config.get("skills", {}).get("gemini", {}).get("api_key")
        self.model = None
        if self.api_key and self.api_key != "YOUR_GEMINI_API_KEY_HERE":
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-2.5-flash')
                logger.info("Gemini API configured successfully.")
            except Exception as e:
                logger.error(f"Failed to configure Gemini API: {e}")

    @property
    def intent_name(self) -> str:
        return "conversational"

    def execute(self, entities: dict) -> str:
        query = entities.get("query", "")
        
        if not self.model:
            return "I don't have a Gemini API key configured yet, so I can only do basic tasks."
            
        if not query:
            return "What would you like to talk about?"
            
        try:
            # We add a small system prompt context to keep answers brief
            prompt = f"You are Pandu, a helpful and brief voice assistant. Keep your response under 2 sentences and use conversational language. If the user just says hello, greet them. User says: {query}"
            
            response = self.model.generate_content(prompt)
            return response.text.replace("*", "").strip()
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            return "I'm having trouble connecting to my AI brain right now."
