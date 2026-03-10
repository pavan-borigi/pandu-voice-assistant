import spacy
from utils.logger import logger

class NLPEngine:
    def __init__(self):
        """Initializes the NLP Engine using spaCy."""
        try:
            # We use the small English model for fast, offline execution
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("spaCy model loaded successfully.")
        except Exception as e:
            logger.warning(f"Could not load spaCy model 'en_core_web_sm'. Fallback to basic regex matching. Error: {e}")
            self.nlp = None

    def extract_intent_and_entities(self, text: str) -> dict:
        """
        Parses the input text to determine the intent and extract relevant entities.
        Returns a dictionary containing 'intent' and 'entities'.
        """
        result = {
            "intent": "unknown",
            "entities": {}
        }

        if not text:
            return result

        doc = self.nlp(text.lower()) if self.nlp else None
        
        # Simple rule-based intent matching for efficiency
        # An advanced system would use a trained Intent Classifier (e.g. Rasa NLU, Transformers)
        if any(word in text.lower() for word in ["weather", "temperature", "forecast", "hot", "cold"]):
            result["intent"] = "weather"
            if doc:
                # Extract Location entity (GPE: Geopolitical entity)
                locations = [ent.text for ent in doc.ents if ent.label_ == "GPE"]
                if locations:
                    result["entities"]["location"] = locations[0]
                    
        elif any(word in text.lower() for word in ["search", "google", "look up", "find online"]):
            result["intent"] = "browser"
            # Extract search query
            # E.g. "search for python tutorials" -> "python tutorials"
            query = text.lower()
            for trigger in ["search for", "search", "google", "look up", "find online"]:
                if trigger in query:
                    query = query.replace(trigger, "").strip()
            result["entities"]["query"] = query
            
        elif any(word in text.lower() for word in ["open", "launch", "start"]):
            result["intent"] = "app_launcher"
            app_name = text.lower()
            
            # Remove common conversational prefixes before the trigger word
            prefixes = ["could you ", "can you ", "please ", "would you "]
            for prefix in prefixes:
                if app_name.startswith(prefix):
                    app_name = app_name[len(prefix):]
                    
            # Try to extract the app name. It's usually after the trigger word.
            # E.g. "open chrome" -> "chrome", "could you open chrome" -> "chrome"
            for trigger in ["open ", "launch ", "start "]:
                if trigger in app_name:
                    app_name = app_name.split(trigger, 1)[-1].strip()
                    break
            else:
                for trigger in ["open", "launch", "start"]:
                    if trigger in app_name:
                        app_name = app_name.replace(trigger, "").strip()
            
            result["entities"]["app_name"] = app_name
            
        elif any(word in text.lower() for word in ["time", "date", "day", "battery"]):
            result["intent"] = "system"
            if "time" in text.lower():
                result["entities"]["action"] = "time"
            elif "date" in text.lower() or "day" in text.lower():
                result["entities"]["action"] = "date"
                
        else:
            # Fallback for anything else: route to Gemini for conversational response
            result["intent"] = "conversational"
            result["entities"]["query"] = text
            
        return result

# Global Instance
nlp_engine = NLPEngine()
