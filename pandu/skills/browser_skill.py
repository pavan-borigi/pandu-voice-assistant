import webbrowser
import urllib.parse
from skills.base_skill import BaseSkill

class BrowserSkill(BaseSkill):
    @property
    def intent_name(self) -> str:
        return "browser"

    def execute(self, entities: dict) -> str:
        query = entities.get("query")
        
        if not query:
            return "What would you like me to search for?"
            
        # URL encode the query for Google Search
        encoded_query = urllib.parse.quote(query)
        search_url = f"https://www.google.com/search?q={encoded_query}"
        
        try:
            webbrowser.open(search_url)
            return f"Here is what I found on the web for {query}."
        except Exception as e:
            from utils.logger import logger
            logger.error(f"Failed to open browser: {e}")
            return "I tried to search the web, but I ran into a problem opening the browser."
