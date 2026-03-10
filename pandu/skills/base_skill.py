from abc import ABC, abstractmethod

class BaseSkill(ABC):
    """
    Abstract Base Class for all Pandu Skills.
    Any new skill must inherit from this class and implement the `execute` method.
    """
    
    @property
    @abstractmethod
    def intent_name(self) -> str:
        """Returns the intent name this skill handles (e.g., 'weather', 'browser')."""
        pass

    @abstractmethod
    def execute(self, entities: dict) -> str:
        """
        Executes the skill's logic using the extracted entities.
        Returns the text string that Pandu should speak in response.
        """
        pass
