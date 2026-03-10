from datetime import datetime
from skills.base_skill import BaseSkill

class SystemSkill(BaseSkill):
    @property
    def intent_name(self) -> str:
        return "system"

    def execute(self, entities: dict) -> str:
        action = entities.get("action", "time")
        
        if action == "time":
            now = datetime.now()
            time_str = now.strftime("%I:%M %p")
            return f"The time is {time_str}."
            
        elif action == "date":
            now = datetime.now()
            date_str = now.strftime("%A, %B %d, %Y")
            return f"Today is {date_str}."
            
        return "I can help you with the current time and date."
