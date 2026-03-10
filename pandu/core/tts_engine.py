import threading
import queue
import os
import pygame
from gtts import gTTS
from utils.logger import logger

class TTSEngine:
    def __init__(self):
        """Initializes the Text-to-Speech engine securely in a background thread."""
        self.q = queue.Queue()
        try:
            pygame.mixer.init()
            self.engine_ready = True
        except Exception as e:
            logger.error(f"Failed to initialize Pygame mixer: {e}")
            self.engine_ready = False
            
        self.thread = threading.Thread(target=self._tts_worker, daemon=True)
        self.thread.start()

    def _tts_worker(self):
        """Dedicated thread to handle audio rendering via gTTS and Pygame."""
        counter = 0
        while True:
            text = self.q.get()
            if text is None:
                self.q.task_done()
                break
                
            if self.engine_ready:
                logger.info(f"Pandu says: {text}")
                try:
                    # Create MP3
                    tts = gTTS(text=text, lang='en', tld='co.in', slow=False)
                    filename = f"temp_tts_{os.getpid()}_{counter}.mp3"
                    counter += 1
                    tts.save(filename)
                    
                    # Play MP3
                    pygame.mixer.music.load(filename)
                    pygame.mixer.music.play()
                    
                    # Wait for playback to finish
                    while pygame.mixer.music.get_busy():
                        pygame.time.Clock().tick(10)
                        
                    # Unload so we can delete the file on Windows
                    pygame.mixer.music.unload()
                    
                    try:
                        os.remove(filename)
                    except OSError:
                        pass # Ignore if file cannot be deleted immediately
                except Exception as e:
                    logger.error(f"Error during TTS playback: {e}")
            self.q.task_done()

    def speak(self, text: str):
        """Speaks the given text synchronously, blocking until finished."""
        if not self.thread.is_alive():
            logger.error("TTS thread is not running.")
            return
            
        self.q.put(text)
        self.q.join() # Wait until the worker thread has spoken the text

    def speak_async(self, text: str):
        """Speaks the given text in the background without blocking."""
        if not self.thread.is_alive():
            logger.error("TTS thread is not running.")
            return
            
        self.q.put(text)

# Global instance for shared use across modules
tts = TTSEngine()
