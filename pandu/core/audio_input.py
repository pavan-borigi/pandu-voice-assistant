import speech_recognition as sr
from core.stt_engine import stt
from utils.logger import logger
from utils.config import config
import time

class AudioInput:
    def __init__(self):
        """Initializes the Audio Input module."""
        self.recognizer = sr.Recognizer()
        
        # Dynamic energy threshold calibration
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.energy_threshold = 4000
        
        self.wake_word = config.get("assistant", {}).get("wake_word", "pandu").lower()
        
    def calibrate_microphone(self):
        """Calibrates the microphone for ambient noise."""
        logger.info("Calibrating microphone for ambient noise...")
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
        logger.info("Microphone calibrated.")

    def listen_for_wake_word(self) -> bool:
        """Listens continuously until the wake word is detected."""
        logger.info(f"Listening for wake word: '{self.wake_word}'...")
        with sr.Microphone() as source:
            while True:
                try:
                    # Listen for a short phrase
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=3)
                    text = stt.transcribe(audio)
                    if not text:
                        continue
                    
                    if self.wake_word in text:
                        logger.info(f"Wake word '{self.wake_word}' detected!")
                        return True
                except sr.WaitTimeoutError:
                    pass # Just loop and listen again
                except Exception as e:
                    logger.error(f"Error in wake word detection: {e}")
                    time.sleep(1)

    def listen_for_command(self) -> str:
        """Listens for the user's main command after the wake word."""
        logger.info("Listening for command...")
        with sr.Microphone() as source:
            try:
                # We give the user 5 seconds to start speaking, and up to 10 seconds of speech
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                command = stt.transcribe(audio)
                if command:
                    logger.info(f"Command received: {command}")
                return command
            except sr.WaitTimeoutError:
                logger.debug("Command listening timed out.")
                return ""
            except Exception as e:
                logger.error(f"Error listening for command: {e}")
                return ""

# Global instance
audio_input = AudioInput()
