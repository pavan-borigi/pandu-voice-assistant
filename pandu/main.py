import sys
import threading
import time
from pathlib import Path
import pystray
from PIL import Image, ImageDraw

from utils.logger import logger
from core.audio_input import audio_input
from core.nlp_engine import nlp_engine
from core.command_router import command_router
from core.tts_engine import tts

class PanduApp:
    def __init__(self):
        self.running = False
        self.icon = None

    def create_icon_image(self):
        """Generates a simple system tray icon dynamically."""
        width = 64
        height = 64
        color1 = (30, 30, 30)
        color2 = (0, 150, 255)
        
        image = Image.new('RGB', (width, height), color1)
        dc = ImageDraw.Draw(image)
        dc.rectangle(
            (width // 4, height // 4, width * 3 // 4, height * 3 // 4),
            fill=color2
        )
        return image

    def start_listening_loop(self):
        """The main loop that listens for wake word and commands."""
        # Initial calibration
        audio_input.calibrate_microphone()
        tts.speak_async("Pandu is online and ready.")
        
        while self.running:
            try:
                # 1. Listen for Wake Word
                if not audio_input.listen_for_wake_word():
                    time.sleep(1)
                    continue

                # Acknowledge wake word (synchronously so it doesn't overlap with microphone)
                tts.speak("Yes?")
                
                # 2. Listen for Command
                command_text = audio_input.listen_for_command()
                if not command_text:
                    continue
                
                # 3. Process with NLP
                nlp_result = nlp_engine.extract_intent_and_entities(command_text)
                intent = nlp_result["intent"]
                entities = nlp_result["entities"]
                
                logger.info(f"Parsed Intent: {intent}, Entities: {entities}")
                
                # 4. Route to Skill and Execute
                response = command_router.route_and_execute(intent, entities)
                
                # 5. Output Response
                tts.speak(response)
                
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                time.sleep(2)

    def on_quit(self, icon, item):
        """Handler for the Quit menu item."""
        logger.info("Quitting Pandu...")
        self.running = False
        icon.stop()

    def run(self):
        """Starts the application."""
        self.running = True
        
        # Start the background listening thread
        listen_thread = threading.Thread(target=self.start_listening_loop, daemon=True)
        listen_thread.start()

        # Set up the system tray icon
        logger.info("Setting up system tray icon...")
        menu = pystray.Menu(
            pystray.MenuItem('Quit', self.on_quit)
        )
        
        self.icon = pystray.Icon("Pandu", self.create_icon_image(), "Pandu Voice Assistant", menu)
        
        # This blocks until the icon is stopped
        self.icon.run()

if __name__ == "__main__":
    app = PanduApp()
    try:
        app.run()
    except KeyboardInterrupt:
        logger.info("Exiting...")
        sys.exit(0)
