import importlib
import pkgutil
import inspect
from skills.base_skill import BaseSkill
from utils.logger import logger
import skills

class CommandRouter:
    def __init__(self):
        """Initializes the router and automatically loads all available skills."""
        self.skills = {}
        self._load_skills()

    def _load_skills(self):
        """Dynamically scans the `skills` module and imports any class inheriting from `BaseSkill`."""
        logger.info("Initializing Command Router and loading skills...")
        
        # Iterate through all modules in the 'skills' package
        for _, module_name, is_pkg in pkgutil.iter_modules(skills.__path__):
            if is_pkg:
                continue
                
            full_module_name = f"skills.{module_name}"
            try:
                module = importlib.import_module(full_module_name)
                
                # Find all classes in the module that inherit from BaseSkill (but are not BaseSkill itself)
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if issubclass(obj, BaseSkill) and obj is not BaseSkill:
                        skill_instance = obj()
                        intent_name = skill_instance.intent_name
                        self.skills[intent_name] = skill_instance
                        logger.debug(f"Loaded skill '{name}' handling intent '{intent_name}'.")

            except Exception as e:
                logger.error(f"Failed to load skill module {full_module_name}: {e}")

        logger.info(f"Loaded {len(self.skills)} skills: {list(self.skills.keys())}")

    def route_and_execute(self, intent: str, entities: dict) -> str:
        """Routes the command to the appropriate skill and returns the response."""
        if intent == "unknown":
            return "I'm sorry, I didn't quite catch what you meant to do."
            
        skill = self.skills.get(intent)
        if not skill:
            logger.warning(f"No skill found to handle intent: {intent}")
            return "I understood your command, but I don't have a skill to handle it right now."
            
        try:
            # Execute the skill
            response = skill.execute(entities)
            return response
        except Exception as e:
            logger.error(f"Error executing skill for intent '{intent}': {e}")
            return "I ran into a problem while trying to do that for you."

# Global Router Instance (we instantiate this at startup)
command_router = CommandRouter()
