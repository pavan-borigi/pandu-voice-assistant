import speech_recognition as sr
from utils.logger import logger

class STTEngine:
    def __init__(self):
        """Initializes the Speech-to-Text engine."""
        self.recognizer = sr.Recognizer()

    def transcribe(self, audio_data: sr.AudioData, language: str = "en-US") -> str:
        """Transcribes the given audio data into text using Google Web Speech API."""
        try:
            # Using Google Web Speech API for simplicity and speed.
            # In a fully offline production system, this could be swapped with Vosk or Whisper.
            text = self.recognizer.recognize_google(audio_data, language=language)
            logger.debug(f"Transcribed Text: {text}")
            return text.lower()
        except sr.UnknownValueError:
            logger.debug("STT could not understand the audio.")
            return ""
        except sr.RequestError as e:
            logger.error(f"Could not request results from STT service; {e}")
            return ""
        except Exception as e:
            logger.error(f"Unexpected error in STT: {e}")
            return ""

# Global instance for shared use
stt = STTEngine()
