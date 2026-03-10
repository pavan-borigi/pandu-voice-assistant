import os
import subprocess
from skills.base_skill import BaseSkill
from utils.logger import logger

class AppLauncherSkill(BaseSkill):
    def __init__(self):
        super().__init__()
        # Common Windows applications mapped to their process names
        self.app_map = {
            "calculator": "calc",
            "notepad": "notepad",
            "browser": "msedge",
            "chrome": "chrome",
            "edge": "msedge",
            "cmd": "cmd",
            "terminal": "wt",
            "word": "winword",
            "excel": "excel",
            "paint": "mspaint"
        }

    @property
    def intent_name(self) -> str:
        return "app_launcher"

    def execute(self, entities: dict) -> str:
        app_name = entities.get("app_name")
        
        if not app_name:
            return "Which application would you like me to open?"

        # Normalize the name
        app_name = app_name.lower().strip()
        
        # Check if we know this app
        process_name = self.app_map.get(app_name)
        
        if process_name:
            try:
                # Use subprocess to start the application
                subprocess.Popen(f"start {process_name}", shell=True)
                return f"Opening {app_name}."
            except Exception as e:
                logger.error(f"Failed to launch app '{app_name}': {e}")
                return f"I had trouble launching {app_name}."
        else:
            # Fallback: Try launching it directly just in case the user provided a valid system alias
            try:
                subprocess.Popen(f"start {app_name}", shell=True)
                return f"Attempting to open {app_name}."
            except Exception:
                return f"I'm not sure how to open the application {app_name}. I only know a few basic ones right now."
